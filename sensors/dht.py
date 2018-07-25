import uasyncio as asyncio
import machine
import dht

from .base import Sensor
from .statistics import mean


class DHT11(Sensor):
    def __init__(self, pin, *args, **kwargs):
        """
        Use micropythons DHT implementation in the provided pin.
        :param pin:
        :param args:
        :param kwargs:
        """
        self.dht = dht.DHT11(machine.Pin(pin))
        super().__init__(*args, **kwargs)

    async def measure(self):
        """
        Because the sensor values deviate quite a bit, collect 10 values.
        :return:
        """
        t_list = []
        h_list = []

        for _ in range(0, 10):
            self.dht.measure()
            t_list.append(self.dht.temperature())
            h_list.append(self.dht.humidity())

            await asyncio.sleep(1)

        t = round(mean(t_list))
        h = round(mean(h_list))

        data = {
            "temperature": t,
            "humidity": h,
        }

        return data