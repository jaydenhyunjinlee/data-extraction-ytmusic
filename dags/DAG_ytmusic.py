from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from get_songs import get_songs
from load_songs import load_songs

# DAG config
default_args = {
    'owner':...,
    'email':...,
    'email_on_failure':...,
    'email_on_retry':...,
    'retries':...,
    'retry_delay':...
}

# file / entity set name configuration
date = datetime.today()
tbl_name = 'songs_{year}_{month}_{day}'.format(year=date.year, month=str(date.month).rjust(2, '0'), day=str(date.day).rjust(2, '0'))
most_listened_view_name = 'most_listened_{year}_{month}_{day}'.format(year=date.year, month=str(date.month).rjust(2, '0'), day=str(date.day).rjust(2, '0'))
num_songs_played_view_name = 'num_songs_played_{year}_{month}_{day}'.format(year=date.year, month=str(date.month).rjust(2, '0'), day=str(date.day).rjust(2, '0'))

# Use context manager `with` phrase to develop under DAG environment
with DAG('DAG_ytmusic', default_args=default_args, start_date=..., \
schedule_interval=..., catchup=False) as dag: # `catchup-False` to avoid overly instantiating DAG 

    container_name = 'NAME _OF_POSTGRES_DOCKER_CONTAINER'
    docker_starter = 'docker start {}'.format(container_name)
    t0 = BashOperator(
        task_id='start_docker_container',
        bash_command=docker_starter
    )

    t1 = PythonOperator(
        task_id='get_songs',
        python_callable=get_songs
    )

    t2 = PythonOperator(
        task_id='load_songs',
        python_callable=load_songs
    )

    t3 = PostgresOperator(
        task_id='listened_to_the_most',
        postgres_conn_id='postgres_connector', # Postgres connector must be installed externally 
        sql='sql/most_listened.sql',
        params={
            'tbl_name':tbl_name,
            'view_name':most_listened_view_name
        }
    )

    t4 = PostgresOperator(
        task_id='num_played',
        postgres_conn_id='postgres_connector',
        sql='sql/num_played_today.sql',
        params={
            'tbl_name':tbl_name,
            'view_name':num_songs_played_view_name
        }
    )

    docker_stopper = 'docker stop {}'.format(container_name)
    t5 = BashOperator(
        task_id='stop_docker_container',
        bash_command=docker_stopper
    )

    # Order of task executions
    [t0, t1] >> t2 >> [t3, t4] >> t5

