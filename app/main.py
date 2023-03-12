from fastapi import FastAPI, Query, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import requests
import re
from datetime import datetime, timedelta
import logging
import time

from .config import settings


def str_timestamp_now():
    return str(int(time.time()))


app = FastAPI()
# setup for logging
logging.basicConfig(filename=f"app/logs/{str_timestamp_now()}.log", encoding="utf-8", level=logging.INFO)


def bool_match_regex(text: str, pattern: str):
    return bool(re.match(pattern, text))


def get_weekly_dates(start_date: str, end_date: str, interval: int):
    list_pairs = list()
    start = datetime.strptime(start_date, settings.DATE_FORMAT_DATETIME)
    end = datetime.strptime(end_date, settings.DATE_FORMAT_DATETIME)
    delta = timedelta(days=interval)
    while start <= end:
        pair = (start.strftime(settings.DATE_FORMAT_DATETIME),
                min(end, start + delta - timedelta(days=1)).strftime(settings.DATE_FORMAT_DATETIME))
        start += delta
        list_pairs.append(pair)
    return list_pairs


def get_length_interval_dates(start_date: str, end_date: str):
    start = datetime.strptime(start_date, settings.DATE_FORMAT_DATETIME)
    end = datetime.strptime(end_date, settings.DATE_FORMAT_DATETIME)
    length = end - start
    return length.days


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"detail": "Invalid entry data"})


@app.get("/", status_code=200)
def hello():
    return {"detail": "hello The MAMA AI"}


@app.get("/objects",
         status_code=200,
         description="Fetches near by objects passing around Earth",
         )
def read_nasa(start_date: str = Query(description="Date in YYYY-MM-DD format",
                                      min_length=10,
                                      max_length=10,
                                      regex=settings.DATE_FORMAT_REGEX,
                                      example="2022-11-09"
                                      ),
              end_date: str = Query(description="Date in YYYY-MM-DD format",
                                    min_length=10,
                                    max_length=10,
                                    regex=settings.DATE_FORMAT_REGEX,
                                    example="2022-11-12"
                                    )
              ):
    """
    Fetches near earth objects going around Earth

    :param start_date: string specifying starting date in YYYY-MM-DD format
    :param end_date: string specifying ending date in YYYY-MM-DD format
    :return: sorted by distance from Earth array of  JSON objects
             containing name, estimated diameter, close_approach_data, date
    """
    # final array for all objects
    result = list()

    # check of input dates if they are corresponding to regex
    if not bool_match_regex(start_date, settings.DATE_FORMAT_REGEX) \
            or not bool_match_regex(end_date, settings.DATE_FORMAT_REGEX):
        raise HTTPException(status_code=400, detail="Incorrect format of dates")
    logging.info("Dates passed regex.")

    # array for tuples of 7-day intervals
    date_intervals = list()

    # test if start date is before end date
    if get_length_interval_dates(start_date, end_date) < 0:
        raise HTTPException(status_code=400, detail="End date is before start date")

    # check if interval is longer than 7-day
    if get_length_interval_dates(start_date, end_date) > settings.DAYS_LIMIT:
        date_intervals = get_weekly_dates(start_date, end_date, interval=settings.DAYS_LIMIT)
    else:
        date_intervals.append((start_date, end_date))
    for new_start_date, new_end_date in date_intervals:
        payload = {"start_date": new_start_date, "end_date": new_end_date, "api_key": settings.API_KEY}
        response = requests.get(f"{settings.BASE_URL}/feed", params=payload).json()

        try:
            near_earth_objects = response["near_earth_objects"]
            logging.info("Near earth objects found.")
        except KeyError:
            raise HTTPException(status_code=404, detail="Item not found")

        neo_items = near_earth_objects.items()

        # creates array of objects
        neo_items = [
            {
                **{
                    key: value[0] if isinstance(value, list) and len(value) == 1 else value
                    for key, value in neo.items()
                    if key in settings.LF_ATTRIBUTES
                },
                'date': date  # adds date to other keys
            }
            for date, neos in neo_items
            for neo in neos
        ]

        # add neo items to final array
        result.extend(neo_items)

    # sort items by distance
    try:
        def key_distance(x):
            return x['close_approach_data']['miss_distance']['astronomical']

        result.sort(key=key_distance, reverse=False)
    except KeyError:
        raise HTTPException(status_code=404, detail="Item not found")

    return JSONResponse(status_code=200, content=result)
