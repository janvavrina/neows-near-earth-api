# neows-near-earth-api
Web application with a single REST endpoint that takes two date arguments and retrieves the list of near-Earth space objects approaching Earth in that time interval

> All of the command below might need `sudo` depending on your configuration

## Build image
```
docker build -t neows-api-image .
```

## Run container
```
docker run -d --name neows-container -p 80:80 neows-api-image
```
