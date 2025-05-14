import random
from expression import safe_eval_helper

def create_variables(variable_format):
    variables = {}
    for variable_format in variable_format:
        name = variable_format['name']
        types = variable_format['type']  # 일단 int/char만
        start_expression, end_expression = variable_format['range']
        variable_format['start'] = str(start_expression)
        variable_format['end'] = str(end_expression)
        start = safe_eval_helper(variables, variable_format, 'start', None)
        end = safe_eval_helper(variables, variable_format, 'end', None)
        variables[name] = (random.randint(start, end), types)
    return variables
