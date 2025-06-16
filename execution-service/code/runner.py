import uuid

from code.code import Code
from code.docker_container import docker_container_pool

def compile(container, code: Code, input_filepath: str):
    language = code.language
    uniq = str(uuid.uuid4())
    if language == 'python':
        return 0, input_filepath
    if language == 'java':
        return 0, input_filepath
    if language == 'cpp':
        exit_code, output = container.container.exec_run(
            cmd=f"bash -c 'g++ {code.filepath} -o {uniq}'",
            demux=False
        )
        return exit_code, uniq

def runner(code: Code, input_filepath, output_filepath, time_limit: int):
    container = docker_container_pool.get_container()
    try:
        exit_code, compiled_path = compile(container, code, input_filepath)

        language = code.language
        if language == 'python':
            run_cmd = f"timeout {time_limit}s python3 {compiled_path}"

        elif language == 'java':
            run_cmd = f"timeout {time_limit}s java {compiled_path}"

        elif language == 'cpp':
            run_cmd = f"timeout {time_limit}s {compiled_path}"

        else:
            raise ValueError(f"Unsupported language: {language}")

        exit_code, output = container.container.exec_run(
            cmd=f"bash -c '{run_cmd} < {input_filepath} > {output_filepath}'",
            demux=False
        )
        return exit_code
    finally:
        container.release()
