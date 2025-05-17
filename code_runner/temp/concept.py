import docker
import os

path = r"C:\Users\dev\PycharmProjects\FastAPIProject\code_runner\temp\seccomp-profile.json"
client = docker.from_env()

container = client.containers.run(
    image="python:3.11-slim",
    command="timeout 5s python3 -c 'import time; time.sleep(99999); print(111)'",
    detach=True,
    mem_limit='256m',
    network_disabled=True,
    tmpfs={"/tmp": ""},
    security_opt=["no-new-privileges", f"seccomp={path}"],
    pids_limit=4,
    stdout=True,
    stderr=True,
    cap_drop=["ALL"],
    # user="runner1",
    read_only=True,
    remove=False  # 끝나면 자동 삭제
)

result = container.wait()
logs = container.logs(stdout=True, stderr=True)
exit_code = result.get("StatusCode", -1)

if exit_code == 124:
    print("⏱ timeout에 의해 종료됨 (exit code 124)")
elif exit_code == 0:
    print("✅ 정상 종료됨")
else:
    print(f"❌ 비정상 종료됨, 코드: {exit_code}")

# 깔끔하게 치우기
container.remove()
