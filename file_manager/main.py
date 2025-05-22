import asyncio
import uuid
from contextlib import asynccontextmanager
from kafka_common.kafka_topic import create_topic

import uvicorn
from fastapi import FastAPI
import threading

from kafka.kafka_io import consume_and_respond

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔥 여기가 startup
    print("FastAPI startup - 워커 실행")

    # 워커 스레드 실행
    create_topic("file_create_tc_res")
    create_topic("file_create_tc_req")
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
    print("egrsrrghfdjkrfegnfcireojxgjixrfexjkgcfnftest", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=8001) #