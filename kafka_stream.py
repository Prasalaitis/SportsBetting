import json
import requests
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os

# Default arguments for the DAG
default_args = {
    'owner': 'prasalaitis',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 29),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email': [os.getenv('ALERT_EMAIL', 'default@example.com')],
}


# Define the function to stream data
def stream_data():
    import logging
    logger = logging.getLogger(__name__)

    try:
        res = requests.get("https://betfair.com")
        res.raise_for_status()  # Raise an HTTPError for bad responses
        data = res.json()
        logger.info(f"Received data: {data}")
        return data
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from Betfair: {e}")
        return None


# Define the DAG
dag = DAG(
    'kafka_consumer_dag',
    default_args=default_args,
    description='A DAG to consume Kafka messages and process them',
    schedule_interval=timedelta(minutes=1),
)

# Define the task to stream data
streaming_task = PythonOperator(
    task_id='stream_data',
    python_callable=stream_data,
    dag=dag,
)

# Define the task to consume Kafka messages (assuming consume_kafka_messages is defined elsewhere)
consume_task = PythonOperator(
    task_id='consume_kafka_messages',
    python_callable=consume_kafka_messages,
    dag=dag,
)

# Set task dependencies if needed
# Example: consume_task.set_upstream(streaming_task)

# Add logging to track the execution of the DAG
streaming_task.log.info('Streaming data task has been set up.')
consume_task.log.info('Kafka consumer task has been set up.')