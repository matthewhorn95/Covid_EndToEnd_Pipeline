import modin.pandas as pd
import snowflake.snowpark.modin.plugin
from snowflake.snowpark.session import Session

# Create a snowpark session with a default connection
session = Session.builder.create()

# Take the appropriate schema into use to import the raw data
session.use_schema('CovidE2EPipeDatabase.raw_data')

# Start using the pandas api and import the raw data csv files as data frames
#stocks_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.stocks_eod_appended')
#currency_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.currency_exchanges_appended')
ind_prod_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.industrial_production_appended')
gdp_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.gdp_appended')
us_cpi_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.us_cpi_appended')
trade_balance_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.trade_balance_appended')
mortgage_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.thirty_yr_mortgage_appended')
unemployment_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.unemployment_rate_appended')

print(ind_prod_df.head())






