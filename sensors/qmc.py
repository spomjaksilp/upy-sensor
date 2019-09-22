import uasyncio as asyncio
import machine

from .QMC5883 import QMC5883 as QMC5883Device
from .base import Sensor

class QMC5883(Sensor):
    def __init__(self, *args, **kwargs):
        """
        Use micropythons DHT implementation in the provided pin.
        :param pin:
        :param args:
        :param kwargs:
        """
        conf = args[0]
        assert "i2c" in conf, "I2C definition for QMC5883 missing"
        i2c = machine.I2C(sda=machine.Pin(conf["i2c"]["pin_sda"]), scl=machine.Pin(conf["i2c"]["pin_scl"]), freq=400000)
        temp_offset = conf["temperature_offset"] if "temperature_offset" in conf else 30.0
        self.qmc5883 = QMC5883Device(i2c=i2c, offset=temp_offset)
        super().__init__(*args, **kwargs)

    async def measure(self):
        x, y, z, t = self.qmc5883.read_scaled()
        
        data = {
            "x": x,
            "y": y,
            "z": z,
            "temperature": t
        }

        return data