COPY INTO CovidE2EPipeDatabase.raw_data.industrial_production
    FROM @CovidE2EPipeDatabase.raw_data.raw_data_stage/industrial_production_2025_01_09.csv
    FILE_FORMAT = ( TYPE='CSV' )
    ON_ERROR = 'CONTINUE';

    COPY INTO CovidE2EPipeDatabase.raw_data.stocks_eod
    FROM @CovidE2EPipeDatabase.raw_data.raw_data_stage/stocks_eod_2025_01_09.csv
    FILE_FORMAT = ( TYPE='CSV' )
    ON_ERROR = 'CONTINUE';

    COPY INTO CovidE2EPipeDatabase.raw_data.currency_exchanges
    FROM @CovidE2EPipeDatabase.raw_data.raw_data_stage/currency_exchanges_2025_01_09.csv
    FILE_FORMAT = ( TYPE='CSV' )
    ON_ERROR = 'CONTINUE';

    COPY INTO CovidE2EPipeDatabase.raw_data.gdp
    FROM @CovidE2EPipeDatabase.raw_data.raw_data_stage/gdp_2025_01_09.csv
    FILE_FORMAT = ( TYPE='CSV' )
    ON_ERROR = 'CONTINUE';

    COPY INTO CovidE2EPipeDatabase.raw_data.us_cpi
    FROM @CovidE2EPipeDatabase.raw_data.raw_data_stage/us_cpi_2025_01_09.csv
    FILE_FORMAT = ( TYPE='CSV' )
    ON_ERROR = 'CONTINUE';

    COPY INTO CovidE2EPipeDatabase.raw_data.unemployment_rate
    FROM @CovidE2EPipeDatabase.raw_data.raw_data_stage/unemployment_rate_2025_01_09.csv
    FILE_FORMAT = ( TYPE='CSV' )
    ON_ERROR = 'CONTINUE';

    COPY INTO CovidE2EPipeDatabase.raw_data.thirty_yr_mortgage
    FROM @CovidE2EPipeDatabase.raw_data.raw_data_stage/thirty_yr_mortage_2025_01_09.csv
    FILE_FORMAT = ( TYPE='CSV' )
    ON_ERROR = 'CONTINUE';

    COPY INTO CovidE2EPipeDatabase.raw_data.trade_balance
    FROM @CovidE2EPipeDatabase.raw_data.raw_data_stage/trade_balance_2025_01_09.csv
    FILE_FORMAT = ( TYPE='CSV' )
    ON_ERROR = 'CONTINUE';
