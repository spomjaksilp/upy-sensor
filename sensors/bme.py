import uasyncio as asyncio
import machine

from .BME280 import BME280 as BME280Device
from .base import Sensor

class BME280(Sensor):
    def __init__(self, *args, **kwargs):
        """
        Use micropythons DHT implementation in the provided pin.
        :param pin:
        :param args:
        :param kwargs:
        """
        conf = args[0]
        assert "i2c" in conf, "I2C definition for BME280 missing"
        i2c = machine.I2C(sda=machine.Pin(conf["i2c"]["pin_sda"]), scl=machine.Pin(conf["i2c"]["pin_scl"]), freq=400000)
        self.bm280 = BME280Device(address=conf["i2c"]["device_id"], i2c=i2c)
        super().__init__(*args, **kwargs)

    async def measure(self):
        t, p, h = self.bm280.read_compensated_data()
        
        data = {
            "temperature": t,
            "humidity": h,
            "pressure": p/100
        }

        return data