import time
from dataclasses import dataclass
import threading

from confluent_kafka import Consumer, KafkaException
from .config import KAFKA_BROKER_URL

@dataclass
class ConsumerPoolKey:
    group_id: str
    topic: list[str]

class ConsumerDemander:
    def __init__(self, consumer_pool_key: ConsumerPoolKey):
        self.consumer = get_consumer(consumer_pool_key.group_id, consumer_pool_key.topic)
        self.is_running = False
        self.lock = threading.Lock()

    def run(self, correlation_id: str):
        with self.lock:
            self.is_running = True
            while True:
                msg = self.consumer.poll(1.0)
                print(msg, flush=True)
                if msg:
                    print('k', msg.key(), flush=True)
                    print('v', msg.value(), flush=True)
                    print("key", msg.key().decode(), flush=True)
                    print("corr", correlation_id, flush=True)
                    if msg.key().decode() == correlation_id:
                        self.is_running = False
                        return msg.value().decode()

    def get_is_running(self):
        with self.lock:
            return self.is_running

class ConsumerPool:
    def __init__(self):
        self._consumerPool: dict[ConsumerPoolKey, list[ConsumerDemander]] = {}
        self.lock = threading.Lock()

    def set_consumer(self, consumer_pool_key: ConsumerPoolKey, consumer_count: int = 1):
        if consumer_pool_key in self._consumerPool:
            return
        self._consumerPool[consumer_pool_key] = []
        for _ in range(consumer_count):
            self._consumerPool[consumer_pool_key].append(ConsumerDemander(consumer_pool_key))

    def get_consumer(self, consumer_pool_key: ConsumerPoolKey) -> ConsumerDemander:
        while True:
            with self.lock:
                for consumer in self._consumerPool[consumer_pool_key]:
                    if not consumer.get_is_running():
                        return consumer
            print("Consumer가 모두 사용중입니다. 3초 대기중...", flush=True)
            time.sleep(3)

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
