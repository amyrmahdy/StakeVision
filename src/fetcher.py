import os
import sys
import time
import ccxt
import dotenv
from datetime import datetime
from zoneinfo import ZoneInfo


# Fetch OHLCV data from the exchange
def fetch_ohlcv_data(since, symbol='TON/USDT', timeframe='1h', limit=10, exchange_id='kucoin'):
    """Fetch OHLCV data from specified exchange."""
    try:
        exchange_class = getattr(ccxt, exchange_id)
        exchange = exchange_class({'enableRateLimit': True})
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
        return ohlcv
    
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return None


# if ohlcv:
#     print("Writing to InfluxDB...")
#     write_to_influxdb(ohlcv)
    
#     # Update SINCE_KEY to fetch new data next time
#     SINCE = int(ohlcv[-1][0] + TIMEDELTA)
#     update_env_file(SINCE_KEY,SINCE)    
# else:
#     print("No data fetched or an error occurred.")


