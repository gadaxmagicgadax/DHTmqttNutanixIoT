import time
from umqtt.simple import MQTTClient # this module taken from https://raw.githubusercontent.com/RuiSantosdotme/ESP-MicroPython/master/code/MQTT/umqttsimple.py
import machine
from machine import Pin
from machine import UART
from time import sleep
import ubinascii
import micropython
import network
import dht
import esp
import random
from nodemcu_gpio_lcd import GpioLcd # this module taken from https://github.com/dhylands/python_lcd
from micropyGPS import MicropyGPS # this module taken from https://github.com/inmcm/micropyGPS

# iphone
ssid = "gadaxiPhone"
password = "xxxxxxxxxxxxxx"


# create uart object to manage serial communication from gps module
uart = UART(1, rx=16, tx=17, baudrate=9600, bits=8, parity=None, stop=1, timeout=5000, rxbuf=1024)

# create lcd object to display data on the breadboard
lcd = GpioLcd(rs_pin=Pin(13),
	enable_pin=Pin(12),
	d4_pin=Pin(21),
	d5_pin=Pin(22),
	d6_pin=Pin(23),
	d7_pin=Pin(25),
	num_lines=2, num_columns=20)
lcd.clear()
lcd.putstr("LCD Ready")

# set up mqtt topic IP address and topic name for publish and subcribe
# set up client id for mqtt connection
mqtt_server = '151.0.230.202'
topic_sub = b'weather/data'
topic_pub = b'weather/data'
client_id = ubinascii.hexlify(machine.unique_id())



last_message = 0
message_interval = 5
counter = 0

# open connection to WIFI

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')

# retrieve IP after connection to WIFI and print on LCD

sc = station.ifconfig()
print(sc)
lcd.clear()
lcd.putstr("after conn:\n" + sc[0])

