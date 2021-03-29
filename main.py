import time
# import random
# import math
# import sys
import ubinascii
import machine
from machine import Pin
from neopixel import NeoPixel
from umqttsimple import MQTTClient
# from machine import soft_reset
import config

mqtt_server = config.BrokerIP
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'4elements/command'
topic_pub = b'4elements/status'

# NEOPIXEL
pin = Pin(0, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
np = NeoPixel(pin, 64)   # create NeoPixel driver on GPIO0 for 64 pixels

# MQTT
mqqt = False
last_message = 0
message_interval = 5
counter = 0
do_reset = False

# Animation
step = 5
delay = 10
winkel = 0
max_brightness = 0.5

buff_target=[[0, 0, 0] for x in range(0,64)]
buff_current=[[0, 0, 0] for x in range(0,64)]

def anim_earth():
  fill(142,98,44)

def anim_fire():
  fill(211,54,2)

def anim_air():
  fill(193,226,255)

def anim_water():
  fill(39,100,193)

anim = anim_fire

def sub_cb(topic, msg):
  print((topic, msg))
  if msg == b'earth':
    global anim = anim_earth
    # fill(142,98,44)
    print("Neue Szene: Earth")
    client.publish(topic_pub, "Neue Szene: Earth")
  elif msg == b'fire':
    global anim = anim_fire
    # fill(211,54,2)
    print("Neue Szene: Fire")
    client.publish(topic_pub, "Neue Szene: Fire")
  elif msg == b'air':
    global anim = anim_air
    # fill(193,226,255)
    print("Neue Szene: Air")
    client.publish(topic_pub, "Neue Szene: Air")
  elif msg == b'water':
    global anim = anim_water
    # fill(39,100,193)
    print("Neue Szene: Water")
    client.publish(topic_pub, "Neue Szene: Water")
  elif msg == b'reset':
    print("Softreset")
    # global do_reset = True # Softreset in der Callback Funktion schlägt irgendwie fehl...
    machine.soft_reset()
  elif topic == b'4elements/command' and msg == b'received':
    print('ESP received hello message')

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def fill(r,g,b):
  for i in range(0,64):
    np[i]=(r,g,b)
  np.write()

try:
  client = connect_and_subscribe()
  mqtt = True
except OSError as e:
  print("Keine Verbindung zum Broker")

while True:
  anim()
  if mqtt:
    try:
      client.check_msg()
      if (time.time() - last_message) > message_interval:
        msg = b'Hello #%d' % counter
        client.publish(topic_pub, msg)
        last_message = time.time()
        counter += 1
    except OSError as e:
      #restart_and_reconnect()
      print("Fehler beim Abrufen der Nachricht")
    time.sleep_ms(100)