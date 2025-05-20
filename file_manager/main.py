import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI
import threading

from file_manager.kafka.kafka_io import consume_and_respond

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔥 여기가 startup
    print("FastAPI startup - 워커 실행")

    # 워커 스레드 실행
    thread = threading.Thread(target=consume_and_respond, daemon=True)
    thread.start()

    yield  # ← 여기까지가 "앱 살아있는 동안"

    # 🔥 여기가 shutdown
    print("FastAPI shutdown - 워커 정리 필요하면 여기서")

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


