#!./venv/bin/python3.12
import ccxt
import pandas as pd
from datetime import datetime, timedelta
import time
import os

def fetch_and_append_ohlcv_data(symbol='TON/USDT', timeframe='1h', 
                                 start_time=None, 
                                 exchange_id='kucoin', 
                                 output_file='ton_usdt_incremental.csv'):
    """
    Fetch OHLCV data incrementally and append to CSV file.
    
    Parameters:
    symbol (str): Trading pair symbol
    timeframe (str): Candle timeframe
    start_time (datetime): Starting time for data collection
    exchange_id (str): Exchange to use
    output_file (str): Path to output CSV file
    """
    try:
        # Initialize exchange
        exchange_class = getattr(ccxt, exchange_id)
        exchange = exchange_class({
            'enableRateLimit': True,
        })
        
        # Determine start time
        if start_time is None:
            start_time = datetime.now() - timedelta(days=7)
        
        # Check if file exists, if not create it
        if not os.path.exists(output_file):
            # Create initial empty DataFrame
            initial_df = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            initial_df.to_csv(output_file, index=False)
        
        # Read existing data
        existing_data = pd.read_csv(output_file, parse_dates=['timestamp'])
        
        # Determine last timestamp (if any)
        if not existing_data.empty:
            last_timestamp = existing_data['timestamp'].max()
            start_time = max(start_time, last_timestamp)
        
        # Fetch new data
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, 
                                     since=int(start_time.timestamp() * 1000))
        
        # Convert to DataFrame
        if ohlcv:
            new_df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            new_df['timestamp'] = pd.to_datetime(new_df['timestamp'], unit='ms')
            
            # Remove duplicates and append
            combined_df = pd.concat([existing_data, new_df]).drop_duplicates(subset='timestamp')
            combined_df.sort_values('timestamp', inplace=True)
            
            # Save to CSV
            combined_df.to_csv(output_file, index=False)
            
            print(f"Data appended. New records: {len(new_df)}")
        else:
            print("No new data found.")
    
    except Exception as e:
        print(f"Error collecting data: {str(e)}")

def continuous_data_collection(symbol='TON/USDT', 
                                timeframe='1h', 
                                start_time=None, 
                                exchange_id='kucoin', 
                                interval=3600):  # Default 1 hour
    """
    Continuously collect data at specified intervals.
    
    Parameters:
    interval (int): Seconds between data collection attempts
    """
    year = 2024
    month = 11
    day = 23
    if start_time is None:
        start_time = datetime(year, month, day)
    
    while True:
        fetch_and_append_ohlcv_data(symbol, timeframe, start_time, exchange_id)
        time.sleep(interval)

# Example usage
if __name__ == "__main__":
    continuous_data_collection()
