-- Create database for covid pipeline project
CREATE DATABASE CovidE2EPipeDatabase;
-- Take the database into use
USE DATABASE CovidE2EPipeDatabase;

-- Create two schemas, one for raw and one for transformed data
CREATE SCHEMA raw_data;
CREATE SCHEMA transformed_data;

-- Take the raw data schema into use
USE SCHEMA raw_data;

-- Create the stage to upload the temporary local raw data csv files and scripts into
CREATE OR REPLACE STAGE daily
    FILE_FORMAT = (TYPE = 'CSV');

-- Create the stage to upload the permanent local raw data csv files and scripts into
CREATE OR REPLACE STAGE permanent
    FILE_FORMAT = (TYPE = 'CSV');

-- Create the daily loaded data tables in raw schema
CREATE OR REPLACE TABLE stocks_eod (
    index NUMBER,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume FLOAT,
    adj_high FLOAT,
    adj_low FLOAT,
    adj_close FLOAT,
    adj_open FLOAT,
    adj_volume FLOAT,
    split_factor FLOAT,
    dividend FLOAT,
    symbol STRING,
    exchange_name STRING,
    curr_date STRING
);

CREATE OR REPLACE TABLE currency_exchanges (
    index NUMBER,
    currency STRING,
    rate FLOAT
);

CREATE OR REPLACE TABLE trade_balance (
    index NUMBER,
    realtime_start DATE,
    realtime_end DATE,
    curr_date DATE,
    value FLOAT
);

CREATE OR REPLACE TABLE unemployment_rate (
    index NUMBER,
    realtime_start DATE,
    realtime_end DATE,
    curr_date DATE,
    value FLOAT
);

CREATE OR REPLACE TABLE US_CPI (
    index NUMBER,
    realtime_start DATE,
    realtime_end DATE,
    curr_date DATE,
    value FLOAT
);

CREATE OR REPLACE TABLE GDP (
    index NUMBER,
    realtime_start DATE,
    realtime_end DATE,
    curr_date DATE,
    value FLOAT
);

CREATE OR REPLACE TABLE thirty_yr_mortgage (
    index NUMBER,
    realtime_start DATE,
    realtime_end DATE,
    curr_date DATE,
    value FLOAT
);

CREATE OR REPLACE TABLE industrial_production (
    index NUMBER,
    realtime_start DATE,
    realtime_end DATE,
    curr_date DATE,
    value FLOAT
);

-- Create the tables for appending daily tables to
CREATE OR REPLACE TABLE stocks_eod_appended (
    index NUMBER,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume FLOAT,
    adj_high FLOAT,
    adj_low FLOAT,
    adj_close FLOAT,
    adj_open FLOAT,
    adj_volume FLOAT,
    split_factor FLOAT,
    dividend FLOAT,
    symbol STRING,
    exchange_name STRING,
    curr_date STRING
);

CREATE OR REPLACE TABLE currency_exchanges_appended (
    index NUMBER,
    currency STRING,
    rate FLOAT
);

CREATE OR REPLACE TABLE trade_balance_appended (
    index NUMBER,
    realtime_start DATE,
    realtime_end DATE,
    curr_date DATE,
    value FLOAT
);

CREATE OR REPLACE TABLE unemployment_rate_appended (
    index NUMBER,
    realtime_start DATE,
    realtime_end DATE,
    curr_date DATE,
    value FLOAT
);

CREATE OR REPLACE TABLE US_CPI_appended (
    index NUMBER,
    realtime_start DATE,
    realtime_end DATE,
    curr_date DATE,
    value FLOAT
);

CREATE OR REPLACE TABLE GDP_appended (
    index NUMBER,
    realtime_start DATE,
    realtime_end DATE,
    curr_date DATE,
    value FLOAT
);

CREATE OR REPLACE TABLE thirty_yr_mortgage_appended (
    index NUMBER,
    realtime_start DATE,
    realtime_end DATE,
    curr_date DATE,
    value FLOAT
);

CREATE OR REPLACE TABLE industrial_production_appended (
    index NUMBER,
    realtime_start DATE,
    realtime_end DATE,
    curr_date DATE,
    value FLOAT
);


-- Now for the transformed schema
-- Take the transformed data schema into use
USE SCHEMA transformed_data;

CREATE OR REPLACE TABLE industrial_production_clean_appended(
    curr_date DATE,
    industrial_production FLOAT
);

CREATE OR REPLACE TABLE thirty_yr_mortgage_clean_appended(
    curr_date DATE,
    thirty_yr_mortgage FLOAT
);

CREATE OR REPLACE TABLE gdp_clean_appended(
    curr_date DATE,
    gdp FLOAT
);

CREATE OR REPLACE TABLE trade_balance_clean_appended(
    curr_date DATE,
    trade_balance FLOAT
);

CREATE OR REPLACE TABLE unemployment_rate_clean_appended(
    curr_date DATE,
    unemployment_rate FLOAT
);

CREATE OR REPLACE TABLE us_cpi_clean_appended(
    curr_date DATE,
    us_cpi FLOAT
);

CREATE OR REPLACE TABLE stocks_eod_clean_appended(
    index NUMBER,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume FLOAT,
    adj_high FLOAT,
    adj_low FLOAT,
    adj_close FLOAT,
    adj_open FLOAT,
    adj_volume FLOAT,
    split_factor FLOAT,
    dividend FLOAT,
    symbol STRING,
    exchange_name STRING,
    curr_date DATE
);

CREATE OR REPLACE TABLE currency_exchanges_clean_appended (
    index NUMBER,
    currency STRING,
    rate FLOAT
);