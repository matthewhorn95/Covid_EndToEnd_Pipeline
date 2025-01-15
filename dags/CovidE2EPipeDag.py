from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import pendulum
import sys

# Include the airflow directory in the python path to access the helper functions
sys.path.insert(0, '/Users/matthewmac/airflow')

# Import helper functions for tasks
from CovidE2EPipe.helper_scripts.api_fetch import main as api_fetch
from CovidE2EPipe.helper_scripts.transform_raw_data import main as transform

#print("Running fetch imported function")
#api_fetch()
#print("Api fetch done")

#
#
#

# Set the default arguments for the DAG
default_args = {
    'owner': 'Matthew Horn',
    'start_date': pendulum.datetime(2025, 1, 1, tz="America/Los_Angeles"),
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

# Define the DAG to run every day at noon
dag = DAG(
    dag_id='CovidE2EPipeDag',
    default_args=default_args,
    description='Covid End To End Pipeline Data Engineering Project',
    schedule_interval='0 12 * * *'
)

# Task to fetch raw data from api's and store locally in csv files
fetch_raw_data = PythonOperator(
    task_id='fetch_raw',
    python_callable=api_fetch,
    dag=dag
)

def convert_to_local_timezone(**kwargs):
    # Get the current date in UTC
    utc_date = pendulum.now("UTC")
    
    # Convert the UTC date to your local time zone
    local_date = utc_date.in_timezone(pendulum.timezone('America/Los_Angeles'))
    
    # Push the local date to XCom for downstream tasks
    kwargs['ti'].xcom_push(key='local_date', value=local_date.format('YYYY-MM-DD'))


# Task to convert `{{ ds }}` to local timezone
convert_date_to_local_tz = PythonOperator(
    task_id='convert_to_local_tz',
    python_callable=convert_to_local_timezone,
    provide_context=True
)

# Task to stage raw data
stage_raw_data = BashOperator(
    task_id='stage_raw_data',
    bash_command='snow stage copy "/Users/matthewmac/airflow/CovidE2EPipe/data/raw/*.csv" @CovidE2EPipeDatabase.raw_data.daily',
    dag=dag
)

# Task to create sql executable file daily to transfer daily raw data from the stage to tables
create_load_sql_file = BashOperator(
    task_id='create_load_sql_file',
    bash_command=f"""echo "TRUNCATE TABLE CovidE2EPipeDatabase.raw_data.industrial_production;
    TRUNCATE TABLE CovidE2EPipeDatabase.raw_data.stocks_eod;
    TRUNCATE TABLE CovidE2EPipeDatabase.raw_data.currency_exchanges;
    TRUNCATE TABLE CovidE2EPipeDatabase.raw_data.gdp;
    TRUNCATE TABLE CovidE2EPipeDatabase.raw_data.us_cpi;
    TRUNCATE TABLE CovidE2EPipeDatabase.raw_data.unemployment_rate;
    TRUNCATE TABLE CovidE2EPipeDatabase.raw_data.thirty_yr_mortgage;
    TRUNCATE TABLE CovidE2EPipeDatabase.raw_data.trade_balance;
    
    COPY INTO CovidE2EPipeDatabase.raw_data.industrial_production
    FROM @CovidE2EPipeDatabase.raw_data.daily/industrial_production_{datetime.now().date()}.csv
    FILE_FORMAT = ( TYPE='CSV' )
    ON_ERROR = 'CONTINUE';

    COPY INTO CovidE2EPipeDatabase.raw_data.stocks_eod
    FROM @CovidE2EPipeDatabase.raw_data.daily/stocks_eod_{datetime.now().date()}.csv
    FILE_FORMAT = ( TYPE='CSV' )
    ON_ERROR = 'CONTINUE';

    COPY INTO CovidE2EPipeDatabase.raw_data.currency_exchanges
    FROM @CovidE2EPipeDatabase.raw_data.daily/currency_exchanges_{datetime.now().date()}.csv
    FILE_FORMAT = ( TYPE='CSV' )
    ON_ERROR = 'CONTINUE';

    COPY INTO CovidE2EPipeDatabase.raw_data.gdp
    FROM @CovidE2EPipeDatabase.raw_data.daily/GDP_{datetime.now().date()}.csv
    FILE_FORMAT = ( TYPE='CSV' )
    ON_ERROR = 'CONTINUE';

    COPY INTO CovidE2EPipeDatabase.raw_data.us_cpi
    FROM @CovidE2EPipeDatabase.raw_data.daily/US_CPI_{datetime.now().date()}.csv
    FILE_FORMAT = ( TYPE='CSV' )
    ON_ERROR = 'CONTINUE';

    COPY INTO CovidE2EPipeDatabase.raw_data.unemployment_rate
    FROM @CovidE2EPipeDatabase.raw_data.daily/unemployment_rate_{datetime.now().date()}.csv
    FILE_FORMAT = ( TYPE='CSV' )
    ON_ERROR = 'CONTINUE';

    COPY INTO CovidE2EPipeDatabase.raw_data.thirty_yr_mortgage
    FROM @CovidE2EPipeDatabase.raw_data.daily/30yr_mortage_{datetime.now().date()}.csv
    FILE_FORMAT = ( TYPE='CSV' )
    ON_ERROR = 'CONTINUE';

    COPY INTO CovidE2EPipeDatabase.raw_data.trade_balance
    FROM @CovidE2EPipeDatabase.raw_data.daily/trade_balance_{datetime.now().date()}.csv
    FILE_FORMAT = ( TYPE='CSV' )
    ON_ERROR = 'CONTINUE';
    " > /Users/matthewmac/airflow/CovidE2EPipe/helper_scripts/load_staged_data_{datetime.now().date()}.sql""",
    dag=dag
)

# Task to stage sql load executable file
stage_sql_exe = BashOperator(
    task_id='stage_sql',
    bash_command='snow stage copy /Users/matthewmac/airflow/CovidE2EPipe/helper_scripts/load_staged_data_{{ ti.xcom_pull(task_ids="convert_to_local_tz", key="local_date") }}.sql @CovidE2EPipeDatabase.raw_data.daily',
    dag=dag
)

# Task to insert staged raw data into tables
insert_staged_raw_data = BashOperator(
    task_id='insert_staged_raw_data',
    bash_command='snow stage execute @CovidE2EPipeDatabase.raw_data.daily/load_staged_data_{{ ti.xcom_pull(task_ids="convert_to_local_tz", key="local_date") }}.sql',
    dag=dag
)

# Task to append daily loaded raw data to all time data
append_daily_raw_data = BashOperator(
    task_id='append_daily_raw_data',
    bash_command='snow stage execute @CovidE2EPipeDatabase.raw_data.permanent/append_raw_data.sql',
    dag=dag
)

# Task to clean up the sql executable from local storage and snowflake stage
clean_up_sql_exe = BashOperator(
    task_id='clean_up_sql_exe',
    bash_command='rm /Users/matthewmac/airflow/CovidE2EPipe/helper_scripts/load_staged_data_{{ ti.xcom_pull(task_ids="convert_to_local_tz", key="local_date") }}.sql',
    dag=dag
)

# Task to unstage used files
unstage_files = BashOperator(
    task_id='unstage_files',
    bash_command=f"""snow stage remove CovidE2EPipeDatabase.raw_data.daily load_staged_data_{datetime.now().date()}.sql;
                    snow stage remove CovidE2EPipeDatabase.raw_data.daily unemployment_rate_{datetime.now().date()}.csv;
                    snow stage remove CovidE2EPipeDatabase.raw_data.daily trade_balance_{datetime.now().date()}.csv;
                    snow stage remove CovidE2EPipeDatabase.raw_data.daily 30yr_mortgage_{datetime.now().date()}.csv;
                    snow stage remove CovidE2EPipeDatabase.raw_data.daily US_CPI_{datetime.now().date()}.csv;
                    snow stage remove CovidE2EPipeDatabase.raw_data.daily GDP_{datetime.now().date()}.csv;
                    snow stage remove CovidE2EPipeDatabase.raw_data.daily industrial_production_{datetime.now().date()}.csv;""",
    dag=dag
)

# Task to archive old raw data files that have already been uploaded to Snowflake
archive_raw_data = BashOperator(
    task_id='archive_raw_data',
    bash_command=f'cd /Users/matthewmac/airflow/CovidE2EPipe/data/raw && \
                    zip raw_data_{datetime.now().date()}.zip *.csv && \
                  mv raw_data_{datetime.now().date()}.zip archived && \
                    rm *.csv',
    dag=dag
)

# Task to archive the previous day's transformed data before overwriting it with the new day's
archive_transformed_data = BashOperator(
    task_id='archive_transformed_data',
    bash_command=f'cd /Users/matthewmac/airflow/CovidE2EPipe/data/transformed && \
                    zip raw_data_{datetime.now().date()}.zip *.csv && \
                    mv raw_data_{datetime.now().date()}.zip archived/',
    dag=dag
)

# Task to transform the appended raw data via the transform_raw_data.py script
transform_data = PythonOperator(
    task_id='transform_data',
    python_callable=transform,
    dag=dag
)

# Define the task dependencies in the pipeline
fetch_raw_data >> stage_raw_data
fetch_raw_data >> create_load_sql_file
convert_date_to_local_tz >> stage_raw_data
create_load_sql_file >> stage_sql_exe
stage_raw_data >> stage_sql_exe
stage_sql_exe >> insert_staged_raw_data
insert_staged_raw_data >> append_daily_raw_data
insert_staged_raw_data >> clean_up_sql_exe
insert_staged_raw_data >> archive_raw_data
append_daily_raw_data >> unstage_files
append_daily_raw_data >> transform_data
transform_data >> archive_transformed_data