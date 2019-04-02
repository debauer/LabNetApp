#!/usr/local/bin/python3.7 -u
from labnetapp import app, socketio, base
import os
from flask_socketio import SocketIO

if __name__ == '__main__':
	base.start_threads()
	#mpd.start_threads()
	socketio.run(app,debug=False, port=app.config['PORT'], host=app.config['IP'])
