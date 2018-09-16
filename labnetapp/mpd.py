#from flask import Flask, render_template, flash, request, redirect, url_for, session, escape, g
#from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
#from labnetapp import app, socketio
#import mpd
#import os,serial,time,sys,psutil,threading,redis,random
#from subprocess import *
#from _thread import start_new_thread
#
##import gevent
##from gevent import Greenlet
#
## use_unicode will enable the utf-8 mode for python2
## see https://python-mpd2.readthedocs.io/en/latest/topics/advanced.html#unicode-handling
#client = mpd.MPDClient(use_unicode=True)
#
#def connect():
#	client.connect(app.config['MPD']["server"], 6600)
#connect()
#
#def ping():
#	try:
#		client.ping()
#	except mpd.ConnectionError:
#		connect()
#
#for key, value in client.status().items():
#	if key == "volume":
#		volume = value
#store.update("mpd_volume", volume)
#
#song = "no song"
#volume = 0
#status = ""
#playlist = [{}]
#
## thread
#def status():
#	global volume, song, status, playlist
#	while True:
#		try:
#			#socketio.sleep(0)
#			song = client.currentsong()
#			for key, value in client.status().items():
#				if key == "volume":
#					volume = value
#				if key == "state":
#					state = value
#				if key == "song":
#					song = value
#			#for value in client.playlist():
#			playlist = client.playlistinfo()
#			#print(playlist)
#			#print(value)
#			store.update("mpd_volume", volume)
#			store.update("mpd_song", song)
#			store.update("mpd_state", state)
#			#socketio.emit('status',{"song": song, "volume": volume, "state": state},broadcast=True, namespace='/mpd')
#		except mpd.ConnectionError:
#			connect()
#
#@app.before_request
#def before_req():
#    g.target = request.args.get('target', 'default')
#
#@socketio.on('mpdPlay', namespace='/mpd')
#def test_message(message):
#	ping()
#	client.play()
#	print("play")
#  
#@socketio.on('mpdPause', namespace='/mpd')
#def test_message(message):
#	ping()
#	client.stop()
#	print("pause")  
#
#@socketio.on('mpdPrev', namespace='/mpd')
#def test_message(message):
#	ping()
#	client.previous()
#	print("prev")  
#
#@socketio.on('mpdNext', namespace='/mpd')
#def test_message(message):
#	ping()
#	client.next()
#	print("next")  
#
#@socketio.on('mpdMinus', namespace='/mpd')
#def test_message(message):
#	ping()
#	volume = int(store.select("mpd_volume"))-2
#	client.setvol(volume)
#	store.update("mpd_volume", str(volume))
#	print("next")  
#
#@socketio.on('mpdPlus', namespace='/mpd')
#def test_message(message):
#	ping()
#	volume = int(store.select("mpd_volume"))+2
#	client.setvol(volume)
#	store.update("mpd_volume", str(volume))
#	print("next") 
#
#@app.route('/mpd')
#def mpd():
#	global playlist
#	print(playlist)
#	return render_template('mpd.html',playlist=playlist)
#
#def start_threads():
#	#thread_rx  = Greenlet.spawn(status)
#	ping()
#	start_new_thread(status,())#