import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

stocks_api_url=f'https://api.marketstack.com/v1/eod?access_key={os.getenv("stocks_key")}'
exchange_api_url=f'https://v6.exchangerate-api.com/v6/{os.getenv("exchange_key")}/latest/USD'
fred_series_url='https://api.stlouisfed.org/fred/series/observations?series_id='
fred_ending = f'&api_key={os.getenv("fred_key")}&file_type=json'
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

def main():
    # Make calls to the api_to_csv function for each api
    api_to_csv(stocks_api_url, 'stocks_eod', process_stock_data, query_string)
    api_to_csv(exchange_api_url, 'exchanges', process_conversion_rates)
    api_to_csv(f"{fred_series_url}MORTGAGE30US{fred_ending}", '30yr_mortage', process_fred_observations)
    api_to_csv(f"{fred_series_url}UNRATE{fred_ending}", 'unemployment_rate', process_fred_observations)
    api_to_csv(f"{fred_series_url}GDP{fred_ending}", 'GDP', process_fred_observations)
    api_to_csv(f"{fred_series_url}CPIAUCSL{fred_ending}", 'US_CPI', process_fred_observations)
    api_to_csv(f"{fred_series_url}NETEXP{fred_ending}", 'trade_balance', process_fred_observations)
    api_to_csv(f"{fred_series_url}INDPRO{fred_ending}", 'industrial_production', process_fred_observations)

