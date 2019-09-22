class I2C_Device():
    def __init__(self, i2c, reginfo, address):
        self.reginfo = reginfo
        self.address = address
        self.i2c = i2c
    
    def read_register(self, register, nbytes=1):
        return self.i2c.readfrom_mem(self.address, register, nbytes)
    
    def write_register(self, register, value):
        return self.i2c.writeto_mem(self.address, register, bytearray(value))

    def update_register(self, register, offset, nbits, value):
        val = int.from_bytes(self.read_register(register), "big")
        val |= (value & (2**nbits -1)) << offset
        return self.i2c.writeto_mem(self.address, register, bytes([val]))

    def set_value(self, field_name, value):
        """
        Set values in the I2C device's memory according to the names specified in the reginfo dict

        :param field_name: String identifier of the bit field as specified in the reginfo dict.
        :param value: String identifier or raw value to be set to the bitfield. If options are specified in the reginfo, only these options can be set.
        """
        if field_name not in self.reginfo: raise ValueError("No bit field with name %s found in reginfo"%(field_name))
        if "ro" in self.reginfo[field_name] and self.reginfo[field_name]["ro"] == True: raise OSError("Trying to write on a read-only field")
        if "options" in self.reginfo[field_name]:
            if value not in self.reginfo[field_name]["options"]: raise ValueError("Value %s is non of the available options"%(value))
            self.update_register(self.reginfo[field_name]["reg"], self.reginfo[field_name]["offset"], self.reginfo[field_name]["len"], self.reginfo[field_name]["options"][value])
        else:
            self.update_register(self.reginfo[field_name]["reg"], self.reginfo[field_name]["offset"], self.reginfo[field_name]["len"], value)

    def read_value(self, field_name):
        if field_name not in self.reginfo: raise ValueError("No bit field with name %s found in reginfo"%(field_name))
        val = (int.from_bytes(self.read_register(self.reginfo[field_name]["reg"]), "big") >> self.reginfo[field_name]["offset"]) & (2**self.reginfo[field_name]["len"]-1)
        return val
