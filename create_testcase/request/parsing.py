import random

from request.config_structs import Variable, Output
from request.expression import safe_eval


def create_variables(variables: dict[str, tuple[int, str]], variable_format: list[Variable]):
    for variable in variable_format:
        # name = variable_format['name']
        # types = variable_format['type']  # 일단 int/char만
        # ranges = variable_format['range'] # range는 list[(s, e)]
        name, range_, type_ = variable.name, variable.range, variable.type
        if type_ in ['int', 'char']:
            start_expression, end_expression = random.choice(range_)
            # variable_format['start'] = str(start_expression)
            # variable_format['end'] = str(end_expression)
            start = safe_eval(str(start_expression), variables)
            end = safe_eval(str(end_expression), variables)
            if start > end:
                raise ValueError(f'start cannot be greater than end : {start_expression} : {start}, {end_expression} : {end}')
            variables[name] = (random.randint(start, end), type_)
        elif type_ in ['enum']:
            select = random.choice(random.choice(range_))
            variables[name] = (select, 'str')
    return variables

def create_outputs(output_dict):
    sequence = output_dict.get('sequence', [])  # formats에서 sequence는 variable에 지정한 변수를 사용 가능하다 하자
    separator = output_dict.get('separator', ' ')  # 그리고 세퍼레이터. 기본값은 스페이스
    end_line = output_dict.get('end_line', '\n')
    return Output(sequence, separator, end_line)
