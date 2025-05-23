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
    print("exit code:", exit_code, flush=True)
    print("output:", output, flush=True)

    container.release() #
    return exit_code
    # if exit_code == 124:
    #     return "⏱ timeout에 의해 종료됨 (exit code 124)"
    # elif exit_code == 0:
        # return exit
    # else:
    #     return f"❌ 비정상 종료됨, 코드: {exit_code}"
