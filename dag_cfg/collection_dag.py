from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from dag_main import main_func

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}

dag = DAG(
    'data_collection_dag',
    default_args=default_args,
    description='A simple data collection DAG',
    schedule=timedelta(days=1),
    start_date=datetime(2024, 7, 30),
    catchup=False,
)

run_etl = PythonOperator(
    task_id='data_collection',
    python_callable=main_func,
    dag=dag,
)

run_etl
