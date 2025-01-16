import sys
from src.fetcher_writer import fetch_write_by_date


if __name__ == '__main__':
    since_user = sys.argv[1]
    fetch_write_by_date(since_user)
