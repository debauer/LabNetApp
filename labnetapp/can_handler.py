
import can
import os,serial,time,sys,psutil,threading,redis,random
from subprocess import *
from labnetapp import app, store,socketio
from binascii import unhexlify, hexlify
from collections import deque

messages = deque([])

if app.config['FEATURE']['can']:
	try:
		bus = can.interface.Bus(app.config['CAN']['interface'], bustype=app.config['CAN']['type'])
		can_buffer = can.BufferedReader()
		notifier = can.Notifier(bus, [can_buffer], timeout=0.1)
	except BaseException as e:
		print("CAN bus error: %s" % e)
		sys.exit(1)
	

def toObj(id, data):
	obj = {}
	obj["id"] = id
	obj["data"] = data
	return obj

def sendObj(obj):
	messages.append(obj)

def canRx():
	if not app.config['FEATURE']['can']:
		while True:
			socketio.sleep(1)
			id = str(random.randint(1, 6))
			if random.randint(0, 1):  
				store.update("rittal_"+"Drehi"+"_"+id, "off")
				socketio.emit('plugStatus',{'leiste': "Drehi",'plug':  id,'status':  "off"},broadcast=True, namespace='/labnet')
			else:
				store.update("rittal_"+"Drehi"+"_"+id, "on")
				socketio.emit('plugStatus',{'leiste': "Drehi",'plug':  id,'status':  "on"},broadcast=True, namespace='/labnet')
	pass

def canTx():
	while True:
		time.sleep(0.1)
		try:
			# 01 F 01 031     00 0C 01 02 02 02 02 02
			obj = messages.pop()
			if app.config['FEATURE']['can']:
				bus.send(can.Message(extended_id=True, arbitration_id=obj["id"], data=obj["data"]))
			else:
				print("Sending CAN message with arbitration id %s and data %s" % (format(obj["id"], '#04x'), hexlify(obj["data"])))
		except IndexError:
			pass

def dummyData():
	while True:
		time.sleep(1)
		data = bytearray(b'\x00\x0C\x01\x02\x02\x02\x02\x02')
		sendObj(toObj(0x01F01031, data))
		sendObj(toObj(0x01F01123, data))
		sendObj(toObj(0x01F01AAA, data))

def start_threads():
	thread_rx 			= threading.Thread(target=canRx)
	thread_rx.daemon 	= False
	thread_rx.start()
	thread_tx 			= threading.Thread(target=canTx)
	thread_tx.daemon 	= False
	thread_tx.start()
	if False: #not app.config['FEATURE']['can']:
		thread_dummy 			= threading.Thread(target=dummyData)
		thread_dummy.daemon 	= True
		thread_dummy.start()