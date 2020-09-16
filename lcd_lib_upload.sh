#!/bin/bash
echo "upload lcd_api.py"
ampy -p /dev/cu.SLAB_USBtoUART -b 115200 put ./python_lcd/lcd/lcd_api.py
echo "upload esp32_gpio_lcd.py"
ampy -p /dev/cu.SLAB_USBtoUART -b 115200 put ./python_lcd/lcd/esp32_gpio_lcd.py
