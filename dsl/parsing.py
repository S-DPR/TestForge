import random
from dataclasses import dataclass

from expression import safe_eval_helper

@dataclass
class Output:
    sequence: list[str]
    separator: str = ' '
    end_line: str = '\n'

def create_variables(variables, variable_format):
    for variable_format in variable_format:
        name = variable_format['name']
        types = variable_format['type']  # 일단 int/char만
        ranges = variable_format['range'] # range는 list[(s, e)]
        if types in ['int', 'char']:
            start_expression, end_expression = random.choice(ranges)
            variable_format['start'] = str(start_expression)
            variable_format['end'] = str(end_expression)
            start = safe_eval_helper(variables, variable_format, 'start', None)
            end = safe_eval_helper(variables, variable_format, 'end', None)
            if start > end:
                raise ValueError(f'start cannot be greater than end : {start_expression} : {start}, {end_expression} : {end}')
            variables[name] = (random.randint(start, end), types)
        elif types in ['enum']:
            select = random.choice(random.choice(ranges))
            variables[name] = (select, 'str')
    return variables

def create_outputs(output_dict):
    sequence = output_dict.get('sequence', [])  # formats에서 sequence는 variable에 지정한 변수를 사용 가능하다 하자
    separator = output_dict.get('separator', ' ')  # 그리고 세퍼레이터. 기본값은 스페이스
    end_line = output_dict.get('end_line', '\n')
    return Output(sequence, separator, end_line)
