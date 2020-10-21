from datetime import datetime, timedelta

import pendulum
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

local_tz = pendulum.timezone('America/Sao_Paulo')

path_allowed = '/usr/local/airflow'

config_default = {
    'owner': 'Scheduler-Clockify',
    'depends_on_past': False,
    'email': ['heitor.aguia@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'start_date': datetime(2020, 10, 21, tzinfo=local_tz),
    'retry_delay': timedelta(minutes=1),
}

dag_config = {
    'Clockify-Start': '00 09 * * 1-5',
    'Clockify-Stop-For-Lunch': '00 13 * * 1-5',
    'Clockify-Start-After-Lunch': '00 14 * * 1-5',
    'Clockify-End': '00 18 * * 1-5',
}


def create_dag(dag_id, schedule):

    dag = DAG(
        dag_id=dag_id,
        schedule_interval=schedule,
        default_args=config_default,
        catchup=False,
    )

    def call_clockify(**kwargs):
        activate_env = f'{path_allowed}/venv/bin/activate'
        path_project = f'{path_allowed}/dags/clockify_star'

        # Checks whether to start or stop.
        command = (
            lambda hour: 'start'
            if hour == '00 09 * * 1-5' or hour == '00 14 * * 1-5'
            else 'stop'
        )

        # Activate env, run shell script with parameter (start or stop)
        # and save logs.
        bash_start = BashOperator(
            task_id=f'run-script-shell',
            bash_command=(
                f'. {activate_env} && cd {path_project}/ && '
                f'. cron.sh {command(schedule)} >> '
                f'{path_allowed}/log_clockify.txt 2>&1'
            ),
            dag=dag,
        )

        # Update task, tags, projects id.
        bash_update_json = BashOperator(
            task_id='update-json',
            bash_command=(
                f'. {activate_env} && cd {path_project}/ &&'
                f'. cron.sh update >> '
                f'{path_allowed}/log_update_json.txt 2>&1'
            ),
            dag=dag,
        )

        bash_start.execute(context=kwargs)
        bash_update_json.execute(context=kwargs)

        bash_start >> bash_update_json

    with dag:

        t1 = PythonOperator(
            task_id='job_clockify', python_callable=call_clockify, dag=dag
        )

    return dag


for dag_id, schedule in dag_config.items():
    globals()[dag_id] = create_dag(dag_id, schedule)
