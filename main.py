#!./venv/bin/python3.12

import os
import time
import ccxt
import dotenv
from datetime import datetime
from zoneinfo import ZoneInfo
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS



# Load environment variables
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file, override=True)

# Environment keys
SINCE_YEAR_KEY = 'SINCE_YEAR'
SINCE_MONTH_KEY = 'SINCE_MONTH'
SINCE_DAY_KEY = 'SINCE_DAY'
SINCE_HOUR_KEY = 'SINCE_HOUR'
SINCE_MINUTES_KEY = 'SINCE_MINUTES'
SINCE_SECONDS_KEY = 'SINCE_SECONDS'
SINCE_KEY = 'SINCE'
INTERVAL_KEY = 'INTERVAL'
TIMEDELTA_KEY = 'TIMEDELTA'
TIMEZONE_KEY = 'TIMEZONE'
INFLUX_BUCKET_KEY = 'INFLUX_BUCKET'
INFLUX_ORG_KEY = 'INFLUX_ORG'
INFLUX_TOKEN_KEY = 'INFLUX_TOKEN'
INFLUX_URL_KEY = 'INFLUX_URL'



SINCE_YEAR = int(os.getenv(SINCE_YEAR_KEY))
SINCE_MONTH = int(os.getenv(SINCE_MONTH_KEY))
SINCE_DAY = int(os.getenv(SINCE_DAY_KEY))
SINCE_HOUR = int(os.getenv(SINCE_HOUR_KEY))
SINCE_MINUTES = int(os.getenv(SINCE_MINUTES_KEY))
SINCE_SECONDS = int(os.getenv(SINCE_SECONDS_KEY))
INTERVAL = int(os.getenv(INTERVAL_KEY))
TIMEDELTA = int(os.getenv(TIMEDELTA_KEY))
INFLUX_BUCKET = os.getenv(INFLUX_BUCKET_KEY)
INFLUX_ORG = os.getenv(INFLUX_ORG_KEY)
INFLUX_TOKEN = os.getenv(INFLUX_TOKEN_KEY)
INFLUX_URL = os.getenv(INFLUX_URL_KEY)

# Enviroment values
# INTERVAL='60'
# TIMEDELTA='6000'
# SINCE='1732307400000'

# 1732307400000 is 2024-11-23
# 1 minute is plus 60000 milisecond
# 1 hour is plus 3.6e+6  milisecond'




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
        with InfluxDBClient(url=INFLUX_URL,
                            token=INFLUX_TOKEN,
                            org=INFLUX_TOKEN) as client:
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
                        
                write_api.write(bucket=INFLUX_BUCKET, record=point, org=INFLUX_ORG)
                print(f"Written to InfluxDB: {point}")

    except Exception as e:
        print(f"InfluxDB import error: {str(e)}")

# Example usage
if __name__ == "__main__":

    # Initiate Date if SINCE value is equal to ZERO
    SINCE = int(os.getenv(SINCE_KEY))
    if not SINCE:
        since_timestamp = int(datetime(SINCE_YEAR,SINCE_MONTH,SINCE_DAY,SINCE_HOUR,SINCE_MINUTES,SINCE_SECONDS,
                                    tzinfo=ZoneInfo('Europe/London')).timestamp() * 1000)
        update_env_file(SINCE_KEY,since_timestamp)    

    while True:
        SINCE = int(os.getenv(SINCE_KEY))
        print(f"SINCE VALUE: {SINCE} START")
        print(f"Fetching OHLCV data since: {SINCE_KEY}")
        ohlcv = fetch_ohlcv_data(SINCE)
        if ohlcv:
            print("Writing to InfluxDB...")
            write_to_influxdb(ohlcv)
            
            # Update SINCE_KEY to fetch new data next time
            SINCE = int(ohlcv[-1][0] + TIMEDELTA)
            update_env_file(SINCE_KEY,SINCE)    
        else:
            print("No data fetched or an error occurred.")
        print(f"SINCE VALUE: {SINCE} FINISH")
        time.sleep(10) # replace with INTERVAL
