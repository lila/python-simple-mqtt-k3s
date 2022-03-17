"""
simple launcher.  looks at the env variable MQTT_APP to decide what
to launch.
"""

import os

debug = os.environ.get("MQTT_DEBUG", False)
app = os.environ.get("MQTT_APP", "fake_temp.py")

if debug:
    print(f"executing app {app}")

os.system(f"python3 {app}")
