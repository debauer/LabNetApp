#!/usr/bin/env python3
from app import app, labnet, socketio
import os
from flask_socketio import SocketIO

labnet.start_threads()

if __name__ == '__main__':
    socketio.run(app,debug=True, port=app.config['PORT'], host=app.config['IP'])
