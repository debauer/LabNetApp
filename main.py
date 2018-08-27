#!/usr/bin/env python3
from labnetapp import app, socketio, can_handler, mpd
import os
from flask_socketio import SocketIO

if __name__ == '__main__':
	can_handler.start_threads()
	mpd.start_threads()
	socketio.run(app,debug=False, port=app.config['PORT'], host=app.config['IP'],log_output=True)
	
