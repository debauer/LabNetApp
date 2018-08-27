#!/usr/bin/env python3
import os, json, sys#, queue
from flask import Flask , render_template, flash
from flask_appconfig import AppConfig
#from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO

app = Flask(__name__)
AppConfig(app,None)
#Bootstrap(app)
socketio = SocketIO(app)

#msgQ = queue.Queue()

conf = json.loads(open('config.json').read())

# in a real app, these should be configured through Flask-Appconfig
app.config['SECRET_KEY'] 			= 'devkey'
app.config['RECAPTCHA_PUBLIC_KEY'] 	= '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'


app.config['BASE_FOLDER'] 		 	= conf['main']['folder']
app.config['FEATURE']				= conf['feature']

app.config['PORT']					= int(conf["main"]['port'])
app.config['IP']					= conf["main"]['ip']

app.config['NODE_CONFIG'] = conf['main']['folder'] + "/node_config"  + "/" + conf["can"]['config']

from labnetapp import keyvalue as kv
store = kv.KeyValue(mongo=False,redis=app.config['FEATURE']['redis'] )

from labnetapp import index
from labnetapp import config
if app.config['FEATURE']["can"]:
	app.config['CAN'] = conf['can']
	from labnetapp import canObj
	from labnetapp import can_handler
	if app.config['FEATURE']["canLog"]:
		app.config['CAN_LOG_FOLDER'] = conf['main']['folder'] + "/" + conf['can']['logFolder']
		from labnetapp import can_log

if app.config['FEATURE']["mpd"]:
	app.config['MPD'] = conf['mpd']
	from labnetapp import mpd
	if app.config['FEATURE']["gmusic"]:
		app.config['GMUSIC'] = conf['gmusic']
		from labnetapp import gmusic
from labnetapp import steckdosen


