import time
import struct
from .i2cdevice import I2C_Device

reginfo_qmc5883 = {
    "X":               {"reg":0x00, "offset": 0, "len": 16, "ro":True},
    "Y":               {"reg":0x02, "offset": 0, "len": 16, "ro":True},
    "Z":               {"reg":0x04, "offset": 0, "len": 16, "ro":True},
    "STATUS_DRDY":     {"reg":0x06, "offset": 0, "len": 1,  "ro":True},
    "STATUS_OVL":      {"reg":0x06, "offset": 1, "len": 1,  "ro":True},
    "STATUS_DOR":      {"reg":0x06, "offset": 2, "len": 1,  "ro":True},
    "TEMP":            {"reg":0x07, "offset": 0, "len": 16, "ro":True},
    "CONFIG_MODE":     {"reg":0x09, "offset": 0, "len": 2, "options": {"STANDBY": 0, "CONTINOUS":1}}, #Acquisition mode
    "CONFIG_ODR":      {"reg":0x09, "offset": 2, "len": 2, "options": {"10HZ": 0, "50HZ":1, "100HZ":3, "200HZ":4}}, #Output data rate. Slower saves more power
    "CONFIG_RNG":      {"reg":0x09, "offset": 4, "len": 2, "options": {"2GAUSS": 0, "8GAUSS":1}}, # Maximum measurement range in Gauss
    "CONFIG_OSR":      {"reg":0x09, "offset": 6, "len": 2, "options": {"512": 0, "256":1, "128":3, "64":4}}, #Oversampling ratio
    "CONFIG_INT_ENB":  {"reg":0x0a, "offset": 0, "len": 1, "options": {False: 0, True: 1}}, #Enable interrupt
    "CONFIG_ROLL_PNT": {"reg":0x0a, "offset": 6, "len": 1, "options": {False: 0, True: 1}}, #Enable rolling pointer mode
    "CONFIG_SOFT_RST": {"reg":0x0a, "offset": 7, "len": 1, "options": {False: 0, True: 1}}, #Trigger soft reset. Restore default register values
    "RESET_PERIOD":    {"reg":0x0b, "offset": 0, "len": 8}, #Reset period. It's recommended to set it to 0x01
    "CHIP_ID":         {"reg":0x0d, "offset": 0, "len": 8, "ro":True} #Returns chip ID. Should be 0xff
}

class QMC5883(I2C_Device):
    def __init__(self, i2c, address=0x0d, offset=50.0):
        super().__init__(i2c, reginfo_qmc5883, address)
        self.temp_offset = offset
        
        self.reset()
        self.set_oversampling("64")
        time.sleep(0.01)
        self.set_range("2GAUSS")
        time.sleep(0.01)
        self.set_sampling_rate("100HZ")
        time.sleep(0.01)
        self.set_mode("CONTINOUS")
        time.sleep(0.01)
        self.set_value("CONFIG_INT_ENB", False)
        time.sleep(0.01)
        
    def reset(self):
        self.set_value("CONFIG_SOFT_RST", True)
        self.set_value("RESET_PERIOD", 1)
        time.sleep(0.1)

    def set_oversampling(self, sampling):
        self.set_value("CONFIG_OSR", sampling)

    def set_range(self, rng):
        self.range = rng
        self.set_value("CONFIG_RNG", rng)

    def set_sampling_rate(self, rate):
        self.set_value("CONFIG_ODR", rate)

    def set_mode(self, mode):
        self.set_value("CONFIG_MODE", mode)

    def ready(self):
        # prevent hanging up here.
        # Happens when reading less bytes then all 3 axis and will
        # end up in a loop. So, return any data but avoid the loop.
        if self.read_value("STATUS_DOR") == 1:
            print("Incomplete read")
            return 1

        return self.read_value("STATUS_DRDY")

    def read_raw(self):
        try:
            while not self.ready():
                time.sleep(0.005)
            val = self.read_register(self.reginfo['X']['reg'], 9)
                                       
        except OSError as error:
            print("OSError", error)
            pass  # just silently re-use the old values
        # Convert the axis values to signed Short before returning
        x, y, z, _, temp = struct.unpack('<hhhBh', val)

        return (x, y, z, temp)

    def read_scaled(self):
        x, y, z, temp = self.read_raw()
        scale = 12000 if self.range == "2GAUSS" else 3000

        return (x / scale, y / scale, z / scale,
                (temp / 100 + self.temp_offset))