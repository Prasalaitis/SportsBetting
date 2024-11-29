from kafka import KafkaProducer
import json
from typing import Any, Dict

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def produce_message(topic: str, message: Dict[str, Any]) -> None:
    producer.send(topic, message)
    producer.flush()