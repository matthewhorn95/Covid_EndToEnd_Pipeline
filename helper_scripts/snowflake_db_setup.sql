-- Create database for covid pipeline project
CREATE DATABASE CovidE2EPipeDatabase;
-- Take the database into use
USE DATABASE CovidE2EPipeDatabase;

-- Create two schemas, one for raw and one for transformed data
CREATE SCHEMA raw_data;
CREATE SCHEMA transformed_data;

-- Take the raw data schema into use
USE SCHEMA raw_data;
-- Create the tables in raw schema
CREATE TABLE IF NOT EXISTS stocks_eod (
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
    exchange STRING,
    "date" STRING
);

CREATE TABLE IF NOT EXISTS currency_exchanges (
    currency STRING,
    rate FLOAT
);

CREATE TABLE IF NOT EXISTS trade_balance (
    realtime_start DATE,
    realtime_end DATE,
    date DATE,
    value FLOAT
);

CREATE TABLE IF NOT EXISTS unemployment_rate (
    realtime_start DATE,
    realtime_end DATE,
    date DATE,
    value FLOAT
);

CREATE TABLE IF NOT EXISTS US_CPI (
    realtime_start DATE,
    realtime_end DATE,
    date DATE,
    value FLOAT
);

CREATE TABLE IF NOT EXISTS GDP (
    realtime_start DATE,
    realtime_end DATE,
    date DATE,
    value FLOAT
);

CREATE TABLE IF NOT EXISTS thirty_yr_mortgage (
    realtime_start DATE,
    realtime_end DATE,
    date DATE,
    value FLOAT
);

CREATE TABLE IF NOT EXISTS industrial_production (
    realtime_start DATE,
    realtime_end DATE,
    date DATE,
    value FLOAT
);





















