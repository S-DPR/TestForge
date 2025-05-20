from confluent_kafka import Producer
from .config import KAFKA_BROKER_URL

producer = Producer({'bootstrap.servers': KAFKA_BROKER_URL})

def send_message(topic: str, key: str, value: str):
    producer.produce(topic, key=key, value=value)
    producer.flush()