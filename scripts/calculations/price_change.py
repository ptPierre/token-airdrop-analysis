import sys
import os
import requests
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from metadata_final import metadata

def datetime_to_timestamp(dt):
    """Convert datetime object to timestamp."""
    return int(dt.timestamp())


data = []

# Initialize periods
periods = [7, 30, 100]
period_strings = {7: 'seven', 30: 'thirty', 100: 'hundred'}

for coin, info in metadata.items():
    # In case the first api call doesnt give anything back we still have an empty row in the table
    coin_data = {'Project': coin, 'date': ''}
    for period in periods:
        coin_data[f'{period_strings[period]}_day_price'] = None  # Initialize with None
    try:
        start_date_url = f"https://coins.llama.fi/prices/first/coingecko:{info['coingecko_handle']}"
        print(start_date_url)
        initial_response = requests.get(start_date_url)

        if initial_response.status_code == 200:
            initial_response_json = initial_response.json()
            print(initial_response_json)
            timestamp = initial_response_json['coins'][f"coingecko:{info['coingecko_handle']}"]['timestamp']
            adjusted_date = datetime.fromtimestamp(timestamp) + timedelta(days=1)
            adjusted_timestamp = adjusted_date.timestamp()
            print(timestamp)

            #Initialize coin_data with default values
            coin_data = {'Project': coin, 'date': datetime.fromtimestamp(timestamp)}
            for period in periods:
                coin_data[f'{period_strings[period]}_day_price'] = None  # Initialize with None

            # Fetch data for each period
            for period in periods:
                try:
                    # Construct the request URL
                    url = f'https://coins.llama.fi/percentage/coingecko:{info['coingecko_handle']}?timestamp={adjusted_timestamp}&lookForward=true&period={period}d'
                    print(url)
                    response = requests.get(url)

                    if response.status_code == 200:
                        response_json = response.json()
                    else:
                        print(f"Failed to fetch data for {coin}. Status code: {response.status_code}")
                        continue  # Skip to the next iteration if the response is not OK

                    if 'coins' in response_json:
                        # Assuming the response contains the percentage change for the period
                        percentage_change = response_json['coins'][f"coingecko:{info['coingecko_handle']}"]
                        print(percentage_change)
                        coin_data[f'{period_strings[period]}_day_price'] = float(percentage_change)
                except Exception as e:
                    print(f"Error fetching data for {coin} for period {period}d: {e}")
                    continue  # Continue to the next period if there's an error

        else:
            print(f"Failed to fetch initial data for {coin}. Status code: {initial_response.status_code}")

    except Exception as e:
       print(f"Error fetching data for {coin}: {e}")


    # Append the coin data to the data list even if some queries failed
    data.append(coin_data)

# Convert the data to a DataFrame
df = pd.DataFrame(data)
print(df)




# Save the DataFrame to a CSV file
df.to_csv('../../final_data/price_data.csv', index=False)


