from kafka_common.kafka_producer import send_message
from kafka_common.kafka_consumer import get_consumer
from kafka_common.kafka_topic import create_topic
import asyncio
import json
import uuid

def send_request(folder: str, content: str, ext: str = ".txt"):
    correlation_id = str(uuid.uuid4())
    args = { "folder": folder, "content": repr(content), "ext": ext }
    consumer = get_consumer("response-listener", "file_create_tc_res")
    send_message("file_create_tc_req", key=correlation_id, value=json.dumps(args))
    return correlation_id, consumer

def listen_for_response(topic: list[str], correlation_id: str):
    consumer = get_consumer("response-listener", topic)
    while True:
        msg = consumer.poll(1.0)
        print(msg, flush=True)
        if msg:
            print('k', msg.key(), flush=True)
            print('v', msg.value(), flush=True)
            print("key", msg.key().decode(), flush=True)
            print("corr", correlation_id, flush=True)
            if msg.key().decode() == correlation_id:
                return msg.value().decode()

# def consume_and_respond():
#     consumer = get_consumer("request-listener", REQUEST_TOPIC)
#     while True:
#         msg = consumer.poll(1.0)
#         if msg and not msg.error():
#             key = msg.key().decode()
#             value = json.loads(msg.value().decode())
#             send_message(RESPONSE_TOPIC, key=key, value=value['filepath'])