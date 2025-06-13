import random
from collections import defaultdict
from types import NoneType

from request.config_structs import Output
from request.expression import safe_eval_helper, safe_eval
from error.exception import ConfigValueError
from input_generator.base_generator import BaseConfig, BaseGenerator, TYPE_FUNCTION

from input_generator.line_generator import line_generator


class MatrixConfig(BaseConfig):
    def __init__(self, variables: dict[str, tuple[int, str]], config: dict[str, str]):
        self.col_size = safe_eval_helper(variables, config, 'col_size', None) # 필수
        self.row_size = safe_eval_helper(variables, config, 'row_size', '1')
        self.num_type = config.get('num_type', 'int')

        self.num_range = self._range_simplify(config.get('num_range', [[1, 255]]), variables)
        self.is_distinct = config.get('is_distinct', False) # ranges에서 각 수가 한 번 씩만 나오게 할지 여부
        self.value_limit = self._value_limit_simplify(self.num_range, config.get('value_limit', {})) # 특정 valuee가 일정 횟수 이상 나오지 못 하도록 할지 여부. {1: 3} 처럼 사용. distinct 있어도 이거 있으면 이거 우선
        self.empty_value = config.get('empty_value', None) # is_distinct가 True일 때 가능한 숫자를 모두 썼으면 사용할 숫자. None이면 비활성화
        self.random_empty = config.get('random_empty', False) # empty_value가 있어도 빈 공간을 최대한 제거할지 아니면 최대한 채울지

        self.is_graph = safe_eval_helper(variables, config, 'is_graph', False) # 이거 True면 col/row인덱스 같은곳이 0
        self.is_symmetric = config.get('is_symmetric', False) # 이거 True면 대칭
        self.validate()

    def _range_simplify(self, ranges, variables):
        if not ranges:
            return []
        try:
            ranges_as_int = [*map(lambda x: [safe_eval(x[0], variables), safe_eval(x[1], variables)], ranges)]
        except Exception as e:
            print(e)
            return []
        sorted_ranges = sorted(ranges_as_int)
        merged = [sorted_ranges[0]]
        for s, e in sorted_ranges[1:]:
            last_s, last_e = merged[-1]
            if last_e >= s - 1:
                merged[-1][1] = max(last_e, e)
            else:
                merged.append([s, e])
        return merged

    def _value_limit_simplify(self, merged_ranges, value_limit):
        current_index = 0
        filtered_value_limit = {}
        for key in sorted(value_limit.keys()):
            while current_index < len(merged_ranges) and not merged_ranges[current_index].min <= key <= merged_ranges[current_index].max:
                current_index += 1
            if current_index != len(merged_ranges):
                filtered_value_limit[key] = value_limit[key]
        return filtered_value_limit

    def validate(self):
        if self.num_type == 'char' and any(s < 0 or e > 255 for s, e in self.num_range):
            raise ConfigValueError('num_range', 'char형일 경우 range는 0 이상 255 이하여야 합니다.')
        if type(self.col_size) is str:
            raise ConfigValueError('col_size', 'col_size는 int여야 합니다.')
        if type(self.row_size) is str:
            raise ConfigValueError('row_size', 'row_size는 int여야 합니다.')
        if self.col_size < 0:
            raise ConfigValueError('col_size', 'col_size는 음수일 수 없습니다.')
        if self.row_size < 0:
            raise ConfigValueError('row_size', 'row_size는 음수일 수 없습니다.')

        matrix_size = self.row_size * self.col_size
        if matrix_size >= 1_000_000:
            raise ConfigValueError('col_size and row_size', 'col_size와 row_size의 곱은 100만을 넘을 수 없습니다.')

        if type(self.empty_value) not in [int, str, NoneType]:
            raise ConfigValueError('empty_value', f'empty_value의 타입은 int, char, None만 허용됩니다.')
        if self.empty_value is None and self.random_empty:
            raise ConfigValueError('random_empty', f'empty_value가 미설정 되었을 경우 random_empty는 사용할 수 없습니다.')

        if len(self.num_range) > 100:
            raise ConfigValueError('num_range', f'num_range의 길이가 100 이하여야 합니다. 현재는 {len(self.num_range)}입니다.')
        range_num_cnt = sum(e-s+1 for s, e in self.num_range)
        if self.is_distinct and range_num_cnt < matrix_size and self.empty_value is None:
            raise ConfigValueError('num_range', f'사용할 수 있는 수의 개수가 {range_num_cnt}개지만, 행렬의 크기는 {matrix_size}이며, is_distinct가 활성화되어있습니다.')
        value_limit_cnt = sum(self.value_limit.values())
        if len(self.value_limit) == range_num_cnt and value_limit_cnt < matrix_size and self.empty_value is None:
            raise ConfigValueError('value_limit', f'range에 포함된 모든 수에 value_limit이 걸려있으며, 유효한 value_limit이 걸린 모든 합은 {value_limit_cnt}이고 행렬의 크기는 {matrix_size}입니다.')

        if self.is_graph and self.row_size != self.col_size:
            raise ConfigValueError('col_size and row_size', f"행렬 그래프로 설정되었지만 행렬이 정사각형이 아닙니다. {self.row_size}*{self.col_size}")
        if self.is_symmetric and self.row_size != self.col_size:
            raise ConfigValueError('col_size and row_size', f"대칭 그래프로 설정되었지만 행렬이 정사각형이 아닙니다. {self.row_size}*{self.col_size}")

class RangeManager:
    def __init__(self, num_ranges: list[list[int, int]], value_limit: dict, is_distinct: bool):
        self.ranges = [i[:] for i in num_ranges]
        self.value_limit = value_limit
        self.is_distinct = is_distinct
        self.use_count = defaultdict(int)

    def _adjust_range(self, index, select) -> None:
        self.use_count[select] += 1
        if self.is_distinct and not select in self.value_limit:
            self.value_limit[select] = 1

        # 현재 수를 다 썼다면 업데이트
        if self.use_count[select] == self.value_limit.get(select, -1):
            start, end = self.ranges[index]
            sep = [[start, select-1], [select+1, end]]
            new_ranges = [[s, e] for s, e in sep if s <= e]
            if len(new_ranges) == 1:
                self.ranges[index] = new_ranges[0]
            elif len(new_ranges) == 2:
                self.ranges[index] = new_ranges[0]
                self.ranges.append(new_ranges[1])
            else:
                last_data = self.ranges.pop()
                if len(self.ranges) > index:
                    self.ranges[index] = last_data

    def is_empty(self):
        return not self.ranges

    def get(self) -> int | None:
        if self.is_empty(): return None
        choice = random.randint(0, len(self.ranges) - 1)
        start, end = self.ranges[choice]
        select = random.randint(start, end)
        self._adjust_range(choice, select)
        return select

class MatrixGenerator(BaseGenerator):
    def generate(self, variables: dict[str, tuple[int, str]], output: Output, config: MatrixConfig) -> list[list[str]]:
        range_manager = RangeManager(config.num_range, config.value_limit, config.is_distinct)
        matrix = [[config.empty_value]*config.col_size for _ in range(config.row_size)]
        matrix_size = config.row_size * config.col_size
        item = [*range(matrix_size)]
        random.shuffle(item)
        select_count = item[0] if config.random_empty else matrix_size
        count = 0
        while item and count < select_count:
            kth = item.pop()
            row, col = kth//config.col_size, kth%config.col_size
            if config.is_graph and row == col: continue
            if range_manager.is_empty(): continue
            matrix[row][col] = range_manager.get()
            count += 1
        if config.is_symmetric:
            for i in range(config.row_size):
                for j in range(config.col_size):
                    matrix[i][j] = matrix[j][i]
        ret = []
        for row in matrix:
            convert = [TYPE_FUNCTION[config.num_type](item) for item in row]
            row_str = output.separator.join(map(str, convert))
            variables['_element'] = (row_str, 'str')
            ret.extend(line_generator.generate(variables, output, config))
        return ret

matrix_generator = MatrixGenerator()
