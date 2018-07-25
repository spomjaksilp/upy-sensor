"""
basic structure of a sensor which has to be implemented.
"""

import uasyncio as asyncio


class Sensor:
    def __init__(self,
                 communicator,
                 topic,
                 interval=30,
                 repeat=True):
        self.communicator = communicator
        self.topic = topic
        self.interval = interval
        self.repeat = repeat

    async def report(self, data: dict):
        await self.communicator.report(data, self.topic)

    async def measure(self) -> dict:
        raise NotImplementedError

    async def run(self):
        while True:
            data = await self.measure()
            await self.report(data)

            if not self.repeat:
                return

            await asyncio.sleep(self.interval)
