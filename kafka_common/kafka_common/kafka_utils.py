from confluent_kafka import Producer, KafkaException
from config import KAFKA_BROKER_URL
import time

conf = {'bootstrap.servers': KAFKA_BROKER_URL}

while True:
    try:
        p = Producer(**conf)
        p.list_topics(timeout=5)
        break
    except KafkaException as e:
        print(f"Kafka 연결 실패: {e}, 3초 뒤 재시도")
        time.sleep(3)