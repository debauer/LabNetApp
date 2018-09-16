# <!-- NOT IN USAGE UNTIL NOW!!! d.bauer -->

#!/usr/bin/python
#
# Autor: David 'debauer' Bauer
# www.debauer.net
# 
# Part of the FabLab Karlsruhe e.V. LabNet (lab automation and integration)
#
# Status: Tested
#

#from flask import Flask, render_template, flash, request, redirect, url_for, session, escape
#from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
#from labnetapp import app, socketio, store 
#import mpd
#import os,serial,time,sys
#
#app = Flask(__name__)
#
#server = "localhost:9999"
#mpd_folder = "/srv/public/Nutzer/"
#playlist_folder = "David_Bauer/temp_playlist/"
#
#def gproxy_get_qry_raw(raw):
#	return "http://" + server + "/"+ raw
#
#def gproxy_get_qry(t="artist",artist="",album=""):
#	s = "http://" + server + "/get_by_search?type="+ t + "&num_tracks=" + str(num)
#	if artist:
#		s = s + "&artist=" + artist 
#	if album:
#		s = s + "&album=" + album 
#	return s
#
#def gproxy_get(artist,album):
#	return "http://" + server + "/get_by_search?type=album&artist=" + artist + "&title=" + album
#
#def gproxy_get_artist(artist):
#	return "http://" + server + "/get_by_search?type=artist&artist=" + artist
#
#def gproxy_get_radio(artist,num):
#	#http://localhost:9999/get_new_station_by_search?type=artist&artist=Queen&num_tracks=100
#	return "http://" + server + "/get_new_station_by_search?type=artist&artist=" + artist + "&num_tracks=" + str(num)
#
#def cmd_run(cmd):
#	p = Popen(cmd, shell=True, stdout=PIPE)
#	output = p.communicate()[0]
#	return output
#
#def playlist_safe(m3u,filename):
#	text_file = open(mpd_folder + playlist_folder + filename, "w")
#	text_file.write(m3u)
#	text_file.close()
#	return m3u
#
#def filename_random():
#	return str(time.time()).replace(".","")  + ".m3u"
#
#def mpc_helper(fn,clear=True):
#	if clear == True:
#		cmd_run("mpc clear")
#	cmd_run("mpc load " + playlist_folder + fn)
#	cmd_run("mpc play")
#	return m3u, 201
#
#@app.route('/play/album/<string:artist>/<string:album>', methods=['get'])
#def play_album(artist, album):
#	filename = filename_random()
#	m3u = playlist_safe(cmd_run("curl -s '" + gproxy_get(quote(artist),quote(album)) + "'"),filename)
#	return m3u, mpc_helper(filename)
#
#@app.route('/add/album/<string:artist>/<string:album>', methods=['get'])
#def add_album(artist, album):
#	filename = filename_random()
#	m3u = playlist_safe(cmd_run("curl -s '" + gproxy_get(quote(artist),quote(album)) + "'"),filename)
#	return m3u, mpc_helper(filename,False)
#
#@app.route('/add/artist/<string:artist>', methods=['get'])
#def add_artist(artist):
#	filename = filename_random()
#	m3u = playlist_safe(cmd_run("curl -s '" + gproxy_get_artist(quote(artist)) + "'"),filename)
#	return m3u, mpc_helper(filename,False)
#
#@app.route('/play/artist/<string:artist>', methods=['get'])
#def play_artist(artist):
#	filename = filename_random()
#	m3u = playlist_safe(cmd_run("curl -s '" + gproxy_get_artist(quote(artist)) + "'"),filename)
#	return m3u, mpc_helper(filename)
#
#@app.route('/add/radio/<string:artist>', methods=['get'])
#def add_radio(artist):
#	filename = filename_random()
#	m3u = playlist_safe(cmd_run("curl -s '" + gproxy_get_radio(quote(artist),100) + "'"),filename)
#	return m3u, mpc_helper(filename,False)
#
#@app.route('/play/radio/<string:artist>', methods=['get'])
#def play_radio(artist):
#	filename = filename_random()
#	m3u = playlist_safe(cmd_run("curl -s '" + gproxy_get_radio(quote(artist),100) + "'"),filename)
#	return m3u, mpc_helper(filename)
#
##if __name__ == '__main__':
##	#app.run(host="192.168.3.184",port=5002,debug=True)
##	app.run(host="192.168.1.6",port=5003,debug=True)
##	#app.run(port=5002,debug=True)#