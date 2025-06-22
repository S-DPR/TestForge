import random

from request.config_structs import Variable, Output
from request.expression import safe_eval


def create_variables(variables: dict[str, tuple[int, str]], variable_format: list[Variable]):
    for variable in variable_format:
        name, range_, type_ = variable.name, variable.range, variable.type
        if type_ in ['int', 'char']:
            select_range = random.choice(range_)
            start_expression = select_range.min
            end_expression = select_range.max
            start = safe_eval(str(start_expression).replace("$", ""), variables)
            end = safe_eval(str(end_expression).replace("$", ""), variables)
            if start > end:
                raise ValueError(f'start cannot be greater than end : {start_expression} : {start}, {end_expression} : {end}')
            variables[name] = (random.randint(start, end), type_)
        elif type_ in ['enum']:
            options = []
            for inner_range in range_:
                inner_option = []
                for i in inner_range:
                    if i[0] == '$':
                        inner_option.append(safe_eval(i.replace('$', ''), variables))
                        continue
                    inner_option.append(i)
                options.append(inner_option)
            select = random.choice(random.choice(options))
            variables[name] = (select, 'str')
    return variables

def create_outputs(output_dict):
    sequence = output_dict.get('sequence', [])  # formats에서 sequence는 variable에 지정한 변수를 사용 가능하다 하자
    separator = output_dict.get('separator', ' ')  # 그리고 세퍼레이터. 기본값은 스페이스
    end_line = output_dict.get('end_line', '\n')
    return Output(sequence, separator, end_line)
