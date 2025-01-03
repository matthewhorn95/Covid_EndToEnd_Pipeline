import requests
import pandas as pd
from datetime import datetime

stocks_api_url='https://api.marketstack.com/v1/eod?access_key=504c213ca813a3190453dcb7d01f8fa9'
exchange_api_url='https://v6.exchangerate-api.com/v6/b9730323a7db7547d1b3373a/latest/USD'
fred_series_url='https://api.stlouisfed.org/fred/series/observations?series_id='
fred_key = '&api_key=899cb2d2478ca9440d6c531e394e7053&file_type=json'
query_string = {"symbols":"AAPL"}

def api_to_csv(url, output_filename, custom_process, query_string={}):
    
    try:
        # Make the API request
        response = requests.get(url, params=query_string) if query_string else requests.get(url)

        # Handle non-success statuses, print response code to console and return
        if response.status_code != 200:
            print(f"Error: Response status {response.status_code}")
            print(f"Response content: {response.text}")
            return
        
        # Get the json response as a dict
        json_res = response.json()

        # Call the custom function param to process json res specific to each api
        data = custom_process(json_res)
        # Convert to Pandas dataframe
        df = pd.DataFrame(data)
        # Designate output file path and save to CSV
        output_path = f'/Users/matthewmac/airflow/data/raw/{output_filename}_{datetime.now().date()}.csv'
        print(f'{output_filename} data was saved to {output_path}')
        df.to_csv(output_path)
        print(df.head())

    # Handle basic exceptions and print errors to console
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the API request: {e}")
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# For conversion rates (where the data is a dictionary of currencies and rates)
def process_conversion_rates(json_res):
    # Extract the data field (conversion rates)
    data = json_res.get('conversion_rates')
    return [{"currency": key, "rate": value} for key, value in data.items()]

# For stock exchange data (assuming it's a list of records)
def process_stock_data(json_res):
    return json_res.get('data')  # Just return it as is if it's already in list format

def process_fred_observations(json_res):
    return json_res.get('observations')

# Make calls to the api_to_csv function for each api
api_to_csv(stocks_api_url, 'stocks_eod', process_stock_data, query_string)
api_to_csv(exchange_api_url, 'exchanges', process_conversion_rates)
api_to_csv(f"{fred_series_url}MORTGAGE30US{fred_key}", '30yr_mortage', process_fred_observations)
api_to_csv(f"{fred_series_url}UNRATE{fred_key}", 'unemployment_rate', process_fred_observations)
api_to_csv(f"{fred_series_url}GDP{fred_key}", 'GDP', process_fred_observations)
api_to_csv(f"{fred_series_url}CPIAUCSL{fred_key}", 'US_CPI', process_fred_observations)
api_to_csv(f"{fred_series_url}NETEXP{fred_key}", 'trade_balance', process_fred_observations)
api_to_csv(f"{fred_series_url}INDPRO{fred_key}", 'industrial_production', process_fred_observations)
