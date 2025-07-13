from dacite import from_dict

from error.exception import ConfigValueError, VariableNotFoundError, BlockExecutionError
from request.config_structs import TestcaseConfig, LineConfigDataclass, GraphConfigDataclass, \
    MatrixConfigDataclass, QueryConfigDataclass, TestcaseBlockConfig, Output, Variable, Range
from input_generator.base_generator import BaseGenerator, BaseConfig
from input_generator.line_generator import line_generator, LineConfig
from input_generator.matrix_generator import matrix_generator, MatrixConfig
from input_generator.query_generator import query_generator, QueryConfig
from input_generator.graph_generator import graph_generator, GraphConfig

from request.parsing import create_variables
from request.expression import safe_eval

from db.sessions import get_db

CONFIG_CLASS_REGISTRY = {
    "line": LineConfig,
    "graph": GraphConfig,
    "matrix": MatrixConfig,
    "query": QueryConfig,
}

CONFIG_DATACLASS_REGISTRY = {
    'line': LineConfigDataclass,
    'graph': GraphConfigDataclass,
    'matrix': MatrixConfigDataclass,
    'query': QueryConfigDataclass
}

GENERATOR_INSTANCE_REGISTRY = {
    "line": line_generator,
    "graph": graph_generator,
    'matrix': matrix_generator,
    "query": query_generator,
}

def resolve_generator_config(type_name: str, variables: dict, config: dict) -> tuple[BaseGenerator, BaseConfig]:
    try:
        cfg_class = CONFIG_CLASS_REGISTRY[type_name]
        data_cfg_class = CONFIG_DATACLASS_REGISTRY[type_name]
        gen = GENERATOR_INSTANCE_REGISTRY[type_name]
        from dacite import Config
        return gen, cfg_class(variables, from_dict(data_class=data_cfg_class, data=config, config=Config(strict=False)))
    except KeyError:
        raise ValueError(f"지원하지 않는 타입: {type_name}")

# $v는 이전에 지정한 변수
# 입력포맷 : [ variable, line ]
# 입력포맷의 variable은 초기init
# line : { variable: [ var.. ], repeat: $v, format: { ... }, type: (str) }
# line.type은 graph나 line..
# var: { name: (str), type: (str), range: [int, int] }
# format: 뭐 이런저런 옵션들... 뭐 separator나 sequence..

def process(account_id, testcaseConfig: TestcaseConfig):
    variable_format, lines = testcaseConfig.variable_format, testcaseConfig.lines
    result = []
    variables = create_variables({}, variable_format)
    for idx, line in enumerate(lines, 1):
        config = line.config
        line_type = line.type

        # output = create_outputs(i.get('output', {}))
        output = line.output
        variable_format = line.variable

        repeat_count = safe_eval(line.repeat.replace('$', ''), variables)
        variables['_repeat'] = repeat_count
        current_line_data = []
        generator, gen_config = resolve_generator_config(line_type, variables, config)
        try:
            for _ in range(repeat_count):
                variables |= create_variables(variables, variable_format)
                current_line_data.extend(generator.generate(variables, output, gen_config))
        except ConfigValueError as e:
            raise BlockExecutionError(idx, e)
        except VariableNotFoundError as e:
            raise BlockExecutionError(idx, e)
        for line_data in current_line_data:
            result.append(output.separator.join(map(str, line_data)))
    # save_database(account_id, "", testcaseConfig)
    return '\n'.join(result)


from db.tcgen.schema import TcGenCreate
from db.tcgen_block.schema import TcGenBlockCreate
from db.tcgen_file.schema import TcGenFileCreate
from db.tcgen import service as tcgen_service
from db.tcgen_file import service as file_service
from db.tcgen_block import service as block_service
from dataclasses import asdict


def save_database(account_id, testcase_file_path, testcaseConfig: TestcaseConfig):
    tcgen_create = TcGenCreate(
        account_id=account_id,
    )
    with get_db() as db:
        tcgen = tcgen_service.create_tcgen(db, tcgen_create)

    variable_format, lines = testcaseConfig.variable_format, testcaseConfig.lines
    tcgen_prv_variable_block_create = TcGenBlockCreate(
        tcgen_id = tcgen.tcgen_id,
        type = "prv_variable_block",
        config = {},
        variable = variable_format,
        output = {},
        repeat = "",
        sequence = 0
    )
    with get_db() as db:
        block_service.create_tcgen_block(db, tcgen_prv_variable_block_create)
    for idx, block in enumerate(lines, 1):
        variable_as_json = [asdict(var) for var in block.variable]
        tcgen_prv_variable_block_create = TcGenBlockCreate(
            tcgen_id=tcgen.tcgen_id,
            type=block.type,
            config=block.config,
            variable=variable_as_json,
            output=asdict(block.output),
            repeat=block.repeat,
            sequence=idx
        )
        with get_db() as db:
            block_service.create_tcgen_block(db, tcgen_prv_variable_block_create)

    tcgen_file_create = TcGenFileCreate(
        tcgen_id = tcgen.tcgen_id,
        filepath = testcase_file_path,
    )
    with get_db() as db:
        file_service.create_tcgen_file(db, tcgen_file_create)

# from request.config_structs import TestcaseConfig
# from input_generator.base_generator import BaseGenerator, BaseConfig
# from input_generator.line_generator import line_generator, LineConfig
# from input_generator.matrix_generator import matrix_generator, MatrixConfig
# from input_generator.query_generator import query_generator, QueryConfig
# from input_generator.graph_generator import graph_generator, UndirectedGraphConfig
#
# from request.parsing import create_variables
# from request.expression import safe_eval
#
# from input-generator-service.db.sessions import get_db
#
# CONFIG_CLASS_REGISTRY = {
#     "line": LineConfig,
#     "graph": UndirectedGraphConfig,
#     "matrix": MatrixConfig,
#     "query": QueryConfig,
# }
#
# GENERATOR_INSTANCE_REGISTRY = {
#     "line": line_generator,
#     "graph": graph_generator,
#     'matrix': matrix_generator,
#     "query": query_generator,
# }
#
# def resolve_generator_config(type_name: str, variables: dict, config: dict) -> tuple[BaseGenerator, BaseConfig]:
#     try:
#         cfg_class = CONFIG_CLASS_REGISTRY[type_name]
#         gen = GENERATOR_INSTANCE_REGISTRY[type_name]
#         return gen, cfg_class(variables, config)
#     except KeyError:
#         raise ValueError(f"지원하지 않는 타입: {type_name}")
#
# # $v는 이전에 지정한 변수
# # 입력포맷 : [ variable, line ]
# # 입력포맷의 variable은 초기init
# # line : { variable: [ var.. ], repeat: $v, format: { ... }, type: (str) }
# # line.type은 graph나 line..
# # var: { name: (str), type: (str), range: [int, int] }
# # format: 뭐 이런저런 옵션들... 뭐 separator나 sequence..
#
# def process(account_id, testcaseConfig: TestcaseConfig):
#     variable_format, lines = testcaseConfig.variable_format, testcaseConfig.lines
#     result = []
#     variables = create_variables({}, variable_format)
#     for line in lines:
#         config = line.config
#         line_type = line.type
#
#         # output = create_outputs(i.get('output', {}))
#         output = line.output
#         variable_format = line.variable
#
#         repeat_count = safe_eval(line.repeat, variables)
#         variables['_repeat'] = repeat_count
#         current_line_data = []
#         generator, gen_config = resolve_generator_config(line_type, variables, config)
#         for _ in range(repeat_count):
#             variables |= create_variables(variables, variable_format)
#             current_line_data.extend(generator.generate(variables, output, gen_config))
#         for line_data in current_line_data:
#             result.append(output.separator.join(map(str, line_data)))
#     save_database(account_id, "", testcaseConfig)
#     return '\n'.join(result)
#
#
# from db.tcgen.schema import TcGenCreate
# from db.tcgen_block.schema import TcGenBlockCreate
# from db.tcgen_file.schema import TcGenFileCreate
# from db.tcgen import service as tcgen_service
# from db.tcgen_file import service as file_service
# from db.tcgen_block import service as block_service
# from db.sessions import SessionLocal
# from dataclasses import asdict
#
#
# def save_database(account_id, testcase_file_path, testcaseConfig: TestcaseConfig):
#     tcgen_create = TcGenCreate(
#         account_id=account_id,
#     )
#     with get_db() as db:
#         tcgen = tcgen_service.create_tcgen(db, tcgen_create)
#
#     variable_format, lines = testcaseConfig.variable_format, testcaseConfig.lines
#     tcgen_prv_variable_block_create = TcGenBlockCreate(
#         tcgen_id = tcgen.tcgen_id,
#         type = "prv_variable_block",
#         config = {},
#         variable = variable_format,
#         output = {},
#         repeat = "",
#         sequence = 0
#     )
#     with get_db() as db:
#         block_service.create_tcgen_block(db, tcgen_prv_variable_block_create)
#     for idx, block in enumerate(lines, 1):
#         variable_as_json = [asdict(var) for var in block.variable]
#         tcgen_prv_variable_block_create = TcGenBlockCreate(
#             tcgen_id=tcgen.tcgen_id,
#             type=block.type,
#             config=block.config,
#             variable=variable_as_json,
#             output=asdict(block.output),
#             repeat=block.repeat,
#             sequence=idx
#         )
#         with get_db() as db:
#             block_service.create_tcgen_block(db, tcgen_prv_variable_block_create)
#
#     tcgen_file_create = TcGenFileCreate(
#         tcgen_id = tcgen.tcgen_id,
#         filepath = testcase_file_path,
#     )
#     with get_db() as db:
#         file_service.create_tcgen_file(db, tcgen_file_create)
#
#
# # print(process([
# #         {'name': 'N', 'type': 'int', 'range': [[3, 3]]}
# #     ], [
# #     {
# #         'variable': [
# #             {'name': 'x', 'type': 'int', 'range': [[1, 5]]}
# #         ],
# #         'type': 'line',
# #         'repeat': '$N',
# #         'output': {
# #             'sequence': ['$x']
# #         }
# #     }
# # ]))
# # print(process([], [
# #     {
# #         'variable': [
# #             { 'name': 'n', 'type': 'int', 'range': [[10, 15]] },
# #         ],
# #         'output': { 'sequence': ['$n'] }
# #     },
# #     {
# #         'type': 'graph',
# #         'config': {
# #             'node_count': '$n',
# #             'is_cycle': False
# #         },
# #         'output': { 'sequence': ['$_s', '$_e'] }
# #     }
# # ]))
# #
# # print()
# #
# # print(process([], [
# #     {
# #         'variable': [
# #             { 'name': 'n', 'type': 'int', 'range': [[2, 3], [8, 10]] },
# #             { 'name': 'm', 'type': 'int', 'range': [['$n-1', '$n*($n-1)//2']] }
# #         ],
# #         'output': { 'sequence': ['$n', '$m'] }
# #     },
# #     {
# #         'type': 'graph',
# #         'config': {
# #             'node_count': '$n',
# #             'edge_count': '$m',
# #             'weight_range': [1, 1000]
# #         },
# #         'output': { 'sequence': ['$_s', '$_e', '$_w'] }
# #     }
# # ]))
# # print(process([], [
# #     {
# #         'variable': [
# #             { 'name': 'n', 'type': 'int', 'range': [[5, 10]] }
# #         ],
# #         'type': 'matrix',
# #         'output': {
# #             'sequence': ['$_element'],
# #             'separator': ',',
# #         },
# #         'config': {
# #             'num_type': 'int',
# #             'col_size': '$n',
# #             'row_size': '$n',
# #             'is_distinct': True,
# #             'empty_value': 90,
# #             'num_range': [[1, 10], [1, 30], [5, 48]]
# #         }
# #     }
# # ]))
#
# # print(process([], [
# #     {
# #         'variable': [
# #             {'name': 'n', 'type': 'int', 'range': [[1, 10]]},
# #             {'name': 'q', 'type': 'int', 'range': [[1, 10]]},
# #         ],
# #         'output': {
# #             'sequence': ['$n', '$q']
# #         }
# #     },
# #     {
# #         'type': 'query',
# #         'variable': [
# #             { 'name': 'x', 'type': 'int', 'range': [[1, '$n']] },
# #             { 'name': 'l', 'type': 'int', 'range': [[1, '$n']] },
# #             { 'name': 'r', 'type': 'int', 'range': [['$l', '$n']] }
# #         ],
# #         'config': {
# #             'outputs': [
# #                 {
# #                     'sequence': ['1', '$x']
# #                 },
# #                 {
# #                     'sequence': ['2', '$l', '$r']
# #                 }
# #             ],
# #             'distribution': [10, 10],
# #             'min_count': [1, 1],
# #             'max_count': [1000000, 1000000],
# #         },
# #         'repeat': '$q'
# #     }
# # ]))
#
# # print(process([], [
# #     {
# #         'variable': [
# #             { 'name': 'n', 'type': 'enum', 'range': [['a', 'b', 'c']] }
# #         ],
# #         'type': 'line',
# #         'output': {
# #             'sequence': ['$n']
# #         }
# #     }
# # ]))
#
#
# print(process('a', TestcaseConfig([], [
#     TestcaseBlockConfig(
#         output=Output(['nn', '$n', '$m']),
#         repeat='1',
#         type='line',
#         variable=[
#             Variable('n', [Range(1, 5)]),
#             Variable('m', [Range(5, 10)]),
#         ],
#         config={}
#     ),
#     TestcaseBlockConfig(
#         output=Output(['$_s', '$_e']),
#         repeat='1',
#         type='graph',
#         variable=[],
#         config={
#             'node_count': '$n'
#         }
#     )
# ])))

# print(process('a', TestcaseConfig([], [
#     TestcaseBlockConfig(
#         output=Output(['nn', '$n', '$m']),
#         repeat='1',
#         type='line',
#         variable=[
#             Variable('n', [Range('3', '5')]),
#             Variable('m', [Range('5', '10')]),
#         ],
#         config={}
#     ),
#     TestcaseBlockConfig(
#         output=Output([]),
#         repeat='$n',
#         type='query',
#         variable=[
#             Variable('x', [Range('1', '$n')]),
#             Variable('l', [Range('1', '$n')]),
#             Variable('r', [Range('$l', '$n')])
#         ],
#         config={
#             'outputs': [
#                 {
#                     'sequence': ['1', '$x']
#                 },
#                 {
#                     'sequence': ['2', '$l', '$r']
#                 }
#             ],
#             'distribution': ['10', '10'],
#             'min_count': ['1', '1'],
#             'max_count': ['1000000', '1000000'],
#         }
#     )
# ])))

# print(process('a', TestcaseConfig([], [
#     TestcaseBlockConfig(
#         output=Output(['nn', '$n', '$m']),
#         repeat='1',
#         type='line',
#         variable=[
#             Variable('n', [Range('3', '5')]),
#             Variable('m', [Range('5', '10')]),
#         ],
#         config={}
#     ),
#     TestcaseBlockConfig(
#         output=Output(['$_element']),
#         repeat='$n',
#         type='matrix',
#         variable=[
#             Variable('x', [Range('1', '$n')]),
#             Variable('l', [Range('1', '$n')]),
#             Variable('r', [Range('$l', '$n')])
#         ],
#         config={
#             'col_size': '$n',
#             'row_size': '$n',
#             'is_distinct': True,
#             'empty_value': '-1',
#             'num_range': [Range('1', '10'), Range('1', '30'), Range('5', '48')]
#         }
#     )
# ])))