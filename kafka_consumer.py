import asyncio
import logging
from confluent_kafka import Consumer, KafkaException, KafkaError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def consume_kafka_messages():
    consumer = Consumer({
        'bootstrap.servers': 'your_kafka_broker:9092',
        'group.id': 'airflow-group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe(['your_topic'])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                await asyncio.sleep(1)
                continue
            if msg.error():
                handle_kafka_error(msg)
            else:
                message_value = msg.value().decode('utf-8')
                logger.info(f"Received message: {message_value}")
                await process_message(message_value)
    except Exception as e:
        logger.error(f"Error consuming messages: {e}")
    finally:
        consumer.close()

def handle_kafka_error(msg):
    if msg.error().code() == KafkaError._PARTITION_EOF:
        logger.info(f"End of partition reached {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
    else:
        raise KafkaException(msg.error())

async def process_message(message):
    odds_difference = calculate_odds_difference(message)
    if abs(odds_difference) > 10:
        trigger_alert(odds_difference)

def calculate_odds_difference(message):
    # Placeholder function to calculate the difference in odds
    return float(message)  # Example: assuming the message is a string representation of the odds difference

def trigger_alert(odds_difference):
    logger.warning(f"Alert! Odds difference is {odds_difference}")

async def main():
    try:
        await consume_kafka_messages()
    except asyncio.CancelledError:
        logger.info("Consumer task cancelled. Shutting down gracefully.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted by user. Exiting...")