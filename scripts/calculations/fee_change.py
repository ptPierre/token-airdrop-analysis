import sys
import os
import pandas as pd
from datetime import datetime, timedelta


sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
# List of CSV files and their corresponding project names
from config import csv_files
from metadata_small import metadata

def calculate_percentage_change(df, start_date_input):
    # Check if start_date_input is already a datetime object
    if isinstance(start_date_input, datetime):
        start_date = start_date_input
    else:
        start_date = datetime.strptime(start_date_input, '%Y-%m-%d')
    
    end_date_seven = start_date + timedelta(days=7)
    end_date_thirty = start_date + timedelta(days=30)
    end_date_hundred = start_date + timedelta(days=100)
    
    # Convert the 'date' column to datetime for comparison
    df['date'] = pd.to_datetime(df['date'])
    
    # Determine which field to use: 'tvl' or 'totalLiquidityUSD'
    field_to_use = 'fee'
    
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
    file_path = f'../../fee_data/{coin}_fee.csv'
    # Check if the file exists before attempting to read it
    if not os.path.exists(file_path):
        print(f"File not found for {coin}, skipping...")
        continue  # Skip to the next iteration if the file does not exist

    df = pd.read_csv(file_path)
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
                        columns=['Project', 'seven_day_fee', 'thirty_day_fee', 'hundred_day_fee'])
df_final.to_csv('../../final_data/fee_data.csv', index=False)
print(percentage_changes)