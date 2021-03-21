# This file is executed on every boot (including wake-boot from deepsleep)
import gc
import machine
import webrepl
import ubinascii
from machine import Pin
from neopixel import NeoPixel
import config

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(config.WLANSSID, config.WLANPW)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

# NEOPIXEL - noch vor dem WLAN aktivieren
pin = Pin(0, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
np = NeoPixel(pin, 64)   # create NeoPixel driver on GPIO0 for 64 pixels

for i in range(0,64):
    np[i]=(211,54,2)
    np.write()


do_connect()
webrepl.start()
gc.collect()

mqtt_server = config.BrokerIP
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'4elements/command'
topic_pub = b'4elements/status'

