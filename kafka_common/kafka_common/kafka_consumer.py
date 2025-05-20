import time
from confluent_kafka import Consumer, KafkaException
from .config import KAFKA_BROKER_URL


def get_consumer(group_id: str, topic: str):
    while True:
        try:
            _consumer = Consumer({
                'bootstrap.servers': KAFKA_BROKER_URL,
                'group.id': group_id,
                'auto.offset.reset': 'earliest'
            })
            _consumer.subscribe([topic])
            _consumer.list_topics(timeout=5)  # 연결 테스트용
            while not _consumer.assignment():
                print("Waiting for partition assignment...", flush=True)
                _consumer.poll(0)
                _consumer.list_topics(timeout=5)
                time.sleep(0.5)
            print(f"Kafka Consumer 연결 성공! group_id={group_id}, topic={topic}", flush=True)
            return _consumer
        except KafkaException as e:
            print(f"Kafka Consumer 연결 실패: {e}, 3초 뒤 재시도", flush=True)
            time.sleep(3)

    return None