#!./venv/bin/python3.12
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
from fetcher import fetch_ohlcv_data


SINCE_USER = sys.argv[1]
SINCE_USER_LIST = [int(i) for i in SINCE_USER.split('-')]
SINCE_YEAR = SINCE_USER_LIST[0]
SINCE_MONTH = SINCE_USER_LIST[1]
SINCE_DAY = SINCE_USER_LIST[2]
SINCE_HOUR = 0
SINCE_MINUTE = 0
SINCE_SECOND = 0


since = int(datetime(SINCE_YEAR,SINCE_MONTH,
                     SINCE_DAY,SINCE_HOUR,
                     SINCE_MINUTE,SINCE_SECOND 
                     ).timestamp() * 1000)
                    # tzinfo=ZoneInfo('Europe/London')

res = fetch_ohlcv_data(since, symbol='TON/USDT', timeframe='1h', limit=20, exchange_id='kucoin')
print(res)
