COPY INTO CovidE2EPipeDatabase.raw_data.industrial_production
    FROM @CovidE2EPipeDatabase.raw_data.raw_data_stage
    FILES = ('/Users/matthewmac/airflow/data/raw/industrial_production_2025-01-04.csv')
    FILE_FORMAT = ( TYPE='CSV' )
    ON_ERROR = 'CONTINUE';
    
