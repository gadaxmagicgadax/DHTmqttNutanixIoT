from micropyGPS import MicropyGPS

gps = MicropyGPS()

while True:
	buf = uart.readline()
	for char in buf:
		gps.update(chr(char))

	print('========= <<<<<<>>>>> =======')
	print(buf[1:6])
	if "GPGGA" in str(buf):
		print('UTC Timestamp:', gps.timestamp)
		print('Date:', gps.date_string('long'))
		print('Latitude:', gps.latitude)
		print('Longitude:', gps.longitude)
		print('Latitude string:', gps.latitude_string())
		print('Longitude string:', gps.longitude_string())
		print('Horizontal Dilution of Precision:', gps.hdop)
		print('Altitude:', gps.altitude)
		print('Satellites:', gps.satellites_in_use)
