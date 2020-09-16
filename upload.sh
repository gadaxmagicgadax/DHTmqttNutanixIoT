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
