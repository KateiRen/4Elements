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

#from bitmaps import earth
# !!!!!!! erzeugt Memory Error
earth = [[ 0, 0, 0], [ 0, 0, 0], [142, 77, 21], [137, 88, 21], [129, 88, 0], [227, 173, 49], [ 0, 0, 0], [ 0, 0, 0], [ 0, 0, 0], [156, 77, 18], [173, 120, 28], [175, 128, 14], [174, 126, 2], [180, 110, 12], [155, 80, 0], [ 0, 0, 0], [207, 146, 39], [159, 103, 10], [172, 118, 9], [172, 118, 9], [172, 118, 9], [142, 84, 20], [149, 76, 7], [154, 77, 5], [166, 138, 5], [177, 145, 22], [137, 90, 10], [139, 84, 19], [137, 75, 14], [142, 84, 20], [142, 81, 14], [144, 81, 14], [157, 117, 4], [151, 108, 6], [137, 90, 10], [144, 80, 16], [153, 96, 29], [142, 84, 20], [135, 88, 8], [136, 85, 22], [157, 77, 0], [187, 110, 28], [137, 90, 10], [159, 97, 0], [159, 97, 0], [159, 97, 0], [130, 94, 0], [135, 88, 6], [ 0, 0, 0], [209, 102, 20], [182, 83, 0], [154, 80, 0], [227, 171, 60], [210, 172, 39], [136, 90, 4], [ 0, 0, 0], [ 0, 0, 0], [ 0, 0, 0], [175, 81, 0], [148, 82, 0], [161, 107, 19], [156, 112, 17], [ 0, 0, 0], [ 0, 0, 0]]

mqtt_server = config.BrokerIP
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'4elements/#'
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
step = 0
delay = 100 # ms
winkel = 0
max_brightness = 0.5

buff_target=[[0, 0, 0] for x in range(0,64)]
buff_current=[[0, 0, 0] for x in range(0,64)]


def anim_earth():
  # fill(142,98,44)
  global step
  for i in range(0,64):
    np[i]=(int(earth[i][0]*max_brightness),int(earth[i][1]*max_brightness),int(earth[i][2]*max_brightness))
  np.write()
  if step < 17:
    step += 1
  else:
    step = 0


def anim_fire():
  fill(211,54,2)

def anim_air():
  fill(193,226,255)

def anim_water():
  fill(39,100,193)

anim = anim_fire

def sub_cb(topic, msg):
  global anim, delay, step, max_brightness
  print((topic, msg))
  if topic == b'4elements/setScene': # sieht in etwa so aus (b'4elements/setScene', b'fire')
    if msg == b'earth':
      anim = anim_earth
      delay = 300
      step = 0
      # fill(142,98,44)
      print("Neue Szene: Earth")
      client.publish(topic_pub, "Neue Szene: Earth")
    elif msg == b'fire':
      anim = anim_fire
      # fill(211,54,2)
      print("Neue Szene: Fire")
      client.publish(topic_pub, "Neue Szene: Fire")
    elif msg == b'air':
      anim = anim_air
      # fill(193,226,255)
      print("Neue Szene: Air")
      client.publish(topic_pub, "Neue Szene: Air")
    elif msg == b'water':
      anim = anim_water
      # fill(39,100,193)
      print("Neue Szene: Water")
      client.publish(topic_pub, "Neue Szene: Water")
    else:
      client.publish(topic_pub, "Unbekannte Szene")

  elif topic == b'4elements/setBrightness':
    a = int(msg)
    print(str(a))
    print(str(a/100))
    if a < 0 or a > 100:
      a = 50
    max_brightness = a / 100

  elif topic == b'4elements/doReset':
    client.publish(topic_pub, "Ich starte mich neu...")
    time.sleep_ms(100)
    machine.reset()
    # machine.soft_reset()

  else:
    pass


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
    np[i]=(int(r*max_brightness),int(g*max_brightness),int(b*max_brightness))
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
    time.sleep_ms(delay)