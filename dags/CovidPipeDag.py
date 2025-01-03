from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from datetime import datetime


import sys
# Include the airflow directory in the python path to access the helper functions
sys.path.insert(0, '/Users/matthewmac/airflow')


# Import helper functions for tasks
from helper_scripts.print_helper import helper_print_task
from helper_scripts.api_fetch import main as api_fetch

# Set the default arguments for the DAG
default_args = {
    'owner': 'Matthew Horn',
    'start_date': datetime.now(),
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

# Define the DAG object
dag = DAG(
    dag_id='CovidE2EPipeDag',
    default_args=default_args,
    description='Covid End To End Pipeline Data Engineering Project',
    schedule_interval='* * * * *'
)

# Task to fetch raw data from api's and store locally in csv files
fetch_raw_data = PythonOperator(
    task_id='fetch_raw',
    python_callable=api_fetch
)

# Task to stage raw data
stage_raw_data = SnowflakeOperator(
    task_id='stage_raw_data',
    snowflake_conn_id='snowflake_default',
    autocommit=True,
    sql=f"PUT ~/airflow/data/raw/industrial_production_{datetime.now().date()}.csv @raw_data_stage",
    database='CovidE2EPipDatabase',
    schema='raw_data',
    warehouse='COMPUTE_WH',
    dag=dag
)

# SQL code to copy staged raw data into tables in raw_data schema
upload_sql = f"""
COPY INTO raw_data_schema.industrial_production
FROM @raw_data_stage/industrial_production_{datetime.now().date()}.csv
FILE_FORMAT = (TYPE = 'CSV')
ON_ERROR = 'CONTINUE';
"""


# Task to insert staged raw data into tables
insert_staged_raw_data = SnowflakeOperator(
    task_id='insert_staged_raw_data',
    snowflake_conn_id='snowflake_default',
    sql=upload_sql,
    database='CovidE2EPipDatabase',
    schema='raw_data',
    warehouse='COMPUTE_WH',
    dag=dag
)

fetch_raw_data >> stage_raw_data >> insert_staged_raw_data
