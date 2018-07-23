#!/usr/bin/env python3
from labnetapp import app, labnet, socketio, can_handler
import os
from flask_socketio import SocketIO


if __name__ == '__main__':
	labnet.start_threads()
	can_handler.start_threads()
	socketio.run(app,debug=True, port=app.config['PORT'], host=app.config['IP'])
	
