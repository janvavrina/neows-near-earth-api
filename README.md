# neows-near-earth-api
Web application with a single REST endpoint that takes two date arguments and retrieves the list of near-Earth space objects approaching Earth in that time interval.

## Prerequisites
- Installed Docker
- Internet connection due to the external API

> All of the command below might need `sudo` depending on your configuration

---
### NOTE

After cloning before usage, create .env file with create_env_file.sh script


**Usage**

```./create_env_file.sh <your_api_key>```

or

```sh create_env_file.sh <your_api_key>```

where `<your_api_key>` is your API key that you generated through (Nasa APIs)[https://api.nasa.gov/]

If you do not enter any api key, you will be using DEMO_KEY with it's limitations.

**If you don't run this script before building image, you will get error.**
---

## Build image
```
docker build -t neows-api-image .
```

## Run container
```
docker run --env-file .env -d --name neows-container -p 8080:8080 neows-api-image
```

## Accessing your application
To access your application docs:
- `127.0.0.1:8080/docs` or `localhost:8080/docs` or `0.0.0.0:8080/docs`

## Tests
To run all tests (multiple ways):

Locally
- `pytest ./app/tests/test_main.py`

In docker
- `docker exec neows-container pytest ./app/tests/test_main.py`
