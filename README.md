# python-simple-mqtt-k3s

This project is a simple example of containerizing an application that 
publishes to an MQTT broker.  It has been tested with mosquitto running
on premise, but should work with any mqtt (eg. adafruit.io, etc). You may
need to set the parameters (ip, port, username, etc).  

## Installation

This application is meant to be installed on a kubernetes cluster, for 
example, I have a small raspberry pi cluster running k3s.  But it should
work on any kubernetes cluster (gke, etc), but you may have to build 
the container for your architecture.  

```bash
helm install github link?
```

## Usage

There is no usage.  it just generates a simple time series that is supposed
to be temperature, and runs for ever. but you can set some of the parameters:

* MQTT_HOST:
* MQTT_PORT:
* MQTT_TOPIC:
* MQTT_SLEEP_DURATION:


## Contributing
Pull requests are welcome. or just fork and do what you want.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)


[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
