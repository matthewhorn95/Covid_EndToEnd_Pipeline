INSERT INTO CovidE2EPipeDatabase.raw_data.industrial_production_appended
    SELECT * FROM CovidE2EPipeDatabase.raw_data.industrial_production b
    WHERE NOT EXISTS(
        SELECT 1
        FROM CovidE2EPipeDatabase.raw_data.industrial_production_appended a
        WHERE a.curr_date = b.curr_date
    );

INSERT INTO CovidE2EPipeDatabase.raw_data.stocks_eod_appended
    SELECT * FROM CovidE2EPipeDatabase.raw_data.stocks_eod b
    WHERE NOT EXISTS(
        SELECT 1
        FROM CovidE2EPipeDatabase.raw_data.stocks_eod_appended a
        WHERE ROW(a.index, a.open, a.high, a.low, a.close, a.volume, a.adj_high, a.adj_low, a.adj_close, a.adj_open, a.adj_volume, a.split_factor, a.dividend, a.symbol, a.exchange_name, a.curr_date) = ROW(b.index, b.open, b.high, b.low, b.close, b.volume, b.adj_high, b.adj_low, b.adj_close, b.adj_open, b.adj_volume, b.split_factor, b.dividend, b.symbol, b.exchange_name, b.curr_date)
    );

INSERT INTO CovidE2EPipeDatabase.raw_data.gdp_appended
    SELECT * FROM CovidE2EPipeDatabase.raw_data.gdp b
    WHERE NOT EXISTS(
        SELECT 1
        FROM CovidE2EPipeDatabase.raw_data.gdp_appended a
        WHERE a.curr_date = b.curr_date
    );

INSERT INTO CovidE2EPipeDatabase.raw_data.thirty_yr_mortgage_appended
    SELECT * FROM CovidE2EPipeDatabase.raw_data.thirty_yr_mortgage b
    WHERE NOT EXISTS(
        SELECT 1
        FROM CovidE2EPipeDatabase.raw_data.thirty_yr_mortgage_appended a
        WHERE a.curr_date = b.curr_date
    );

INSERT INTO CovidE2EPipeDatabase.raw_data.unemployment_rate_appended
    SELECT * FROM CovidE2EPipeDatabase.raw_data.unemployment_rate b
    WHERE NOT EXISTS(
        SELECT 1
        FROM CovidE2EPipeDatabase.raw_data.unemployment_rate_appended a
        WHERE a.curr_date = b.curr_date
    );

INSERT INTO CovidE2EPipeDatabase.raw_data.trade_balance_appended
    SELECT * FROM CovidE2EPipeDatabase.raw_data.trade_balance b
    WHERE NOT EXISTS(
        SELECT 1
        FROM CovidE2EPipeDatabase.raw_data.trade_balance_appended a
        WHERE a.curr_date = b.curr_date
    );

INSERT INTO CovidE2EPipeDatabase.raw_data.us_cpi_appended
    SELECT * FROM CovidE2EPipeDatabase.raw_data.us_cpi b
    WHERE NOT EXISTS(
        SELECT 1
        FROM CovidE2EPipeDatabase.raw_data.us_cpi_appended a
        WHERE a.curr_date = b.curr_date
    );

INSERT INTO CovidE2EPipeDatabase.raw_data.currency_exchanges_appended
    SELECT * FROM CovidE2EPipeDatabase.raw_data.currency_exchanges b
    WHERE NOT EXISTS(
        SELECT 1
        FROM CovidE2EPipeDatabase.raw_data.currency_exchanges_appended a
        WHERE ROW(a.index, a.currency, a.rate) = ROW(b.index, b.currency, b.rate)
    );