"""
sample mqtt app that gets rss feed and publishes it to mqtt broker

requires 3 env variables:  MQTT_HOST and MQTT_PORT to be defined, 
along with RSS_FEED to specify the rss. 
"""

import os, sys
import time
import paho.mqtt.publish as publish
import feedparser
import json
from datetime import datetime
from time import mktime

debug = os.environ.get("MQTT_DEBUG", False)

mqttBroker = os.environ.get("MQTT_HOST", "192.168.1.4")
mqttPort = int(os.environ.get("MQTT_PORT", "1883"))
hostname = os.environ.get("HOSTNAME", "unknown")
topic = os.environ.get("MQTT_TOPIC", "RSS/pilocator")
sleep_duration = int(os.environ.get("MQTT_SLEEP_DURATION", "1800")) # 30 min = 60 * 30 = 1800
rss = os.environ.get("RSS_FEED", "https://rpilocator.com/feed.rss")

lastdate = datetime.min

if debug:
    print(f"connecting to mqtt://{mqttBroker}:{mqttPort}/")

while True:
    today = datetime.now()
    d = feedparser.parse(rss)
    
    if debug:
        print(f"retrieved: d = {d.feed}")
    
    updated = 0
    for e in d.entries[::-1]:  # reverse the list
        p = datetime.fromtimestamp(mktime(e.published_parsed))
        if lastdate < p:
            updated += 1
            publish.single(
                topic,
                json.dumps(e, indent=4),
                hostname=mqttBroker,
                port=mqttPort,
                client_id=rss,
            )
            if debug:
                print(f"{lastdate} < {p}")
                print(e.title)
                print(f"Just published to Topic {topic}")

    lastdate = today
    if debug:
        print(f"updated {updated} records.  lastdate is now: {lastdate}")
    

    sys.stdout.flush()
    time.sleep(sleep_duration)
