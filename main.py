#!/usr/bin/python3 -u
from labnetapp import app, socketio, base, mpd
import os
from flask_socketio import SocketIO


if __name__ == '__main__':
	base.start_threads()
	#mpd.start_threads()
	socketio.run(app,debug=True, port=app.config['PORT'], host=app.config['IP'] ,log_output=True)
	
