# standard python
import json
import time
import uasyncio as asyncio

# bare metal imports
import machine

# local imports
from utils import connect_wifi, MQTTCommunicator
from sensors import sensor_class


async def main():
    # get configuration from file
    with open("configuration.json") as f:
        conf = json.load(f)

    # wifi is not connected we just got the coroutine
    wifi = connect_wifi(ssid=conf["network"]["ssid"],
                        passphrase=conf["network"]["passphrase"])

    # mqtt
    mqtt = MQTTCommunicator(host=conf["mqtt"]["host"], wifi_network=wifi)

    # sensor
    for sensor in conf["sensors"]:
        if sensor["class"] not in sensor_class:
            print("Sensor class %s not available"%(sensor["class"]))
            continue
        print("Activate sensor %s (%s)"%(sensor['name'], sensor['class']))
        s = sensor_class[sensor["class"]](sensor, communicator=mqtt)
        asyncio.ensure_future(s.run())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
