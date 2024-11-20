import requests
import pandas as pd
from datetime import datetime
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from metadata_final import metadata

baseUrl = 'https://api.llama.fi'

for coin, info in metadata.items():

    print(info['type'])

    if info['type'] == 'chain':
        type = 'historicalChainTvl'
        pre = 'v2/'
    else:
        type = 'protocol'
        pre = ''

    print(baseUrl + f"/{pre}{type}/{coin}")
    #https://api.llama.fi/v2/historicalChainTvl/arbitrum
    tvl = requests.get(baseUrl + f"/{pre}{type}/{coin}")
    print(tvl.status_code)
    if tvl.status_code != 200:
            print(f"Request for {coin} failed with status code: {tvl.status_code}")
            continue  # Skip to the next iteration
    print(tvl)

    json = tvl.json()

    if info['type'] == 'chain':
        print("we are in chain")
        df = pd.DataFrame.from_dict(json)
    else:
        print("we are in protocol")
        df = pd.DataFrame.from_dict(json['tvl'])


    df['date'] = df['date'].apply(lambda x:  datetime.fromtimestamp(x))

    df.to_csv(f"../../tvl_data/{coin}_tvl.csv")