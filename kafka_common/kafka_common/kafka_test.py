from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException
from .config import KAFKA_BROKER_URL

def create_topic(topic_name: str, num_partitions: int = 1, replication_factor: int = 1):
    admin = AdminClient({'bootstrap.servers': KAFKA_BROKER_URL})

    fs = admin.create_topics([
        NewTopic(topic=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
    ])

    for topic, f in fs.items():
        try:
            f.result()  # exception 던지면 실패한 것
            print(f"[Kafka] 토픽 '{topic}' 생성 성공")
        except KafkaException as e:
            # 이미 있는 경우엔 에러 던지니까 무시해도 됨
            if "Topic already exists" in str(e):
                print(f"[Kafka] 토픽 '{topic}' 이미 존재함 (무시)")
            else:
                print(f"[Kafka] 토픽 '{topic}' 생성 실패: {e}")