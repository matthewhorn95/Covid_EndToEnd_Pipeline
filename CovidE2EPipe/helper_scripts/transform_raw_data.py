import modin.pandas as pd
import snowflake.snowpark.modin.plugin

import modin.pandas as pd

# Import the Snowpark plugin for modin.
import snowflake.snowpark.modin.plugin

# Create a Snowpark session with a default connection.
from snowflake.snowpark.session import Session
session = Session.builder.create()

stocks_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.stocks_eod_appended')
currency_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.currency_exchanges_appended')
ind_prod_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.industrial_production_appended')
gdp_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.gdp_appended')
us_cpi_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.us_cpi_appended')
trade_balance_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.trade_balance_appended')
mortgage_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.thirty_yr_mortage_appended')
unemployment_df = pd.read_snowflake('CovidE2EPipeDatabase.raw_data.unemployment_appended')






