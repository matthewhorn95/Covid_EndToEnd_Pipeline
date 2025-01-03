from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

import sys
# Include the airflow directory in the python path to access the helper functions
sys.path.insert(0, '/Users/matthewmac/airflow')


# Import helper functions for tasks
from helper_scripts.print_helper import helper_print_task

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

# Define the bash echo task
task1 = BashOperator(
    task_id='echo1',
    bash_command='echo One',
    dag=dag
)

# Define the main function for the python task
def print_task():
    print("Two")

# Define the python print task
task2 = PythonOperator(
    task_id='print2',
    python_callable=print_task,
    dag=dag
)

# Define the imported helper print task
task3 = PythonOperator(
    task_id='print3',
    python_callable=helper_print_task,
    dag=dag
)

# Define the pipeline dependencies
task1 >> [task2, task3]
