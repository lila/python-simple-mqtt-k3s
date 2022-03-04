"""
sample mqtt app that gets containerized and run in k8s

requires 2 env variables:  MQTT_HOST and MQTT_PORT to be defined 
"""

import os, sys
from random import randrange
import time
import paho.mqtt.client as mqtt

debug = os.environ.get("MQTT_DEBUG", False)

mqttBroker = os.environ.get("MQTT_HOST", "192.168.1.4")
mqttPort = int(os.environ.get("MQTT_PORT", "1883"))
hostname = os.environ.get("HOSTNAME", "unknown")
topic = f'{hostname}/{os.environ.get("MQTT_TOPIC", "TEMPERATURE")}'
sleep_duration = int(os.environ.get("MQTT_SLEEP_DURATION", "5"))

if debug:
    print(f"connecting to mqtt://{mqttBroker}:{mqttPort}/")

client = mqtt.Client("Temperature_Outside")
client.connect(mqttBroker, mqttPort)

while True:
    randNumber = randrange(10)
    client.publish(topic, randNumber)
    if debug: 
        print(f'Just published {randNumber} to Topic {topic}')
    sys.stdout.flush()
    time.sleep(sleep_duration)
