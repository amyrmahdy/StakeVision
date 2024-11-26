#!./venv/bin/python3.12

import os
import time
import dotenv
import pandas as pd
import ccxt
from datetime import datetime



def fetch_ohlcv_data(since, symbol='TON/USDT', timeframe='1m', limit=10, exchange_id='kucoin'):
    """Fetch OHLCV data from specified exchange."""
    try:
        exchange_class = getattr(ccxt, exchange_id)
        exchange = exchange_class({'enableRateLimit': True})
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
        return ohlcv
    
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return None


def update_env_file(key,value):

    os.environ[key] = str(value)
    dotenv.set_key(dotenv_file, key, os.environ[key])
    return 0


def convert_to_dataframe(data):
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    return df



# Example usage
if __name__ == "__main__":
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    
    since_key = 'SINCE'
    interval_key = 'INTERVAL'
    timedelta_key = 'TIMEDELTA'
    # 1732307400000 is 2024-11-23
    # 1 minute is plus 60000 milisecond
    # 1 hour is plus 3.6e+6  milisecond'

    interval_value = int(os.getenv(interval_key))
    timedelta_value = int(os.getenv(timedelta_key))

    # Convert to DataFrame with timestamp as index


    while True:
        since_value = int(os.getenv(since_key))
        print(since_value)
        print("fetch_and_append_ohlcv_data")
        ohlcv = fetch_ohlcv_data(since_value)
        df = convert_to_dataframe(ohlcv)
        print(df)
        # Update since_value for continuously fetching
        since_value = int(ohlcv[-1][0] + timedelta_value)
        update_env_file(since_key,since_value)    
        print(since_value)
        print("import_to_influxdb")
        # import_to_influxdb()

        time.sleep(10) # replace with interval_value
