import asyncio
import uuid
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
import threading

from file_manager.kafka.kafka_io import consume_and_respond

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔥 여기가 startup
    print("FastAPI startup - 워커 실행")

    # 워커 스레드 실행
    task = asyncio.create_task(consume_and_respond())

    yield  # ← 여기까지가 "앱 살아있는 동안"

    # 🔥 여기가 shutdown
    print("FastAPI shutdown - 워커 정리 필요하면 여기서")
    task.cancel()

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8001) #
