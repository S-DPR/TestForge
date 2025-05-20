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
    async with aiofiles.open(p, "w") as f:
        await f.write(content)
    return {
        "filepath": p
    }

def wrap_kwargs(fn, kwargs):
    return lambda: fn(**kwargs)

async def handle_request(fn, kwargs):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, wrap_kwargs(fn, kwargs))
    return result

async def consume_and_respond():
    try:
        consumer = get_consumer("request-listener", "file_create_tc_req")
        loop = asyncio.get_running_loop()

        while True:
            try:
                msg = await loop.run_in_executor(None, lambda: consumer.poll(1.0))
                print("msg", msg, flush=True)
                if msg is None or msg.error():
                    continue

                key = msg.key().decode()
                value = json.loads(msg.value().decode())
                result = await save_file(**value)
                print("res", result, flush=True)
                send_message("file_create_tc_res", key=key, value=json.dumps(result))

            except Exception as inner_e:
                print(f"[consume loop 에러] {inner_e}", flush=True)

    except Exception as e:
        print(f"[consume_and_respond 전체 실패] {e}", flush=True)