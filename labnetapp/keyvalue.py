from subprocess import *
import os,sys

class KeyValue(object):

	store_mongo = False
	store_redis = False
	mongo_values = {}
	values = {}
	redis_values = {}

	def __init__(self, mongo = True, redis = False):
		self.store_mongo = mongo
		self.store_redis = redis
		if(mongo):
			import pymongo
			self.mongo = pymongo.MongoClient()
			#mongo = MongoClient('mongodb://localhost:27017/')
			self.mongo_db = self.mongo.rallye
			self.mongo_values = self.mongo_db.values
		if(redis):
			import redis
			self.redis_values = redis.StrictRedis(host='localhost', port=6379, db=0,decode_responses=True)
	
	def update(self, key, value):
		if(self.store_mongo):
			self.mongo_values.update({'key':key},{"key": key,"value":value},True)
		elif(self.store_redis):
			self.redis_values.set(key, value)
			#print("store redis: " + key +" + " + value)
			#print "redis: " + key + " " + str(value)
		else:
			self.check_key(key)
			#print("store local: " + key +" + " + value)
			self.values[key] = value
	
	def select(self, key):
		try:
			self.check_key(key)
			if(self.store_mongo):
				s = self.mongo_values.find_one({"key":key})
				if s:
					return s["value"]
				else:
					return "empty"
			elif(self.store_redis):
				s = self.redis_values.get(key)
				if s:
					#print "redis: " + key + " " + str(s)
					return s
				else:
					#print "redis: no value for" + key
					return "empty"
			else:
				if key in self.values:
					return self.values[key]
				else:
					return "empty"
		except:
			print("what?!")
			print(sys.exc_info())

	def check_key(self,key):
		if not key in self.values:
			self.values[key] = "empty"