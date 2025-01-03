from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import sys

# Include the airflow directory in the python path to access the helper functions
sys.path.insert(0, '/Users/matthewmac/airflow')

# Import helper functions for tasks
from helper_scripts.api_fetch import main as api_fetch

#
#
#

# Set the default arguments for the DAG
default_args = {
    'owner': 'Matthew Horn',
    'start_date': datetime(2025, 1, 1),
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
    python_callable=api_fetch,
    dag=dag
)

# Task to stage raw data
stage_raw_data = BashOperator(
    task_id='stage_raw_data',
    bash_command='snow stage copy ~/airflow/data/raw/industrial_production_{{ ds }}.csv @raw_data_stage',
    dag=dag
)

# Task to create sql executable file daily to transfer daily raw data from the stage to tables
create_load_sql_file = BashOperator(
    task_id='create_load_sql_file',
    bash_command="""
    echo "COPY INTO CovidE2EPipeDatabase.raw_data.industrial_production
    FROM @raw_data_stage
    FILES = ('~/airflow/data/raw/industrial_production_{{ ds }}.csv')
    FILE_FORMAT = ( TYPE='CSV' )
    ON_ERROR = 'CONTINUE';
    " > ~/airflow/helper_scripts/load_staged_data_{{ ds }}.sql
    """,
    dag=dag
)

# Task to stage sql executable file
stage_sql_exe = BashOperator(
    task_id='stage_sql',
    bash_command='snow stage copy ~/airflow/helper_scripts/load_staged_data_{{ ds }}.sql',
    dag=dag
)

# Task to insert staged raw data into tables
insert_staged_raw_data = BashOperator(
    task_id='insert_staged_raw_data',
    bash_command='snow stage execute @raw_data_stage/load_staged_data_{{ ds }}.sql',
    dag=dag
)

# Task to clean up the sql executable from local storage and snowflake stage
clean_up_sql_files = BashOperator(
    task_id='clean_up_sql_exe',
    bash_command='snow stage remove @raw_data_stage/load_staged_data_{{ ds }}.sql; \
                  rm ~/airflow/helper_scripts/load_staged_data_{{ ds }}.sql',
    dag=dag
)

# Task to archive old raw data files that have already been uploaded to snowflake
archive_raw_data = BashOperator(
    task_id='archive_raw_data',
    bash_command='cd ~/airflow/data/raw && zip raw_data_{{ ds }}.zip *.csv \
                    && mv raw_data_{{ ds }}.zip archived/',
    dag=dag
)

# Define the pipeline task dependencies
(
    fetch_raw_data 
    >> [stage_raw_data, create_load_sql_file] 
    >> stage_sql_exe 
    >> insert_staged_raw_data 
    >> [clean_up_sql_files, archive_raw_data]

)