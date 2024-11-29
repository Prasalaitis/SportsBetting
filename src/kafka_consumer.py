from kafka import KafkaConsumer
import json
from typing import Any

def consume_messages(topic: str) -> None:
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='betfair-group',
        value_serializer=lambda v: json.loads(v.decode('utf-8'))
    )
    for message in consumer:
        print(f"Consumed message: {message.value}")