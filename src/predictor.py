from .reader import read_query
from .preprocessor import process_data


def preprocess_and_predict_by_table_name(table_name):
    # Read
    # 'tonusdt.hourly'
    retrieved_rows = read_query(table_name)

    # Preprocess
    df = process_data(retrieved_rows)
    print(df.head())
    return df