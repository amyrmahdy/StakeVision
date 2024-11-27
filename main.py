#!./venv/bin/python3.12

import os
import time
import ccxt
import dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


# Load environment variables
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

# Environment keys
SINCE_KEY = 'SINCE'
INTERVAL_KEY = 'INTERVAL'
TIMEDELTA_KEY = 'TIMEDELTA'
INFLUX_BUCKET_KEY = 'INFLUX_BUCKET'
INFLUX_ORG_KEY = 'INFLUX_ORG'
INFLUX_TOKEN_KEY = 'INFLUX_TOKEN'
INFLUX_URL_KEY = 'INFLUX_URL'

INFLUX_BUCKET_VALUE = os.getenv(INFLUX_BUCKET_KEY)
INFLUX_ORG_VALUE = os.getenv(INFLUX_ORG_KEY)
INFLUX_TOKEN_VALUE = os.getenv(INFLUX_TOKEN_KEY)
INFLUX_URL_VALUE = os.getenv(INFLUX_URL_KEY)

# Enviroment values
# INTERVAL='60'
# TIMEDELTA='6000'
# SINCE='1732307400000'

# 1732307400000 is 2024-11-23
# 1 minute is plus 60000 milisecond
# 1 hour is plus 3.6e+6  milisecond'

INTERVAL_VALUE = int(os.getenv(INTERVAL_KEY))
TIMEDELTA_VALUE = int(os.getenv(TIMEDELTA_KEY))

# Fetch OHLCV data from the exchange
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

# Update the .env file with the new value of SINCE
def update_env_file(key,value):

    os.environ[key] = str(value)
    dotenv.set_key(dotenv_file, key, os.environ[key])
    return 0


# Write data to InfluxDB
def write_to_influxdb(data):
    """Write candlestick data into InfluxDB."""
    try:
        with InfluxDBClient(url=INFLUX_URL_VALUE,
                            token=INFLUX_TOKEN_VALUE,
                            org=INFLUX_TOKEN_VALUE) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            
            for row in data:
                timestamp_ns = int(row[0] * 1e6)  # Convert to nanoseconds
                open_price, high, low, close, volume = row[1], row[2], row[3], row[4], row[5]
                point = Point('ton_price_data')\
                        .field("open", float(open_price) ) \
                        .field("high", float(high) ) \
                        .field("low", float(low) ) \
                        .field("close", float(close) ) \
                        .field("volume", float(volume) ) \
                        .time(timestamp_ns)
                        
                write_api.write(bucket=INFLUX_BUCKET_VALUE, record=point, org=INFLUX_ORG_VALUE)
                print(f"Written to InfluxDB: {point}")

    except Exception as e:
        print(f"InfluxDB import error: {str(e)}")

# Example usage
if __name__ == "__main__":


    while True:
        SINCE_VALUE = int(os.getenv(SINCE_KEY))
        print(f"SINCE VALUE: {SINCE_VALUE} START")
        print(f"Fetching OHLCV data since: {SINCE_KEY}")
        ohlcv = fetch_ohlcv_data(SINCE_VALUE)
        if ohlcv:
            print("Writing to InfluxDB...")
            write_to_influxdb(ohlcv)
            
            # Update SINCE_KEY to fetch new data next time
            SINCE_VALUE = int(ohlcv[-1][0] + TIMEDELTA_VALUE)
            update_env_file(SINCE_KEY,SINCE_VALUE)    
        else:
            print("No data fetched or an error occurred.")
        print(f"SINCE VALUE: {SINCE_VALUE} FINISH")
        time.sleep(10) # replace with INTERVAL_VALUE
