from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from main import main

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 29),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'betfair_trading_platform',
    default_args=default_args,
    description='A DAG for Betfair Trading Platform',
    schedule_interval=timedelta(days=1),
)

run_main = PythonOperator(
    task_id='run_main',
    python_callable=main,
    dag=dag,
)