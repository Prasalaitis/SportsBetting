from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'prasalaitis',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 29),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email': ['gyvenimasritmu@gmail.com'],
}

dag = DAG(
    'kafka_consumer_dag',
    default_args=default_args,
    description='A simple Kafka consumer DAG',
    schedule_interval=timedelta(minutes=1),
)

consume_task = PythonOperator(
    task_id='consume_kafka_messages',
    python_callable=consume_kafka_messages,
    dag=dag,
)