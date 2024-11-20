import requests
from datetime import datetime
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from metadata_final import metadata


def get_supply_details(handle):
    url = f"https://pro-api.coingecko.com/api/v3/coins/{handle}"
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        max_supply = data.get('market_data', {}).get('max_supply')
        total_supply = data.get('market_data', {}).get('total_supply')
        return max_supply, total_supply
    else:
        print(f"Failed to fetch data for {handle}")
        return None, None

for key, value in metadata.items():
    max_supply, total_supply = get_supply_details(value['coingecko_handle'])
    alloc_size = value['alloc_size']

    if max_supply is not None and max_supply > 0:
        alloc_size_pct = (alloc_size / max_supply) * 100
    elif total_supply is not None and total_supply > 0:
        alloc_size_pct = (alloc_size / total_supply) * 100
    else:
        alloc_size_pct = None

    print(f"{key}: Allocation size as percentage of supply = {alloc_size_pct}%")

# Note: This script does not handle errors comprehensively and assumes the API returns well-formed JSON in expected structure.
