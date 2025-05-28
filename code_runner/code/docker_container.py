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
        self.pool = Queue()
        self.security_opt = ["no-new-privileges"]

        if platform.system() == "Linux":
            self.security_opt.append("apparmor=docker-execute-profile")

        for _ in range(self.MAX_CONTAINER):
            container = self.create_container()
            self.pool.put(Container(container))

    def create_container(self):
        container = client.containers.create(
            image="python:3.13",
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
            security_opt=self.security_opt,
            pids_limit=16,
            cap_drop=["ALL"],
            restart_policy={"Name": "unless-stopped"},
            cpu_count=1
        )
        container.start()
        return container

    def get_container(self):
        return self.pool.get()  # 블로킹: 없으면 알아서 기다림

docker_container_pool = DockerContainerPool()

# import docker
# import platform
# from threading import Lock
# from collections import deque
# import threading
#
# client = docker.from_env()
#
# class Container:
#     def __init__(self, container, docker_container):
#         self.container = container
#         self.is_running = False
#         self.docker_container = docker_container
#         self.lock = Lock()
#
#     def is_idle(self):
#         with self.lock:
#             if not self.is_running:
#                 self.is_running = True
#                 return True
#             return False
#
#     def release(self):
#         with self.lock:
#             self.is_running = False
#         self.docker_container.notify_idle()
#
# class DockerContainer:
#     MAX_CONTAINER = 5
#
#     def __init__(self):
#         self.security_opt = ["no-new-privileges"]
#         if platform.system() == "Linux":
#             # security_opt.append("seccomp=/home/sdpr/projects/code_runner/temp/seccomp-profile.json")
#             self.security_opt.append("apparmor=docker-execute-profile")
#
#         self.containers = deque(Container(self.create_container(), self) for _ in range(self.MAX_CONTAINER))
#         self.condition = threading.Condition()
#
#     def create_container(self):
#         container = client.containers.create(
#             image="python:3.13",
#             command="sleep infinity",
#             detach=True,
#             mem_limit='1024m',
#             memswap_limit='1024m',
#             oom_kill_disable=False,
#             network_disabled=True,
#             volumes={
#                 "security": {
#                     "bind": "/security",
#                     "mode": "ro"
#                 },
#                 "/home/sdpr/scripts": {
#                     "bind": "/script",
#                     "mode": "rw"
#                 }
#             },
#             security_opt=self.security_opt,
#             pids_limit=16,
#             cap_drop=["ALL"],
#             # user="runner1",
#             restart_policy={
#                 "Name": "unless-stopped"
#             },
#             cpu_count=1
#         )
#         container.start()
#         return container
#
#     def get_idle_container(self):
#         with self.condition:
#             while True:
#                 for container in self.containers:
#                     if container.is_idle():
#                         return container
#                 self.condition.wait()
#
#     def notify_idle(self):
#         with self.condition:
#             self.condition.notify()
#
# docker_container = DockerContainer()
