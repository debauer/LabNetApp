import os,serial,time,sys,psutil,struct
from binascii import unhexlify, hexlify

def long_to_bytes(val):
	result = []

	for i in range(8):
		result.insert(0, (val & (0xFF << i*8)) >> i*8)	
	return bytearray(result)

class canObj:
	def __init__(self):
		pass

	def genPlugChangeMsg(self, adr, status):
		#logging.debug("Power Dose %s on Leiste %s for hub %s" % (adr["strip"], adr["strip"], adr["hub"]))
		data = 0x01
		if status == 'on':
			data = 0x01
		elif status == 'off':
			data = 0x00
		if not data == 0x02:
			arbitration_id = 0x01F00000
			arbitration_id = arbitration_id + (adr["node"] << 12) + 0x30 + adr["strip"]
	
			status = 0x0000
			for i in range(6-adr["plug"]):
				status = status + (0x02 << i * 8)
			status = status + (data << (6 - adr["plug"]) * 8)
			for i in range(adr["plug"]-1):
				status = status + (0x02 << (5 - i) * 8)
		return {"data": long_to_bytes(status), "id": arbitration_id}

	def readMsg(self,msg):
		self.arbitrationId = msg.arbitration_id
		self.data = msg.data
		self.dataStr = self.dataHex(" ")

		self.nodeId  = (self.arbitrationId & 0x000FF000) >> 12
		self.nodeType = (self.arbitrationId & 0x00F00000) >> 20
		if self.nodeType == 0x0: # Bridge
			self.nodeTypeName = "Bridge"
		elif self.nodeType == 0x1:  # Basis
			self.nodeTypeName = "Basis"
		elif self.nodeType == 0xF:  # Power-Hub
			self.nodeTypeName = "Power-Hub"
		else:	
			self.nodeTypeName = "Unknown"
		self.msgType = (self.arbitrationId & 0xFF000000) >> 24

		self.eventId = (self.arbitrationId & 0x00000FFF) >> 0
		self.eventName = "Unknown"
		if self.eventId == 0x01:
			self.eventName = "startup"
			self.dataStr = self.dataASCII()
		if self.eventId == 0x02:
			self.eventName = "startup"
			self.dataStr = self.dataASCII()
		if self.eventId == 0x20:
			self.eventName = "fuse status"
			#self.dataStr = self.dataASCII()

		if self.eventId < 0x40 and self.eventId > 0x30:
			self.eventName = "rittal status"

	def __str__(self):
		return str(self.nodeTypeName) + " event:" + self.eventName + " id=" + str(self.nodeId) + " data=" + self.dataStr
	# return hex string

	def arbitration(self):
		return {"msgType": self.msgType, "eventId": self.eventId, "eventName": self.eventName, "nodeId": self.nodeType, "nodeTypeName": self.nodeTypeName}

	def event(self):
		return {"id": self.eventId, "name": self.eventName}

	def dataHex(self, seperator=""):
		str = ""
		for x in self.data:
			str += '{:02X}'.format(x) + seperator
		return str

	# return ascii string
	def dataASCII(self):
		return self.data.decode()

	def powerPlugs(self):
		dose = []
		#print(self.data)
		#dose.append(int(self.data & 0x0000FF0000000000) >> 40))
		#dose.append(int(self.data & 0x000000FF00000000) >> 32))
		#dose.append(int(self.data & 0x00000000FF000000) >> 24))
		#dose.append(int(self.data & 0x0000000000FF0000) >> 16))
		#dose.append(int(self.data & 0x000000000000FF00) >>  8))
		#dose.append(int(self.data & 0x00000000000000FF) >>  0))
		return dose

	def handle_power_hub_message(self):
		node_id  = (self.arbitrationId & 0x000FF000) >> 12
		event_id = (self.arbitrationId & 0x00000FFF) >> 0
		steckdosen_id  = (self.arbitrationId & 0x0000000F) >> 0
		if event_id <= 0x30 or event_id > 0x39:
			return
		dosen = []
		for i in range(2,8):
			dosen.append(self.data[i])
		return {"plugs": dosen, "strip": steckdosen_id, "node": node_id}

		#logging.debug("CAN Payload: %s" % format(data, '#02x'))

		#min_amp = (self.data & 0xFF00000000000000) >> 56
		#max_amp = (self.data & 0x00FF000000000000) >> 48
		#print(min_amp)
		#print(max_amp)

		#logging.debug("min amp %s" % min_amp)
		#logging.debug("max amp %s" % max_amp)

		

		#for i in range(6):
		#	topic = create_mqtt_stat_topic(steckdosen_id, i + 1)
		#	payload = payload_from_power_msg(dose[i])
		#	if payload:
		#send_mqtt_message(mqtt_client, topic, payload)