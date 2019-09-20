"""
everything regarding the connection to the mqtt server.
"""

import time
from umqtt.simple import MQTTClient
import uasyncio as asyncio
from uasyncio.synchro import Lock
import json


class MQTTCommunicator:
    def __init__(self, host: str, wifi_network):
        self.host = host
        self.wifi_network = wifi_network

        self.con = None

        # setup lock
        self.com_lock = Lock()

        asyncio.ensure_future(self.connect_mqtt())

    async def connect_mqtt(self):
        yield from self.com_lock.acquire()
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
        self.com_lock.release()

    async def report(self, data: dict, topic: str) -> None:
        yield from self.com_lock.acquire()
        payload = json.dumps(data)
        self.con.publish(topic.encode(), payload.encode())
        self.com_lock.release()
