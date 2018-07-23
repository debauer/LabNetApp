import can
import os,serial,time,sys,psutil,threading,redis
from subprocess import *
from app import app
from binascii import unhexlify, hexlify

if app.config['FEATURE']['can']:
	try:
		bus = can.interface.Bus(app.config['CAN']['interface'], bustype=app.config['CAN']['type'])
		can_buffer = can.BufferedReader()
		notifier = can.Notifier(bus, [can_buffer], timeout=0.1)
	except BaseException as e:
		print("CAN bus error: %s" % e)
		sys.exit(1)
	
def send_can_message(id, data):
	print("Sending CAN message with arbitration id %s and data %s" % (format(id, '#04x'), hexlify(data)))
	if app.config['FEATURE']['can']:
		bus.send(can.Message(extended_id=True, arbitration_id=id, data=data))

def canRx():

	pass

def canTx():
	while True:
		time.sleep(5)
		try:
			# 01 F 01 031     00 0C 01 02 02 02 02 02
			data = bytearray(b'\x00\x0C\x01\x02\x02\x02\x02\x02')
			send_can_message(0x01F01031, bytearray(b'\x00\x0C\x01\x02\x02\x02\x02\x02'))
		except IndexError:
			pass

thread_rx 			= threading.Thread(target=canRx)
thread_rx.daemon 	= True
thread_rx.start()
thread_tx 			= threading.Thread(target=canTx)
thread_tx.daemon 	= True
thread_tx.start()