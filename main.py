from machine import Pin
from machine import soft_reset
from neopixel import NeoPixel
import time
import random
import math
import sys


# NEOPIXEL
# pin = Pin(0, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
# np = NeoPixel(pin, 64)   # create NeoPixel driver on GPIO0 for 64 pixels

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

#np = [ [0, 0, 0] for x in range(0,64)]

heart = [[0x00,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00], 
        [0x03,0x03,0x00], [0xff,0x6a,0x00], [0xad,0x00,0x00], [0x03,0x00,0x00], [0xb5,0x00,0x00], [0xac,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00], 
        [0xff,0x6a,0x00], [0xc4,0x0d,0x00], [0xbf,0x00,0x00], [0xb3,0x00,0x00], [0xc0,0x00,0x00], [0xbf,0x00,0x00], [0xa6,0x00,0x00], [0x00,0x00,0x00], 
        [0xc4,0x11,0x0a], [0xc0,0x00,0x00], [0xc3,0x00,0x00], [0xfc,0x00,0x00], [0xfa,0x00,0x00], [0xc0,0x00,0x00], [0xb3,0x00,0x00], [0x00,0x00,0x00], 
        [0xb9,0x0a,0x0a], [0xc2,0x00,0x00], [0xfc,0x00,0x00], [0xff,0x00,0x00], [0xfa,0x00,0x00], [0xc0,0x00,0x00], [0xab,0x00,0x00], [0x00,0x00,0x00], 
        [0x03,0x00,0x00], [0xb3,0x00,0x00], [0xc3,0x00,0x00], [0xf9,0x00,0x00], [0xc0,0x00,0x00], [0xa9,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00], 
        [0x00,0x00,0x00], [0x05,0x00,0x00], [0xae,0x00,0x00], [0xc0,0x00,0x00], [0xa7,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00], 
        [0x00,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00], [0xc0,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00], [0x00,0x00,0x00]] 



def reset():      # a convinient way to restart from WebREPL
#  import machine
#  machine.soft_reset()
  #soft_reset()
  sys.exit()



def sub_cb(topic, msg):
  print((topic, msg))
  if msg == b'earth':
    fill(142,98,44)
  elif msg == b'fire':
    fill(211,54,2)
  elif msg == b'air':
    fill(193,226,255)
  elif msg == b'water':
    fill(39,100,193)
    print("Setze Szene auf Wasser")
  elif msg == b'reset':
    print("Softreset")
    do_reset = True # Softreset in der Callback Funktion schlägt irgendwie fehl...
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



def initialFill():
  for i in range(0, 16):
    np[i]=(i+1,0,i+1)
    np.write()
    time.sleep_ms(20)    
  for i in range(16, 32):
    np[i]=(0,i,i)
    np.write()
    time.sleep_ms(20)    
  for i in range(32, 48):
    np[i]=(i,i,0)
    np.write()
    time.sleep_ms(20)    
  for i in range(48, 64):
    np[i]=(i,i,i)
    np.write()
    time.sleep_ms(20)    


# 3-5 Zufallswerte inerhalb der Farbwelt setzen, zufallspositionen, Zwischenwerte interpolieren
# Alle Pixel Frame by Frame auf diesen Wert hinsteuern

def test():
  test_color()

def fill(r,g,b):
  for i in range(0,64):
    np[i]=(r,g,b)
  np.write()

def test_color():
  for i in range(0,256):
    print("i="+str(i))
    fill(i,0,0)
    time.sleep_ms(10)
  for i in range(0,256):
    print("i="+str(i))
    fill(0,i,0)
    time.sleep_ms(10)
  for i in range(0,256):
    print("i="+str(i))
    fill(0,0,i)
    time.sleep_ms(10)
  for i in range(0,256):
    print("i="+str(i))
    fill(i,i,i)
    time.sleep_ms(10)




def create_rnd_target(buffer, r_min=0, r_max=0, g_min=0, g_max=30, b_min=30, b_max=255):
  for i in range(0,64):
    if r_max>0:
      buffer[i][0]=random.randint(r_min,r_max)
    else:
      buffer[i][0]=0
    if g_max>0:
      buffer[i][1]=random.randint(g_min,g_max)
    else:
      buffer[i][1]=0
    if b_max>0:
      buffer[i][2]=random.randint(b_min,b_max)
    else:
      buffer[i][2]=0

def draw_buffer(buffer):
  for i in range(0,64):
    np[i]=(buffer[i][0], buffer[i][1], buffer[i][2])
  np.write()

def breathe():
  step = 1
  delay = 30
  winkel = 0
  while True:
    brightness=math.sin(math.radians(winkel))

    for i in range(0,64):
      np[i]=(int(heart[i][0]*brightness), int(heart[i][1]*brightness), int(heart[i][2]*brightness))
    np.write()
    winkel = winkel + step
    if winkel > 180:
      winkel=0
    time.sleep_ms(delay)


initialFill()
#time.sleep(10)
#breathe()




try:
  client = connect_and_subscribe()
  mqtt = True
except OSError as e:
  #restart_and_reconnect()
  print("Keine Verbindung zum Broker")
  #time.sleep(10)

while True:
  if do_reset:
    reset()

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
      #print("Fehler beim Abrufen der Nachricht")
      time.sleep(10)


while True:
  step=random.randint(1,10) # Geschwindigkeit des Fades
  print("step="+str(step))
  create_rnd_target(buff_target,0,155,0,155,0,155) # Zielfarbe
  fading = True
  while fading:
    changes = 0
    for led in range(0,64): # für jede LED
      for color in range(0,3): # für jedes Farb-Byte
        if buff_current[led][color] < buff_target[led][color]: # Intensität erhöhen
          changes += 1
          if buff_current[led][color] + step > buff_target[led][color]:
            buff_current[led][color] = buff_target[led][color]
          else:
            buff_current[led][color] += step

        elif buff_current[led][color] > buff_target[led][color]: # Intensität verringern
          changes += 1
          if buff_current[led][color] - step < buff_target[led][color]:
            buff_current[led][color] = buff_target[led][color]
          else:
            buff_current[led][color] -= step
    print(changes)
    if changes == 0:
      fading=False
    draw_buffer(buff_current)
    #draw_buffer(buff_target)
    time.sleep_ms(10)




#while True:
#  create_rnd_target(buff_target,0,10,0,20,0,255)
#  draw_buffer(buff_target)
#  time.sleep_ms(2000)
