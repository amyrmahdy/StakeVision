#!./venv/bin/python3.12
import sys
from datetime import datetime
from fetcher import fetch_ohlcv_data

since_user = sys.argv[1]
since_user_list = [int(i) for i in since_user.split('-')]
since_year = since_user_list[0]
since_month = since_user_list[1]
since_day = since_user_list[2]

since = int(datetime(since_year,since_month,since_day 
                     ).timestamp() * 1000)


res = fetch_ohlcv_data(since, symbol='TON/USDT', timeframe='1h', limit=20, exchange_id='kucoin')
print(res)
