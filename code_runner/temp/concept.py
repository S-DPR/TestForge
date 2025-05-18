import docker
import platform
import time

security_opt = ["no-new-privileges"]
if platform.system() == "Linux":
    security_opt.append("seccomp=/home/sdpr/projects/code_runner/temp/seccomp-profile.json")
    security_opt.append("apparmor=docker-execute-profile")

print(security_opt)

client = docker.from_env()
container = client.containers.create(
    image="python:3.11-slim",
    command="sleep infinity",
    detach=True,
    mem_limit='1024m',
    network_disabled=True,
    volumes={
        "security": {
            "bind": "/security",
            "mode": "ro"
        },
        "script": {
            "bind": "/script",
            "mode": "rw"
        }
    },
    security_opt=security_opt,
    pids_limit=16,
    cap_drop=["ALL"],
    # user="runner1",
)
container.start()

for _ in range(10):
    c = client.containers.get(container.id)
    if c.status == "running":
        break
    time.sleep(0.5)

code = "print(\"hihidsfsdfsdhi\")"
escaped = repr(code)
exit_code, output = container.exec_run(
    cmd=["python3", "-c", f"with open('/script/run.py', 'w') as f: f.write({escaped})"],
    demux=False
)

command = f"timeout 5s python3 /script/test.py"
exit_code, output = container.exec_run(
    cmd=["sh", "-c", "timeout 5s python3 /script/run.py > /script/output.txt"],
    demux=False
)


if exit_code == 124:
    print("⏱ timeout에 의해 종료됨 (exit code 124)")
elif exit_code == 0:
    print("✅ 정상 종료됨")
else:
    print(f"❌ 비정상 종료됨, 코드: {exit_code}")

# 깔끔하게 치우기
container.kill()
container.remove()
#
