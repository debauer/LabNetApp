
import can
import os,serial,time,sys,psutil,threading,redis,random
from subprocess import *
from labnetapp import app, store,socketio,canObj
from binascii import unhexlify, hexlify
from collections import deque
from _thread import start_new_thread
import logging, gevent
from gevent import Greenlet

#import gevent
#from gevent import Greenlet

from nodeConfig import *
msgTX = deque([])
msgRX = deque([])

if app.config['FEATURE']['can']:
	try:
		#bus = can.interface.Bus(app.config['CAN']['interface'], bustype=app.config['CAN']['type'])
		bus = can.Bus('ws://192.168.1.11:54701/', bustype='remote', bitrate=500000, receive_own_messages=True)
		#can_buffer = can.BufferedReader()
		#notifier = can.Notifier(bus, [can_buffer], timeout=0.1)
	except BaseException as e:
		print("CAN bus error: %s" % e)
		sys.exit(1)


### RX #####

def canRx():
	while True:
		time.sleep(0.1)
		message = bus.recv(1)
		#print(message)
		if message is not None:
			msgRX.append(message)

def rxToSocket():
	while True:
		try:
			gevent.sleep(0.1)
			if len(msgRX) > 0:
				message = msgRX.pop()
				if message is not None:
					#print(message)
					obj = canObj.canObj()
					obj.readMsg(message)
					if obj.arbitration()["eventName"] == "rittal status" and obj.arbitration()["msgType"] == 0x04:
						#print(obj.arbitration()["eventName"])
						#print(obj.arbitration()["msgType"])
						adress = obj.handle_power_hub_message()
						print(adress)
						plugNr = 1
						for plug in adress["plugs"]:
							if plug == 1 or plug == 0:
								if plug == 1:
									status = "on"
								elif plug == 0:
									status = "off"
								plugName = getPlugNameByAdress(plugNr,adress["strip"],adress["node"])
								stripName = getStripNameByAdress(adress["strip"],adress["node"])
								if plugName:
									#print("found: " + plugName + " " + stripName)
									print({'leiste': stripName,'plug':  plugName,'status':  status})
									socketio.emit('plugStatus',{'leiste': stripName,'plug':  plugName,'status':  status},broadcast=True, namespace='/labnet')		
							plugNr += 1	
		except IndexError as err:
			print(err)
			pass
	
### TX #####

def canTx():
	while True:
		time.sleep(0.1)
		try:
			# 01 F 01 031     00 0C 01 02 02 02 02 02
			obj = msgTX.pop()
			#if app.config['FEATURE']['can']:
			#	
			#print("Sending CAN message with arbitration id %s and data %s" % (format(obj["id"], '#04x'), hexlify(obj["data"])))
			bus.send(can.Message(extended_id=True, arbitration_id=obj["id"], data=obj["data"]))
			#print("Sending CAN message with arbitration id %s and data %s" % (format(obj["id"], '#04x'), hexlify(obj["data"])))
		except IndexError:
			pass

@socketio.on('sendButton', namespace='/labnet')
def test_message(message):
	#print(message)
	obj = canObj.canObj()
	if message["status"] == "off":
		newStatus = "on"
	else:
		newStatus = "off"
	msg = obj.genPlugChangeMsg(getPlugAdressByName(message["name"]),newStatus)
	#print(msg)
	msgTX.append(msg)
	#if message["status"] == "on":  
	#    store.update("rittal_"+message["leiste"]+"_"+message["plug"], "off")
	#    socketio.emit('plugStatus',{'leiste': message["leiste"],'plug':  message["plug"],'status':  "off"},broadcast=True, namespace='/labnet')
	#else:
	#    store.update("rittal_"+message["leiste"]+"_"+message["plug"], "on")
	#    socketio.emit('plugStatus',{'leiste': message["leiste"],'plug':  message["plug"],'status':  "on"},broadcast=True, namespace='/labnet')

if app.config['FEATURE']['can']:
	def start_threads():
		#thread_rx  = Greenlet.spawn(canRx)
		#thread_tx = Greenlet.spawn(canTx)
		#thread_rx 			= threading.Thread(target=canRx)
		#thread_rx.daemon 	= False
		#thread_rx.start()



		# working who sends received can signals to frontend
		thread_rxToSocket = Greenlet.spawn(rxToSocket )
		#thread_rx 			= threading.Thread(target=rxToSocket)
		#thread_rx.daemon 	= False
		#thread_rx.start()
	
		# real Threads!!! No Frontend stuff here!
		start_new_thread(canRx,())
		start_new_thread(canTx,())
		logging.getLogger('socketio').setLevel(logging.DEBUG)
		logging.getLogger('engineio').setLevel(logging.DEBUG)