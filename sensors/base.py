"""
basic structure of a sensor which has to be implemented.
"""

import uasyncio as asyncio


class Sensor:
    def __init__(self,
                 config,
                 communicator,
                 interval=30,
                 repeat=True):
        self.config = config
        self.communicator = communicator
        self.topic = config["topic"] if "topic" in config else config['name']
        self.interval = config["interval"] if "interval" in config else interval
        self.repeat = config["repeat"] if "repeat" in config else repeat

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
