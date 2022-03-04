[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# python-simple-mqtt-k3s

This project is a simple example of containerizing an application that 
publishes to an MQTT broker.  It has been tested with mosquitto running
on premise, but should work with any mqtt (eg. adafruit.io, etc). You may
need to set the parameters (ip, port, username, etc).  

## Installation

This application is meant to be installed on a kubernetes cluster, for 
example, I have a small raspberry pi cluster running k3s.  But it should
work on any kubernetes cluster (gke, etc).  

Currently automated builds are configured for `arm64` and `amd64`.  The 
auto-build containers are available at:

```ghcr.io/lila/python-simple-mqtt-k3s:main```


## Usage

There is no usage.  it just generates a simple time series that is supposed
to be temperature, and runs for ever. but you can set some of the parameters:

* MQTT_HOST:
* MQTT_PORT:
* MQTT_TOPIC:
* MQTT_SLEEP_DURATION:

To run on the commandline, use:

```bash
 docker run --env "MQTT_DEBUG=true" --env "MQTT_HOST=192.168.86.4"  ghcr.io/lila/python-simple-mqtt-k3s:main
 ```

 Of course, use your own MQTT Broker IP address. To run it in kubernetes:

 ```bash
 kubectl create -f deploy.yaml
 ```

the deployment yaml is very simple, you can configure it with the environment variables
as needed:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-simple-mqtt
spec:
  selector:
    matchLabels:
      app: python-simple-mqtt
  template:
    metadata:
      labels:
        app: python-simple-mqtt
    spec:
      containers:
        - name: python-simple-mqtt
          image: "ghcr.io/lila/python-simple-mqtt-k3s:main"
          env:
            - name: MQTT_HOST
              value: "192.168.86.4" 
            - name: MQTT_DEBUG
              value: "true"
```

## Contributing
Pull requests are welcome. or just fork and do what you want.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)



