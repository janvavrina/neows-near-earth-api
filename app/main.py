from typing import Union

from fastapi import FastAPI, Query, HTTPException
import requests

from pydantic import BaseModel

from app import settings

app = FastAPI()


# class RangeIn(BaseModel):
#     start_date: str
#     end_date: str
#     api_key: str = API_KEY


# class ObjectsOut(BaseModel):


@app.get("/objects")
def read_nasa(start_date: str | None = Query(default="2022-11-09",
                                             min_length=10,
                                             max_length=10,
                                             regex=settings.DATE_FORMAT_REGEX),
              end_date: str | None = Query(default="2022-11-11",
                                           min_length=10,
                                           max_length=10,
                                           regex=settings.DATE_FORMAT_REGEX)
              ):
    payload = {"start_date": start_date, "end_date": end_date, "api_key": settings.API_KEY}
    response = requests.get(f"{settings.BASE_URL}/feed", params=payload).json()
    dict_res = dict(response)
    try:
        near_earth_objects = dict_res["near_earth_objects"]
    except KeyError:
        raise HTTPException(status_code=404, detail="Item not found")
    if near_earth_objects:
        items = near_earth_objects.items()
        # TODO sort by closest approach
        items = [
            {
                key: value
                for attribute in attributes
                for key, value in attribute.items()
                if key in {'name', 'estimated_diameter', 'close_approach_data'}
            }
            for date, attributes in items
        ]
    return items
