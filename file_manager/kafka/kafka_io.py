import uvicorn
from kafka_common.kafka_producer import send_message
from kafka_common.kafka_consumer import get_consumer
import asyncio
import aiofiles
import json
import uuid

async def save_file(folder: str, content: str, ext: str = ".txt") -> dict[str, str]:
    filename = str(uuid.uuid4())
    p = f"{folder}/{filename}.{ext}"
    with aiofiles.open(p, "w") as f:
        f.write(content)
    return {
        "filepath": p
    }

def wrap_kwargs(fn, kwargs):
    return lambda: fn(**kwargs)

async def handle_request(fn, kwargs):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, wrap_kwargs(fn, kwargs))
    return result

def consume_and_respond():
    consumer = get_consumer("request-listener", "file_create_tc_req")
    while True:
        msg = consumer.poll(1.0)
        if msg and not msg.error():
            key = msg.key().decode()
            value = json.loads(msg.value().decode())
            result = save_file(**value)
            send_message("file_create_tc_res", key=key, value=json.dumps(result))

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8001) #

