import os
import sys
import dotenv
from datetime import datetime
from writer import insert_query
from fetcher import fetch_ohlcv_data



since_user = sys.argv[1]
since_user_list = [int(i) for i in since_user.split('-')]
since_year = since_user_list[0]
since_month = since_user_list[1]
since_day = since_user_list[2]

since = int(datetime(since_year,since_month,since_day 
                     ).timestamp() * 1000)


symbol = 'TON/USDT'
timeframe = '1h'
limit_fetcher = 20
exchange_id = 'kucoin'
ohlcv_data = fetch_ohlcv_data(since, symbol=symbol, timeframe=timeframe, limit=limit_fetcher, exchange_id=exchange_id)

ohlcv_data_tup_str = [str(tuple(row)) for row in ohlcv_data]
ohlcv_data_all_in_one = ','.join(ohlcv_data_tup_str)


target_table = 'tonusdt.hourly'
insert_query(table_name= target_table, values=ohlcv_data_all_in_one)
