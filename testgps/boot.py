from machine import UART 
uart = UART(1, rx=16, tx=17, baudrate=9600, bits=8, parity=None, stop=1, timeout=5000, rxbuf=1024)
