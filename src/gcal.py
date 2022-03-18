"""
sample mqtt app that retrieves your calendar entries from google
calendar and publishes them to a mqtt topic

requires 2 env variables:  MQTT_HOST and MQTT_PORT to be defined 
and requires the secrets.py file that holds the credentials and
refresh tokens.
"""

import os
import sys
import time
import json
import requests
from pathlib import Path
import paho.mqtt.client as mqtt
from OAuth2 import OAuth2

#
# set up mqtt environment
#

debug = os.environ.get("MQTT_DEBUG", False)

mqttBroker = os.environ.get("MQTT_HOST", "192.168.86.4")
mqttPort = int(os.environ.get("MQTT_PORT", "1883"))
hostname = os.environ.get("HOSTNAME", "unknown")
topic = os.environ.get("MQTT_TOPIC", "Calendar")
sleep_duration = int(os.environ.get("MQTT_SLEEP_DURATION", "5"))

if debug:
    print(f"connecting to mqtt://{mqttBroker}:{mqttPort}/")

client = mqtt.Client("Google Calendar updater")
client.connect(mqttBroker, mqttPort)

#
# set up google calendar creds and apis
#


path = str(Path(__file__).parent.parent.absolute())
if debug:
    print("credentials stored in: " + path + "/secrets")
    print(os.listdir(path+"/secrets"))
sys.path.insert(1, path+"/secrets")
from secrets import secrets

TOKEN_OBTAINED_AT: int
TOKEN_OBTAINED_AT = 0
TIMEZONE = "+00:00"
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
GOOGLE_AUTH = OAuth2(
    requests,
    secrets["google_client_id"],
    secrets["google_client_secret"],
    SCOPES,
    secrets["google_access_token"],
    secrets["google_refresh_token"],
)


def _refresh_token() -> None:
    global TOKEN_OBTAINED_AT
    # Check if we have a token, if not we need to get one
    if (
        GOOGLE_AUTH.access_token_expiration is None
        or int(time.monotonic()) - TOKEN_OBTAINED_AT
        >= GOOGLE_AUTH.access_token_expiration
    ):
        print("Fetching a new access token ...")
        if not GOOGLE_AUTH.refresh_access_token():
            raise RuntimeError(
                "Unable to refresh access token - has the token been revoked?"
            )
        TOKEN_OBTAINED_AT = int(time.monotonic())


def _iso_date(date: time.struct_time) -> str:
    return "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}{:s}".format(
        date.tm_year,
        date.tm_mon,
        date.tm_mday,
        date.tm_hour,
        date.tm_min,
        date.tm_sec,
        TIMEZONE,
    )


def _url_encode(raw: str) -> str:
    return (
        raw.replace(":", "%3A")
        .replace("+", "%2B")
        .replace(" ", "%20")
        .replace("/", "%2F")
    )


def _fetch_events(event_count: int = 3) -> list:
    # see: https://developers.google.com/calendar/api/v3/reference/events/list
    _refresh_token()

    now = _iso_date(time.gmtime())
    minTime = _url_encode(now)
    url = (
        "https://www.googleapis.com/calendar/v3/calendars/{0}"
        "/events?maxResults={1}&timeMin={2}&orderBy=startTime"
        "&singleEvents=true"
    ).format(secrets["calendar_id"], event_count, minTime)
    headers = {
        "Authorization": "Bearer " + GOOGLE_AUTH.access_token,
        "Accept": "application/json",
        "Content-Length": "0",
    }

    print("Fetching events since " + now)
    response = requests.get(url, headers=headers)
    parsed = response.json()
    if "error" in parsed:
        raise RuntimeError("Error:", parsed)
    response.close()

    if not parsed["items"]:
        print("No upcoming events found.")
        return []

    return parsed["items"]


while True:
    el = _fetch_events()
    r = client.publish(f"{secrets['calendar_id']}/{topic}", json.dumps(el, indent=4))
    if debug:
        print(f"Just published to Topic {topic}: {r}")
    sys.stdout.flush()
    time.sleep(sleep_duration)
