from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from scripts.extract import main as extract_main
from scripts.transform import transform_data
from scripts.store import main as store_main


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'data_pipeline',
    default_args=default_args,
    description='A simple data pipeline that extracts article data, transforms it, and stores it using DVC.',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2022, 1, 1),
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_main
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        op_kwargs={'articles': '{{ ti.xcom_pull(task_ids="extract_data") }}'}
    )

    store_task = PythonOperator(
        task_id='store_data',
        python_callable=store_main,
        op_kwargs={'articles': '{{ ti.xcom_pull(task_ids="transform_data") }}'}
    )

    extract_task >> transform_task >> store_task
