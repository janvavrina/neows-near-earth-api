from typing import Union

from fastapi import FastAPI, Query, HTTPException
import requests
import re
import logging

from app import settings

app = FastAPI()


def bool_match_regex(text: str, pattern: str):
    return bool(re.match(text, pattern))


@app.get("/", status_code=200)
def hello():
    return {"output": "hello The MAMA AI"}


@app.get("/objects", status_code=200)
def read_nasa(start_date: str | None = Query(default="2022-11-09",
                                             min_length=10,
                                             max_length=10,
                                             regex=settings.DATE_FORMAT_REGEX),
              end_date: str | None = Query(default="2022-11-11",
                                           min_length=10,
                                           max_length=10,
                                           regex=settings.DATE_FORMAT_REGEX)
              ):
    """

    :param start_date: string specifying starting date in YYYY-MM-DD format
    :param end_date: string specifying ending date in YYYY-MM-DD format
    :return: array of  JSON objects containing name, estimated diameter, close_approach_data
    """
    if bool_match_regex(start_date, settings.DATE_FORMAT_REGEX) \
            or bool_match_regex(end_date, settings.DATE_FORMAT_REGEX):
        raise HTTPException(status_code=403, detail="Incorrect format of dates")

    payload = {"start_date": start_date, "end_date": end_date, "api_key": settings.API_KEY}
    response = requests.get(f"{settings.BASE_URL}/feed", params=payload).json()

    try:
        near_earth_objects = response["near_earth_objects"]
    except KeyError:
        raise HTTPException(status_code=404, detail="Item not found")
    if near_earth_objects:
        neo_items = near_earth_objects.items()
        neo_items = [
            {
                date:
                    [
                        {
                            key: value[0] if isinstance(value, list) and len(value) == 1 else value
                            for key, value in neo.items()
                            if key in {'name', 'estimated_diameter', 'close_approach_data'}
                        }
                        for neo in neos
                    ]
            }
            for date, neos in neo_items
        ]

        # TODO sort items by distance
        # if lambda x: len(x.get('close_approach_data')) == 1:
        #     neo_items.sort(key=lambda x: (x.get('close_approach_data')[0]
        #                                   .get('miss_distance')
        #                                   .get('astronomical')
        #                                   ),
        #                    reverse=False)
    return neo_items
