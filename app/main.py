from typing import Union

from fastapi import FastAPI
import requests

from pydantic import BaseModel

app = FastAPI()

BASE_URL = "https://api.nasa.gov/neo/rest/v1"



@app.get("/objects")
def read_nasa(start_date: str, end_date: str):
    payload = {"start_date": start_date, "end_date": end_date, "api_key": API_KEY}
    response = requests.get(f"{BASE_URL}/feed", params=payload).json()
    return response
