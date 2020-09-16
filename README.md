# Overview

This projects is aimed to build a device pushing temperature, humidity and location info from a microcontroller ESP32 to mqtt topic in Nutanix Karbon Platform Services. So, before using it you must define a "Data Source sensor" in Karbn Platform Services and get the appropriate  certificates to connect.

Bill of materials:

* A breadboard
* ESP32 microcontroller
* DHT11 sensor for temperature and humidity
* UBLOX - neo6m as GPS receiver
* LCD1602 lcd to display data from micropython code in ESP32
* A poteziometer (10K) for lcd

Best will be to mount on the breadboard one piece at a time and check if it is working. I've left in this git hub some tests I did.

This project has been implemented on Mac OS. 

# Preparing ESP32

First of all you must prepare ESP32 to work with micropython.

You need esptool and ampy tools you can install with :

```
pip install adafruit-ampy
pip install esptool
```

Get the micropython firmware esp32-idf3-20191220-v1.12.bin from [https://micropython.org/download/esp32/](https://micropython.org/download/esp32/)
