# Overview

This projects is aimed to build a device pushing temperature, humidity and location info from a microcontroller ESP32 to mqtt topic in Nutanix Karbon Platform Services. So, before using it you must define a "Data Source sensor" in Karbn Platform Services and get the appropriate  certificates to connect.

Bill of materials:

* A breadboard
* ESP32 microcontroller
* DHT11 sensor for temperature and humidity
* UBLOX - neo6m as GPS receiver
* LCD1602 lcd to display data from micropython code in ESP32
* A poteziometer (10K) for lcd
* A USB cable
* A powerbank. (initially I tried with a power supply with a battery. No way! the UBLOX neo6m needs 5V and 0.5 Ampere stable )

Best will be to mount on the breadboard one piece at a time and check if it is working. I've left in this git hub some tests I did.

This project has been implemented on Mac OS.

![Test Image 4]([https://github.com/gadaxmagicgadax/DHTmqttNutanixIoT/blob/master/ESP32-DHT11-UBlox-LCD.jpg])

Here below the table with all the links (see also the file BBpinslinks.xlsx)

![1600275582196.png](./1600275582196.png)


# Preparing ESP32

First of all you must prepare ESP32 to work with micropython.

You need *esptool* and *ampy* tools you can install with :

```
pip install adafruit-ampy
pip install esptool
pip install rshell
```

Get the micropython firmware *esp32-idf3-20191220-v1.12.bin* from [https://micropython.org/download/esp32/](https://micropython.org/download/esp32/)

Connect the ESP32 microcontroller to your serial port of the MAC and run the following commands:

```
esptool.py --chip esp32 --port /dev/cu.SLAB_USBtoUART --baud 115200 erase_flash
esptool.py --chip esp32 --port /dev/cu.SLAB_USBtoUART --baud 115200 write_flash -z 0x1000 esp32-idf3-20191220-v1.12.bin
```

Done ! The ESP32 is now ready to receive your code !

Basically the code can be organised as you wish. I choose to have a boot.py file , which is executed any time you boot the ESP32, and a main.py with all the code.

# Upload the software

As a prerequisite you will have to get the certificate files for the MQTT and SSID/Password of your smartphone hotspot.

Why a smartphone hotspot ? Because if you want to test the device you should move around  to get different latitude/longitude/altitude data. I have a car with USB port so I used a USB cable and connect the ESP32 directly in my car. My iphone provided the hotspot for the WIFI.

The upload.sh chell file containes the exact list of uploads you have to do:

```
#!/bin/bash
echo "upload 1595946770019_CACertificate.crt"
ampy -p /dev/cu.SLAB_USBtoUART -b 115200 put 1595946770019_CACertificate.crt
echo "upload 1595946770019_certificate.crt"
ampy -p /dev/cu.SLAB_USBtoUART -b 115200 put 1595946770019_certificate.crt
echo "upload 1595946770019_privateKey.key"
ampy -p /dev/cu.SLAB_USBtoUART -b 115200 put 1595946770019_privateKey.key
echo "upload lcd_api.py"
ampy -p /dev/cu.SLAB_USBtoUART -b 115200 put ./python_lcd/lcd/lcd_api.py
echo "upload nodemcu_gpio_lcd.py"
ampy -p /dev/cu.SLAB_USBtoUART -b 115200 put ./python_lcd/lcd/nodemcu_gpio_lcd.py
echo "upload micropyGPS.py"
ampy -p /dev/cu.SLAB_USBtoUART -b 115200 put ./micropyGPS/micropyGPS.py
echo "upload main.py"
ampy -p /dev/cu.SLAB_USBtoUART -b 115200 put main.py
echo "upload boot.py"
ampy -p /dev/cu.SLAB_USBtoUART -b 115200 put boot.py

```

You can use tools like Thonny or uPyCraft to upload the code and run tests and troubleshooting. I did but I had lot of problems so I decided to use *rshell*

If you connect the usb cable from ESP32 to your MAC , use this command:

````
rshell -p /dev/cu.SLAB_USBtoUART -b 115200
````

at the prompt run:

*repl*

then

ctr-D (this will reboot the ESP32)

You will see in your terminal all the prints of your micropython code.

Here below an example with my MAC (lat/lon/altitude are 0 because I was at home and the GPS receiver works only in open air):

```
$ rshell -p /dev/cu.SLAB_USBtoUART -b 115200
Using buffer-size of 32
Connecting to /dev/cu.SLAB_USBtoUART (buffer-size 32)...
Trying to connect to REPL  connected
Testing if ubinascii.unhexlify exists ... Y
Retrieving root directories ... /1595946770019_CACertificate.crt/ /1595946770019_certificate.crt/ /1595946770019_privateKey.key/ /lcd_api.py/ /nodemcu_gpio_lcd.py/ /micropyGPS.py/ /main.py/ /boot.py/
Setting time ... Sep 16, 2020 19:06:10
Evaluating board_name ... pyboard
Retrieving time epoch ... Jan 01, 2000
Welcome to rshell. Use Control-D (or the exit command) to exit rshell.
/Users/giovannigadaleta/micropython/DHTmqttNutanixIoT> repl
Entering REPL. Use Control-X to exit.
>
MicroPython v1.12 on 2019-12-20; ESP32 module with ESP32
Type "help()" for more information.
>>> 
>>> 
MPY: soft reboot
Connection successful
('172.20.10.14', '255.255.255.240', '172.20.10.1', '172.20.10.1')
main entered
Connected to 151.0.230.202 MQTT broker, subscribed to b'weather/data' topic
Temperature: 26.0 C
Temperature: 78.8 F
Humidity: 56.0 %
b'$GPGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99*30\r\n'
Satellites in use : 0
b'$GPGSV,1,1,00*79\r\n'
Satellites in use : 0
b'$GPGLL,,,,,,V,N*64\r\n'
Satellites in use : 0
b'$GPRMC,,V,,,,,,,,,,N*53\r\n'
Satellites in use : 0
b'$GPVTG,,,,,,,,,N*30\r\n'
Satellites in use : 0
b'$GPGGA,,,,,,0,00,99.99,,,,,,*48\r\n'
Satellites in use : 0
{"measurement":"weather", "tags": { "Area": "Italy", "Location": "Aprilia" }, "fields": {"temperature" : "26","humidity" : "56","latitude" : 0.0,"longitude" : 0.0,"altitude" : 0.0}}
```
