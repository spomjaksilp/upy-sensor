from .statistics import mean
from .dht import DHT11
from .bme import BME280

sensor_class = {
    "DHT11_OneWire": DHT11,
    "BME280_I2C": BME280,
}