from fastapi import FastAPI
from pydantic import BaseModel
from src.fetcher_writer import fetch_write_by_date


class WriteRequest(BaseModel):
    since: str
    # timeframe: float | None = None

app = FastAPI()


@app.post('/fetch_and_write/')
async def fetch_and_write(write_request: WriteRequest):
    number_of_affected_rows = fetch_write_by_date(write_request.since)
    return {"result" : f"{number_of_affected_rows} rows were affected."}
