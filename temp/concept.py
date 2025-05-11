# $v는 이전에 지정한 변수
# 입력포맷 : [ variable, line ]
# 입력포맷의 variable은 초기init
# line : { variable: [ var.. ], repeat: $v, format: { ... }, type: (str), line_repeat: $v }
# line.type은 graph나 line..
# var: { name: (str), type: (str), range: [int, int] }
# format: 뭐 이런저런 옵션들... 뭐 separator나 sequence..

import random
import ast
import operator as op

operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,   # 소수까지 나오게
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}

def safe_eval(expr, variables=None):
    variables = variables or {}

    def _eval(node):
        if isinstance(node, ast.Constant):  # Python 3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            raise TypeError("숫자만 허용됨")
        elif isinstance(node, ast.Name):
            if node.id in variables:
                return variables[node.id][0]
            raise ValueError(f"정의되지 않은 변수: {node.id}")
        elif isinstance(node, ast.BinOp):
            return operators[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            return operators[type(node.op)](_eval(node.operand))
        else:
            raise TypeError(f"허용되지 않은 표현식: {type(node)}")

    parsed = ast.parse(expr, mode='eval')
    return _eval(parsed.body)

def create_variables(variable_format):
    variables = {}
    for variable_format in variable_format:
        name = variable_format['name']
        types = variable_format['type']  # 일단 int/char만
        start, end = map(int, variable_format['range'])  # 당연히 시작과 끝 모두 int
        variables[name] = (random.randint(start, end), types)
    return variables

def type_line_data_generator(variables, sequence):
    line_data = []
    TYPE_FUNCTION = {
        'int': lambda val: val,
        'char': lambda val: chr(val)
    }
    for seq in sequence:
        if seq[0] == '$':
            value, types = variables[seq[1:]]
            line_data.append(TYPE_FUNCTION[types](value))
        else:
            line_data.append(seq)
    return line_data

LINE_TYPE_FUNCTION = {
    'line': type_line_data_generator,
}

def process(variable_format, lines):
    result = []
    variables = create_variables(variable_format)
    for i in lines:
        line_repeat = safe_eval(i.get('line_repeat', '1').replace("$", ""), variables)
        for _ in range(line_repeat):
            formats = i.get('format', {})
            line_type = i.get('type', 'line')
            sequence = formats.get('sequence', [])  # formats에서 sequence는 variable에 지정한 변수를 사용 가능하다 하자
            separator = formats.get('separator', ' ')  # 그리고 세퍼레이터. 기본값은 스페이스
            type_function = LINE_TYPE_FUNCTION[line_type]
            variable_format = i.get('variable', {})

            repeat_count = safe_eval(i.get('repeat', '1').replace("$", ""), variables)
            current_line_data = []
            for _ in range(repeat_count):
                variables |= create_variables(variable_format)
                current_line_data.extend(type_function(variables, sequence))
            result.append(separator.join(map(str, current_line_data)))
    return result

print(process([
    { "name": "T", "type": "int", "range": [3, 3] }
], [
  {
    "variable": [{ "name": "n", "type": "int", "range": [1, 1] }],
    "format": { "sequence": ["$n"] }
  },
  {
    "variable": [{ "name": "a", "type": "char", "range": [97, 122] }],
    "repeat": "1",
    "line_repeat": "$T",
    "format": { "sequence": ["$a"], "separator": "" }
  }
]
))
