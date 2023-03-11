from pydantic import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "API"

    BASE_URL = "https://api.nasa.gov/neo/rest/v1"
    # if the limit range of days changes
    DAYS_LIMIT = 7
    DATE_FORMAT_REGEX = "^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
    DATE_FORMAT_DATETIME = '%Y-%m-%d'
    LF_ATTRIBUTES = {'name', 'estimated_diameter', 'close_approach_data'}

    API_KEY = os.environ.get('API_KEY')


settings = Settings()
