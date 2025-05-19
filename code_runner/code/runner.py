from code import Code
from docker_container import docker_container

def runner(code: Code, time_limit: int):
    container = docker_container.get_idle_container()
    exit_code, output = container.container.exec_run(
        cmd=['timeout', f'{time_limit}s', 'python3', f'{code.filename}'],
        demux=False
    )

    if exit_code == 124:
        print("⏱ timeout에 의해 종료됨 (exit code 124)")
    elif exit_code == 0:
        print("✅ 정상 종료됨")
    else:
        print(f"❌ 비정상 종료됨, 코드: {exit_code}")
    print(output.decode())

    container.release() #
