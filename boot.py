# This file is executed on every boot (including wake-boot from deepsleep)
import uos, machine
import gc
import webrepl
from umqttsimple import MQTTClient
import ubinascii
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

do_connect()
webrepl.start()
gc.collect()

mqtt_server = config.BrokerIP
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'4elements/command'
topic_pub = b'4elements/status'

