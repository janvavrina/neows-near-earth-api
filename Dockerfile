FROM python:3.11

# create dir in docker image
WORKDIR /code

# copy requirements to docker image
COPY ./requirements.txt /code/requirements.txt

# upgrade pip
RUN pip install --upgrade pip

# install and don't cache downloaded packages plus upgrade already installed ones
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY .env .env

# copy app files to docker image
COPY ./app /code/app

# run through uvicorn on address 0.0.0.0:80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]