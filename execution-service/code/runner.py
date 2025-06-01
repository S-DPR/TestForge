from code.code import Code
from code.docker_container import docker_container_pool

def runner(code: Code, input_filepath, output_filepath, time_limit: int):
    container = docker_container_pool.get_container()
    try:
        exit_code, output = container.container.exec_run(
            cmd=f"bash -c 'timeout {time_limit}s python3 {code.filepath} < {input_filepath} > {output_filepath}'",
            demux=False
        )
        return exit_code
    finally:
        container.release()

# import sys
# from code.code import Code
# from code.docker_container import docker_container
# import uuid
#
# def runner(code: Code, input_filepath, output_filepath, time_limit: int):
#     container = docker_container.get_idle_container()
#     try:
#         exit_code, output = container.container.exec_run(
#             # cmd=['timeout', f'{time_limit}s', 'python3', f'{code.filepath} < {input_filepath} > {output_filepath}'],
#             cmd=f"bash -c 'timeout {time_limit}s python3 {code.filepath} < {input_filepath} > {output_filepath}'",
#             demux=False
#         )
#         return exit_code
#     finally:
#         container.release()
