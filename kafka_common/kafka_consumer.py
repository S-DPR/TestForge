from confluent_kafka import Consumer
from .config import KAFKA_BROKER_URL

def get_consumer(group_id: str, topic: str):
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BROKER_URL,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])
    return consumer