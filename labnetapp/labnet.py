import os,serial,time,sys,psutil,threading,redis
from subprocess import *
from labnetapp import app
from datetime import datetime
from collections import deque

SERIAL_DATA = deque([])
if app.config['FEATURE']['com']:
	ser = serial.Serial(app.config['COM']['port'], app.config['COM']['baud'], timeout=app.config['COM']['timeout'])
time.sleep(1)

def send(telegram):
	SERIAL_DATA.append(telegram)

def ping():
	while True:
		time.sleep(10)
		send("ping")

def serial_in():
	pass

def serial_out():
	while True:
		time.sleep(0.1)
		try:
			ds = SERIAL_DATA.popleft()
			print("mcp: " +  ds)
			#ser.write(ds)
		except IndexError:
			pass

def start_threads():
	if app.config['FEATURE']['com']:
		thread_serial_in 			= threading.Thread(target=serial_in)
		thread_serial_in.daemon 	= True
		thread_serial_in.start()
		thread_serial_out 			= threading.Thread(target=serial_out)
		thread_serial_out.daemon 	= True
		thread_serial_out.start()
#	thread_ping 				= threading.Thread(target=ping)
#	thread_ping.daemon 			= True
#	thread_ping.start()

def cleanup():
	#ser.close()
	pass