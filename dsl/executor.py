from input_generator.base_generator import BaseGenerator, BaseConfig
from input_generator.line_generator import line_generator, LineConfig
from input_generator.undirected_graph_generator import undirected_graph_generator, UndirectedGraphConfig

from parsing import create_variables
from expression import safe_eval_helper
from dataclasses import dataclass

CONFIG_CLASS_REGISTRY = {
    "line": LineConfig,
    "undirected_graph": UndirectedGraphConfig,
}

GENERATOR_INSTANCE_REGISTRY = {
    "line": line_generator,
    "undirected_graph": undirected_graph_generator,
}

@dataclass
class Output:
    sequence: list[str]
    separator: str = ' '
    end_line: str = '\n'

def resolve_generator_config(type_name: str, variables: dict, config: dict) -> tuple[BaseGenerator, BaseConfig]:
    try:
        cfg_class = CONFIG_CLASS_REGISTRY[type_name]
        gen = GENERATOR_INSTANCE_REGISTRY[type_name]
        return gen, cfg_class(variables, config)
    except KeyError:
        raise ValueError(f"지원하지 않는 타입: {type_name}")

# $v는 이전에 지정한 변수
# 입력포맷 : [ variable, line ]
# 입력포맷의 variable은 초기init
# line : { variable: [ var.. ], repeat: $v, format: { ... }, type: (str), block_repeat: $v }
# line.type은 graph나 line..
# var: { name: (str), type: (str), range: [int, int] }
# format: 뭐 이런저런 옵션들... 뭐 separator나 sequence..

def process(variable_format, lines):
    result = []
    variables = create_variables(variable_format)
    for i in lines:
        block_repeat = safe_eval_helper(variables, i, 'block_repeat', '1')
        config = i.get('config', {})
        line_type = i.get('type', 'line')
        for _ in range(block_repeat):
            formats = i.get('output', {})
            sequence = formats.get('sequence', [])  # formats에서 sequence는 variable에 지정한 변수를 사용 가능하다 하자
            separator = formats.get('separator', ' ')  # 그리고 세퍼레이터. 기본값은 스페이스
            end_line = formats.get('end_line', '\n')
            format = Output(sequence, separator, end_line)
            variable_format = i.get('variable', {})

            repeat_count = safe_eval_helper(variables, i, 'repeat', '1')
            current_line_data = []
            for _ in range(repeat_count):
                generator, config = resolve_generator_config(line_type, variables, config)
                variables |= create_variables(variable_format)
                print('gen', generator.generate(variables, sequence, config))
                current_line_data.extend(generator.generate(variables, format, config))
            for line_data in current_line_data:
                result.append(separator.join(map(str, line_data)))
            print(current_line_data)
            # print(result)
    return '\n'.join(result)

# print(process([
#         {'name': 'N', 'type': 'int', 'range': [[3, 3]]}
#     ], [
#     {
#         'variable': [
#             {'name': 'x', 'type': 'int', 'range': [[1, 5]]}
#         ],
#         'type': 'line',
#         'repeat': '$N',
#         'output': {
#             'sequence': ['$x']
#         }
#     }
# ]))
# print(process([], [
#     {
#         'variable': [
#             { 'name': 'n', 'type': 'int', 'range': [[10, 15]] },
#         ],
#         'output': { 'sequence': ['$n'] }
#     },
#     {
#         'type': 'undirected_graph',
#         'config': {
#             'node_count': '$n',
#             'is_cycle': False
#         },
#         'output': { 'sequence': ['$_s', '$_e'] }
#     }
# ]))
#
# print()
#
# print(process([], [
#     {
#         'variable': [
#             { 'name': 'n', 'type': 'int', 'range': [[2, 3], [8, 10]] },
#             { 'name': 'm', 'type': 'int', 'range': [['$n-1', '$n*($n-1)//2']] }
#         ],
#         'output': { 'sequence': ['$n', '$m'] }
#     },
#     {
#         'type': 'undirected_graph',
#         'config': {
#             'node_count': '$n',
#             'edge_count': '$m'
#         },
#         'output': { 'sequence': ['$_s', '$_e'] }
#     }
# ]))
# print(process([], [
#     {
#         'variable': [
#             { 'name': 'n', 'type': 'int', 'range': [[5, 10]] }
#         ],
#         'output':
#     }
# ]))