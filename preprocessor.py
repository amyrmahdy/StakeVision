import pandas as pd
from datetime import timedelta


def process_data(retrieved_rows):
    # to DataFrame
    df = pd.DataFrame(retrieved_rows, columns = ['epoch','open','high','low','close','volume'])

    df['date'] = pd.to_datetime(df['epoch'],unit = 'ms')
    df['date'] = df['date'] + timedelta(hours = 3, minutes = 30)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['second'] = df['date'].dt.second                
    # df.drop(['date','epoch','second'], axis = 1, inplace = True)
    return df


