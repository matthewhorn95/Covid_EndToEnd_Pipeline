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

    # Convert object (string) type to datetime for curr_date variable
    ind_prod_df["CURR_DATE"] = pd.to_datetime(ind_prod_df["CURR_DATE"])
    gdp_df["CURR_DATE"] = pd.to_datetime(gdp_df["CURR_DATE"])
    us_cpi_df["CURR_DATE"] = pd.to_datetime(us_cpi_df["CURR_DATE"])
    trade_balance_df["CURR_DATE"] = pd.to_datetime(trade_balance_df["CURR_DATE"])
    mortgage_df["CURR_DATE"] = pd.to_datetime(mortgage_df["CURR_DATE"])
    unemployment_df["CURR_DATE"] = pd.to_datetime(unemployment_df["CURR_DATE"])

    # Subset the data to keep only years after 2000 (inclusive)
    ind_prod_df = ind_prod_df.loc[ind_prod_df["CURR_DATE"] >= "2000-01-01"]
    gdp_df = gdp_df.loc[gdp_df["CURR_DATE"] >= "2000-01-01"]
    us_cpi_df = us_cpi_df.loc[us_cpi_df["CURR_DATE"] >= "2000-01-01"]
    trade_balance_df = trade_balance_df.loc[trade_balance_df["CURR_DATE"] >= "2000-01-01"]
    mortgage_df = mortgage_df.loc[mortgage_df["CURR_DATE"] >= "2000-01-01"]
    unemployment_df = unemployment_df.loc[unemployment_df["CURR_DATE"] >= "2000-01-01"]

    # Output the data frames to csv in the data/transformed directory for the project
    stocks_df.to_csv(f'/Users/matthewmac/airflow/CovidE2EPipe/data/transformed/stocks_transformed_{datetime.now().date()}.csv')
    currency_df.to_csv(f'/Users/matthewmac/airflow/CovidE2EPipe/data/transformed/currency_transformed_{datetime.now().date()}.csv')
    ind_prod_df.to_csv(f'/Users/matthewmac/airflow/CovidE2EPipe/data/transformed/ind_prod_transformed_{datetime.now().date()}.csv')
    gdp_df.to_csv(f'/Users/matthewmac/airflow/CovidE2EPipe/data/transformed/gdp_transformed_{datetime.now().date()}.csv')
    us_cpi_df.to_csv(f'/Users/matthewmac/airflow/CovidE2EPipe/data/transformed/us_cpi_transformed_{datetime.now().date()}.csv')
    trade_balance_df.to_csv(f'/Users/matthewmac/airflow/CovidE2EPipe/data/transformed/trade_balance_transformed_{datetime.now().date()}.csv')
    mortgage_df.to_csv(f'/Users/matthewmac/airflow/CovidE2EPipe/data/transformed/mortgage_transformed_{datetime.now().date()}.csv')
    unemployment_df.to_csv(f'/Users/matthewmac/airflow/CovidE2EPipe/data/transformed/unemployment_transformed_{datetime.now().date()}.csv')

# Make sure the script is only run when executed, not every time it's imported
if __name__ == "__main__":
    main()