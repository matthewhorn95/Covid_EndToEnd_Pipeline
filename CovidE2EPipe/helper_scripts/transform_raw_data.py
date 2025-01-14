import modin.pandas as pd
import snowflake.snowpark.modin.plugin
from snowflake.snowpark.session import Session
from functools import reduce
from datetime import datetime

def main():
    # Create a snowpark session with a default connection
    session = Session.builder.create()

    # Take the appropriate schema into use to import the raw data
    session.use_schema('CovidE2EPipeDatabase.raw_data')

    # Start using the pandas api and import the raw data csv files as data frames
    stocks_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.stocks_eod_appended')
    currency_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.currency_exchanges_appended')
    ind_prod_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.industrial_production_appended')[["CURR_DATE", "VALUE"]].rename(columns={'VALUE': 'industrial_production'})
    gdp_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.gdp_appended')[["CURR_DATE", "VALUE"]].rename(columns={'VALUE': 'GDP'})
    us_cpi_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.us_cpi_appended')[["CURR_DATE", "VALUE"]].rename(columns={'VALUE': 'CPI'})
    trade_balance_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.trade_balance_appended')[["CURR_DATE", "VALUE"]].rename(columns={'VALUE': 'trade_balance'})
    mortgage_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.thirty_yr_mortgage_appended')[["CURR_DATE", "VALUE"]].rename(columns={'VALUE': 'thirty_yr_mortgage'})
    unemployment_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.unemployment_rate_appended')[["CURR_DATE", "VALUE"]].rename(columns={'VALUE': 'unemployment_rate'})


    stocks_df.to_csv(f'/Users/matthewmac/airflow/CovidE2EPipe/data/transformed/stocks_transformed_{datetime.now().date()}.csv')
    currency_df.to_csv(f'/Users/matthewmac/airflow/CovidE2EPipe/data/transformed/currency_transformed_{datetime.now().date()}.csv')
    ind_prod_df.to_csv(f'/Users/matthewmac/airflow/CovidE2EPipe/data/transformed/ind_prod_transformed_{datetime.now().date()}.csv')
    gdp_df.to_csv(f'/Users/matthewmac/airflow/CovidE2EPipe/data/transformed/gdp_transformed_{datetime.now().date()}.csv')
    us_cpi_df.to_csv(f'/Users/matthewmac/airflow/CovidE2EPipe/data/transformed/us_cpi_transformed_{datetime.now().date()}.csv')
    trade_balance_df.to_csv(f'/Users/matthewmac/airflow/CovidE2EPipe/data/transformed/trade_balance_transformed_{datetime.now().date()}.csv')
    mortgage_df.to_csv(f'/Users/matthewmac/airflow/CovidE2EPipe/data/transformed/mortgage_transformed_{datetime.now().date()}.csv')
    unemployment_df.to_csv(f'/Users/matthewmac/airflow/CovidE2EPipe/data/transformed/unemployment_transformed_{datetime.now().date()}.csv')

main()