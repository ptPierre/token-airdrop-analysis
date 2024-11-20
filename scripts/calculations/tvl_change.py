import sys
import os
import pandas as pd
from datetime import datetime, timedelta


sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from metadata_final import metadata

def calculate_percentage_change(df, start_date_input):
    # Check if start_date_input is already a datetime object
    if isinstance(start_date_input, datetime):
        start_date = start_date_input
    else:
        start_date = datetime.strptime(start_date_input, '%Y-%m-%d')

    # Convert the 'date' column to datetime for comparison
    df['date'] = pd.to_datetime(df['date'])
    
    # Check if start_date is within the DataFrame's date range
    if not ((df['date'] >= start_date).any() and (df['date'] <= start_date).any()):
        # If not, use the earliest date in the DataFrame
        start_date = df['date'].min()
    
    end_date_seven = start_date + timedelta(days=7)
    end_date_thirty = start_date + timedelta(days=30)
    end_date_hundred = start_date + timedelta(days=100)

    
    # Determine which field to use: 'tvl' or 'totalLiquidityUSD'
    if 'tvl' in df.columns:
        field_to_use = 'tvl'
    elif 'totalLiquidityUSD' in df.columns:
        field_to_use = 'totalLiquidityUSD'
    else:
        raise ValueError("Neither 'tvl' nor 'totalLiquidityUSD' fields are present in the DataFrame.")
    
    filtered_df_seven = df[(df['date'] >= start_date) & (df['date'] <= end_date_seven)]
    filtered_df_thirty = df[(df['date'] >= start_date) & (df['date'] <= end_date_thirty)]
    filtered_df_hundred = df[(df['date'] >= start_date) & (df['date'] <= end_date_hundred)]
    
    # Calculate the actual number of days present for each period
    actual_days_seven = (filtered_df_seven['date'].max() - filtered_df_seven['date'].min()).days + 1
    actual_days_thirty = (filtered_df_thirty['date'].max() - filtered_df_thirty['date'].min()).days + 1
    actual_days_hundred = (filtered_df_hundred['date'].max() - filtered_df_hundred['date'].min()).days + 1

    # Calculate percentage change with adjusted periods
    seven_day_pct_change = filtered_df_seven[field_to_use].pct_change(periods=actual_days_seven-1).iloc[-1] * 100
    thirty_day_pct_change = filtered_df_thirty[field_to_use].pct_change(periods=actual_days_thirty-1).iloc[-1] * 100
    hundred_day_pct_change = filtered_df_hundred[field_to_use].pct_change(periods=actual_days_hundred-1).iloc[-1] * 100

    return seven_day_pct_change, thirty_day_pct_change, hundred_day_pct_change



# Dictionary to store the results
percentage_changes = {}


#Looping through csv files dictioary and calling everything
#for csv_file, project in csv_files.items():
for coin, info in metadata.items():
    df = pd.read_csv(f'../../tvl_data/{coin}_tvl.csv')
    start_date_str = info['date']
    print(coin)
    print(start_date_str)
    try:
        change1, change2, change3 = calculate_percentage_change(df, start_date_str)
        percentage_changes[coin] = [change1, change2, change3]
    except Exception as e:
        print(f"Error processing {coin}: {e}")



#Dataframe to csv
df_final = pd.DataFrame([(project, *changes) for project, changes in percentage_changes.items()], 
                        columns=['Project', 'seven_day_tvl', 'thirty_day_tvl', 'hundred_day_tvl'])
df_final.to_csv('../../final_data/tvl_data.csv', index=False)
print(percentage_changes)