import requests
import pandas as pd
from datetime import datetime
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from metadata_small import metadata

baseUrl = 'https://api.llama.fi'

for coin, info in metadata.items():
    try:
        print(baseUrl + f"/summary/fees/{coin}?dataType=dailyFees")
        fee = requests.get(baseUrl + f"/summary/fees/{coin}?dataType=dailyFees")
        print(fee)

        # Check if the request was successful
        if fee.status_code != 200:
            print(f"Request for {coin} failed with status code: {fee.status_code}")
            continue  # Skip to the next iteration

        json = fee.json()

        df = pd.DataFrame.from_dict(json['totalDataChart'])
        df.columns = ['date', 'fee']

        # Uncomment if you need to convert timestamps to datetime
        df['date'] = df['date'].apply(lambda x: datetime.fromtimestamp(x))

        df.to_csv(f"../../fee_data/{coin}_fee.csv")
    except requests.exceptions.RequestException as e:
        print(f"Request error for {coin}: {e}")
    except ValueError as e:
        print(f"JSON decoding error for {coin}: {e}")
    except Exception as e:
        print(f"Unexpected error for {coin}: {e}")
    
    