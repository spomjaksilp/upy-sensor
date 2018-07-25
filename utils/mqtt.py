"""
everything regarding the connection to the mqtt server.
"""

import time
from umqtt.simple import MQTTClient
import uasyncio as asyncio
import json


class MQTTCommunicator:
    def __init__(self, host: str, wifi_network):
        self.host = host
        self.wifi_network = wifi_network

        self.con = None

        # setup lock
        self.com_lock = asyncio.Lock()

        asyncio.ensure_future(self.connect_mqtt())

    async def connect_mqtt(self):
        async with self.com_lock:
            # connect to wifi
            await self.wifi_network

            # now connect to mqtt server
            self.con = MQTTClient(repr(time.time()), self.host)
            con_reply = None
            while con_reply is None:
                try:
                    con_reply = self.con.connect()
                    await asyncio.sleep(1)
                except OSError:
                    print("failed to connect to mqtt")
            print("connected to mqtt {}".format(self.host))

    async def report(self, data: dict, topic: str) -> None:
        async with self.com_lock:
            payload = json.dumps(data)
            self.con.publish(topic.encode(), payload.encode())
