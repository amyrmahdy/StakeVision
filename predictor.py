#!./venv/bin/python3.12
import os
import dotenv
import pandas as pd
from reader import read_query
from preprocessor import process_data


if __name__ == '__main__':
    # Read
    retrieved_rows = read_query('tonusdt.hourly')
    
    # Preprocess
    df = process_data(retrieved_rows)
    print(df.head())