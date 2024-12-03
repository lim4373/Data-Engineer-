from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

# Default Arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 6, 26),  # DAG 시작 날짜
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

# Define the DAG
dag = DAG(
    "newjeans-youtube-pipeline",
    default_args=default_args,
    max_active_runs=1,
    schedule_interval="30 0 * * *",  # 매일 00:30 UTC에 실행
    catchup=False,
    tags=['data']
)

# Task: Download data
download_data = BashOperator(
    task_id='download-data',
    bash_command='/opt/airflow/jobs/download-data.sh {{ ds }}',  # ds는 실행 날짜를 전달
    dag=dag
)

# Task: Process data
process_data = BashOperator(
    task_id='process-data',
    bash_command='python3 /opt/airflow/jobs/main.py --target_date {{ ds }}',  # target_date에 {{ ds }} 사용
    dag=dag
)

# Set task dependencies
download_data >> process_data
