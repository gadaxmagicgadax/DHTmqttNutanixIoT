def sub_cb(topic_sub, msg):
	print((topic, msg))
	#if topic == b'notification' and msg == b'received':
	#  print('ESP received hello message')

# connects to mqtt topic with certificates and subscribe
def connect_and_subscribe():
	global client_id, mqtt_server, topic_sub
	with open ('1595946770019_privateKey.key') as f:
		key_data = f.read()
	with open ('1595946770019_certificate.crt') as f:
		cert_data = f.read()

	client = MQTTClient(client_id, mqtt_server,port=1883,ssl=True,ssl_params={'key': key_data,'cert': cert_data})
  
	client.set_callback(sub_cb)
	client.connect()
	client.subscribe(topic_sub)
	print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
	lcd.clear()
	lcd.move_to(0,0)
	lcd.putstr("MQTT conn !!")
	return client

def restart_and_reconnect():
	print('Failed to connect to MQTT broker. Reconnecting...')
	time.sleep(10)
	machine.reset() 

def main():

	try:
		client = connect_and_subscribe()
	except OSError as e:
		print(e)
		restart_and_reconnect()

	sensor = dht.DHT11(Pin(4))
	# define micropygps object
	gps = MicropyGPS()

	# initialize paylod with initial fixed json
	payload = '{"measurement":"weather", "tags": { "Area": "Italy", "Location": "Aprilia" }, "fields": {'

	while True:
		try:
			sleep(5)
			# call DHT sensor and get temperature and humidity
			sensor.measure()
			temp = sensor.temperature()
			hum = sensor.humidity()
			temp_f = temp *(9/5) +32.0
			print('Temperature: %3.1f C' %temp)
			print('Temperature: %3.1f F' %temp_f)
			print('Humidity: %3.1f %%' %hum)
			payload = payload + '\"temperature\" : \"' + str(temp) + "\","
			payload = payload + '\"humidity\" : \"' + str(hum) + "\","

			while True:
				# read gps sentences
				buf = uart.readline()
				for char in buf:
					gps.update(chr(char))
				# this will show on the serial all the GPS sentences received
				print(buf)
				# this will show on the serial how many satellites are connected. They must be at least 3
				print("Satellites in use : " + str(gps.satellites_in_use))
				# manage GPGGA sentence only to get altitude, latitude and longitude
				if "GPGGA" in str(buf):
					lat = gps.latitude[0] + (gps.latitude[1]/60)
					lng = gps.longitude[0] + (gps.longitude[1]/60)
					payload = payload + '\"latitude\" : ' + str(float(lat)) + ','
					payload = payload + '\"longitude\" : ' + str(float(lng)) + ','
					payload = payload + '\"altitude\" : ' + str(gps.altitude) + '}}'
					
					# display on serial and lcd for debugging purpose
					print(payload)
					lcd.clear()
					lcd.move_to(0,0)
					print("lat="+str(lat))
					break
			# Sending data to mqtt only if gps data are available
			# When all starts on the bradboard, GPS module takes some time to connect to the GPS network
			# during this startup time, data are all 0
			if float(lat) != 0.0:
				print("latitude is not 0")
				client.publish(topic_pub,payload)
				lcd.clear()
				lcd.move_to(0,0)
				lcd.putstr("T=" + str(temp))
				lcd.putstr("H=" + str(hum))
				lcd.move_to(0,1)
				lcd.putstr("GPS lat="+str(lat))
				client.publish(topic_pub,payload)
			else:
				lcd.clear()
				lcd.move_to(0,0)
				lcd.putstr("GPS starting up")
				print("latitude is 0")

			# reset the payload for next iteration	
			payload = '{"measurement":"weather", "tags": { "Area": "Italy", "Location": "Aprilia" }, "fields": {'
		except OSError as e:
			print('Failed to read sensor.')
			print (e)

if __name__ == '__main__':
    print("main entered")
    esp.osdebug(0)
    main()
  




