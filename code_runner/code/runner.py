import sys
from code.code import Code
from code.docker_container import docker_container
import uuid

def runner(code: Code, input_filepath, output_filepath, time_limit: int):
    container = docker_container.get_idle_container()
    exit_code, output = container.container.exec_run(
        # cmd=['timeout', f'{time_limit}s', 'python3', f'{code.filepath} < {input_filepath} > {output_filepath}'],
        cmd=f"bash -c 'timeout {time_limit}s python3 {code.filepath} < {input_filepath} > {output_filepath}'",
        demux=False
    )

    container.release()
    return exit_code
