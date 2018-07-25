"""
helpers which are related to connecting the sensor to wifi.
"""

import machine
import uasyncio as asyncio
import network

async def connect_wifi(ssid, passphrase):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, passphrase)
        while not wlan.isconnected():
            machine.idle()
            pass
    print('network config:', wlan.ifconfig())
    return wlan
