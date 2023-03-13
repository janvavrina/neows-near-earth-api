# neows-near-earth-api
Web application with a single REST endpoint that takes two date arguments and retrieves the list of near-Earth space objects approaching Earth in that time interval.

## Prerequisites
- Installed Docker
- Internet connection due to the external API

> All of the command below might need `sudo` depending on your configuration

## Build image
```
docker build -t neows-api-image .
```

## Run container
```
docker run --env-file .env -d --name neows-container -p 80:80 neows-api-image
```

## Accessing your application
To access your application docs:
- `127.0.0.1:80/docs` or `localhost:80/docs`

## Tests
To run all tests (multiple ways):
> You need to be in app directory
- `./tests.sh`
- `sh tests.sh`
- `pytest tests/test_main.py`