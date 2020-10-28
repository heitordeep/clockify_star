from datetime import datetime, timedelta

import pendulum
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

local_tz = pendulum.timezone('America/Sao_Paulo')

path_allowed = '/usr/local/airflow'
activate_env = f'{path_allowed}/venv/bin/activate'
path_project = f'{path_allowed}/dags/clockify_star'

config_default = {
    'owner': 'Get-Parameter',
    'depends_on_past': False,
    'email': ['heitor.aguia@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'start_date': datetime(2020, 10, 28, tzinfo=local_tz),
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    dag_id='update_jsons',
    schedule_interval='00 12 * * 1-5',
    default_args=config_default,
    catchup=False,
)

bash_start = BashOperator(
    task_id='run-script-python',
    bash_command=(
        f'. {activate_env} && cd {path_project}/ && '
        f'. cron.sh update >> '
        f'{path_allowed}/log_update_file_json.txt 2>&1'
    ),
    dag=dag,
)
