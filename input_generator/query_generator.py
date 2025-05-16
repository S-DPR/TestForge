import random

from request.config_structs import Output
from request.expression import safe_eval_helper
from request.parsing import create_outputs
from error.exception import ConfigValueError
from input_generator.base_generator import BaseGenerator, BaseConfig
from input_generator.line_generator import line_generator


class QueryConfig(BaseConfig):
    def __init__(self, variables: dict[str, tuple[int, str]], config: dict[str, str]):
        self.outputs = config.get("outputs", None)
        self.distribution = config.get("distribution", [])
        self.min_count = config.get("min_count", [])
        self.max_count = config.get("max_count", [])
        self.repeat = variables.get("_repeat", 1)

        self.outputs = [create_outputs(i) for i in self.outputs]
        while len(self.distribution) < len(self.outputs):
            self.distribution.append(1)
        while len(self.min_count) < len(self.outputs):
            self.min_count.append(0)
        while len(self.max_count) < len(self.outputs):
            self.max_count.append(1<<60)
        self.distribution = [safe_eval_helper(variables, variables, i, None) if type(i) == str else i for i in self.distribution]
        self.min_count = [safe_eval_helper(variables, variables, i, None) if type(i) == str else i for i in self.min_count]
        self.max_count = [safe_eval_helper(variables, variables, i, None) if type(i) == str else i for i in self.max_count]

        self.count = [0]*len(self.outputs)
        self.validate()

    def validate(self):
        eq_len = any(len(self.outputs) == len(i) for i in [self.distribution, self.min_count, self.max_count])
        if not eq_len:
            raise ConfigValueError('ALL', f'config로 들어온 배열들의 길이가 같지 않습니다. outputs: {len(self.outputs)}, distribution: {self.distribution}, min_count: {self.min_count}, max_count: {self.max_count}')
        if self.repeat > 1_000_000:
            raise ConfigValueError('repeat', f'{self.repeat}은 100만을 넘을 수 엇습니다. repeat: {self.repeat}')
        if len(self.outputs) > 100:
            raise ConfigValueError('outputs', f'outputs는 길이 100을 넘을 수 없습니다. outputs length: {len(self.outputs)}')
        if sum(self.min_count) > self.repeat:
            raise ConfigValueError('min_count', f'min_count의 합이 {self.repeat}보다 큽니다. 현재: {sum(self.min_count)}')
        if sum(self.max_count) < self.repeat:
            raise ConfigValueError('max_count', f'max_count의 합이 {self.repeat}보다 작습니다. 현재: {sum(self.max_count)}')
        if any(i < 0 for i in self.distribution):
            raise ConfigValueError('distribution', f'distribution 내부 값은 음수일 수 없습니다.')
        if any(mn > mx for mn, mx in zip(self.min_count, self.max_count)):
            raise ConfigValueError('min_count, max_count', f'min_count의 값이 max_count보다 큰 부분이 존재합니다. min_count: {self.min_count}, max_count: {self.max_count}')

class QueryGenerator(BaseGenerator):
    def generate(self, variables: dict[str, tuple[int, str]], output: Output, config: QueryConfig) -> list[list[str]]:
        ret = []
        ln = len(config.outputs)
        count = config.count
        left_turn = config.repeat-sum(count)
        need_turn = sum(max(mn-cur, 0) for cur, mn in zip(count, config.min_count))
        option = []
        weight = []
        compare_list = config.min_count if left_turn == need_turn else config.max_count
        for i in range(ln):
            if compare_list[i] > count[i]:
                option.append(i)
                weight.append(config.distribution[i])
        select = random.choices(option, weights=weight, k=1)[0]
        config.count[select] += 1
        line = line_generator.generate(variables, config.outputs[select], config)
        ret.append([config.outputs[select].separator.join(line[0])])
        return ret

query_generator = QueryGenerator()
