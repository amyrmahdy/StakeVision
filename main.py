from fastapi import FastAPI
from pydantic import BaseModel
from src.fetcher_writer import fetch_write_by_date


class Since(BaseModel):
    since_user: str
    # timeframe: float | None = None

app = FastAPI()


@app.post('/fetch_and_write/')
def fetch_and_write(since: Since):
    result = fetch_write_by_date(since.since_user)
    return result
