import docker
import platform
from queue import Queue
from threading import Thread

client = docker.from_env()

class Container:
    def __init__(self, container):
        self.container = container

    def release(self):
        docker_container_pool.pool.put(self)  # 다시 풀에 반납

class DockerContainerPool:
    MAX_CONTAINER = 10

    def __init__(self):
        for c in client.containers.list(all=True, filters={"label": "purpose=code-execution"}):
            c.remove(force=True)
        self.pool = Queue()
        self.security_opt = ["no-new-privileges"]

        if platform.system() == "Linux":
            self.security_opt.append("apparmor=docker-execute-profile")

        for _ in range(self.MAX_CONTAINER):
            container = self.create_container()
            self.pool.put(Container(container))

    def create_container(self):
        container = client.containers.create(
            image="my/executor:latest",
            command="sleep infinity",
            detach=True,
            mem_limit='1024m',
            memswap_limit='1024m',
            oom_kill_disable=False,
            network_disabled=True,
            volumes={
                "security": {
                    "bind": "/security",
                    "mode": "ro"
                },
                "/home/sdpr/scripts": {
                    "bind": "/script",
                    "mode": "rw"
                }
            },
            labels={
                "purpose": "code-execution",
            },
            security_opt=self.security_opt,
            pids_limit=128,
            cap_drop=["ALL"],
            restart_policy={"Name": "unless-stopped"},
            cpu_count=1
        )
        container.start()
        return container

    def get_container(self):
        return self.pool.get()

    def cleanup(self):
        for container in self.pool.queue:
            container.container.stop(timeout=1)
            container.container.remove(force=True)

docker_container_pool = DockerContainerPool()
