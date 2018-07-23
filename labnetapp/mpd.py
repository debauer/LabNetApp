from flask import Flask, render_template, flash, request, redirect, url_for, session, escape
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from labnetapp import app, socketio, store 
import mpd

# use_unicode will enable the utf-8 mode for python2
# see https://python-mpd2.readthedocs.io/en/latest/topics/advanced.html#unicode-handling
client = mpd.MPDClient(use_unicode=True)
client.connect("192.168.1.6", 6600)

for entry in client.lsinfo("/"):
	print("%s" % entry)
for key, value in client.status().items():
	if key == "volume":
		volume = value
print(volume)
store.update("mpd_volume", volume)

@socketio.on('mpdPlay', namespace='/mpd')
def test_message(message):
	client.play()
	print("play")
  
@socketio.on('mpdPause', namespace='/mpd')
def test_message(message):
	client.stop()
	print("pause")  

@socketio.on('mpdPrev', namespace='/mpd')
def test_message(message):
	client.previous()
	print("prev")  

@socketio.on('mpdNext', namespace='/mpd')
def test_message(message):
	client.next()
	print("next")  

@socketio.on('mpdMinus', namespace='/mpd')
def test_message(message):
	volume = int(store.select("mpd_volume"))-2
	client.setvol(volume)
	store.update("mpd_volume", str(volume))
	print("next")  

@socketio.on('mpdPlus', namespace='/mpd')
def test_message(message):
	volume = int(store.select("mpd_volume"))+2
	client.setvol(volume)
	store.update("mpd_volume", str(volume))
	print("next") 