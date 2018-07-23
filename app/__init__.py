#!/usr/bin/env python3
import os, json, sys
from flask import Flask , render_template, flash
from flask_appconfig import AppConfig
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO

app = Flask(__name__)
AppConfig(app,None)
Bootstrap(app)
socketio = SocketIO(app)

conf = json.loads(open('config.json').read())

# in a real app, these should be configured through Flask-Appconfig
app.config['SECRET_KEY'] 			= 'devkey'
app.config['RECAPTCHA_PUBLIC_KEY'] 	= '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'


app.config['BASE_FOLDER'] 		 	= conf['main']['folder']
app.config['CAN_LOG_FOLDER'] 		= conf['main']['folder'] + "/" + conf['can']['logFolder']
app.config['FEATURE']				= conf['feature']
app.config['CAN']				= conf['can']

app.config['PORT']					= int(conf["main"]['port'])
app.config['IP']					= conf["main"]['ip']

app.config['NODE_CONFIG']			= conf['main']['folder'] + "/node_config"  + "/" + conf["can"]['config']

if conf['feature']['com'] :
	app.config['COM'] 					= {}
	app.config['COM']['port']			= conf['com']['port']
	app.config['COM']['baud']			= conf['com']['baud']
	app.config['COM']['timeout']		= 1

from app import index
from app import journal
from app import config
from app import can_log
from app import can_handler
from app import csv_wrapper
from app import labnet
from app import keyvalue as kv

keyvalue 	= kv.KeyValue(mongo=False,redis=app.config['FEATURE']['redis'] )