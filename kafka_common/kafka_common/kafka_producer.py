import time
from threading import Lock
from confluent_kafka import Producer, KafkaException
from .config import KAFKA_BROKER_URL

_producer = None
_lock = Lock()

def get_kafka_producer():
    global _producer
    with _lock:
        if _producer is not None:
            return _producer
        while True:
            try:
                _producer = Producer({'bootstrap.servers': KAFKA_BROKER_URL})
                _producer.list_topics(timeout=5)
                print("Kafka 연결 성공!")
                break
            except KafkaException as e:
                print(f"Kafka 연결 실패: {e}, 3초 뒤 재시도")
                time.sleep(3)
        return _producer

def send_message(topic: str, key: str, value: str):
    p = get_kafka_producer()
    p.produce(topic, key=key, value=value)
    p.flush()
