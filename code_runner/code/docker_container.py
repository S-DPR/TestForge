import docker
import platform
from threading import Lock
from collections import deque
import threading

client = docker.from_env()

class Container:
    def __init__(self, container, docker_container):
        self.container = container
        self.is_running = False
        self.docker_container = docker_container
        self.lock = Lock()

    def is_idle(self):
        with self.lock:
            if not self.is_running:
                self.is_running = True
                return True
            return False

    def release(self):
        with self.lock:
            self.is_running = False
        self.docker_container.notify_idle()

class DockerContainer:
    MAX_CONTAINER = 5

    def __init__(self):
        self.security_opt = ["no-new-privileges"]
        if platform.system() == "Linux":
            # security_opt.append("seccomp=/home/sdpr/projects/code_runner/temp/seccomp-profile.json")
            self.security_opt.append("apparmor=docker-execute-profile")

        self.containers = deque(Container(self.create_container(), self) for _ in range(self.MAX_CONTAINER))
        self.condition = threading.Condition()

    def create_container(self):
        return client.containers.create(
            image="python:3.13",
            command="sleep infinity",
            detach=True,
            mem_limit='1024m',
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
            security_opt=self.security_opt,
            pids_limit=16,
            cap_drop=["ALL"],
            # user="runner1",
            restart_policy={
                "Name": "unless-stopped"
            },
            cpu_count=1
        )

    def get_idle_container(self):
        with self.condition:
            while True:
                for container in self.containers:
                    if container.is_idle():
                        return container
                self.condition.wait()

    def notify_idle(self):
        with self.condition:
            self.condition.notify()

docker_container = DockerContainer()
