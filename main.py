from fastapi import FastAPI
from pydantic import BaseModel
from src.fetcher_writer import fetch_write_by_date
from src.predictor import preprocess_and_predict_by_table_name

class WriteRequest(BaseModel):
    since: str
    # timeframe: float | None = None

class ReadRequest(BaseModel):
    table_name: str
    # timeframe: float | None = None


app = FastAPI()


@app.post('/fetch_and_write/')
async def fetch_and_write(write_request: WriteRequest):
    number_of_affected_rows = fetch_write_by_date(write_request.since)
    return {"result" : f"{number_of_affected_rows} rows were affected."}



@app.post('/preprocess_and_predict/')
async def preprocess_and_predict(read_request: ReadRequest):
    dataframe = preprocess_and_predict_by_table_name(read_request.table_name)
    return {"result" : f"{dataframe}"}
