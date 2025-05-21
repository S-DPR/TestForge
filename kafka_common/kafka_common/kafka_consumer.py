import time
from confluent_kafka import Consumer, KafkaException
from .config import KAFKA_BROKER_URL


def get_consumer(group_id: str, topic: list[str]):
    while True:
        try:
            _consumer = Consumer({
                'bootstrap.servers': KAFKA_BROKER_URL,
                'group.id': group_id,
                'auto.offset.reset': 'earliest'
            })
            _consumer.subscribe(topic)
            print(f"Kafka Consumer 연결 성공! group_id={group_id}, topic={','.join(topic)}", flush=True)
            return _consumer
        except KafkaException as e:
            print(f"Kafka Consumer 연결 실패: {e}, 3초 뒤 재시도", flush=True)
            time.sleep(3)
