#!/usr/bin/python
from flask import Flask, render_template, flash, request, redirect, url_for, session, escape
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from app import app, socketio
from os import listdir
from os.path import isfile, join
import os, json


@socketio.on('sendButton', namespace='/can')
def test_message(message):
    print(message)
    if message["status"] == "on":
        emit('setButton',{'leiste': message["leiste"],'plug':  message["plug"],'status':  "off"})
    else:
        emit('setButton',{'leiste': message["leiste"],'plug':  message["plug"],'status':  "on"})
    

@app.route('/', methods=('GET', 'POST'))
@app.route('/index')
def index():
    strips = []
    plugs={}
    debug = ""
    default = {"name": "unused","description": "unused","onOff": 0, "onOn": 1,"default": 0,"changeable": 0}
                
    #flash('critical message', 'critical')
    #flash('error message', 'error')
    #flash('warning message', 'warning')
    #flash('info message', 'info')
    #flash('debug message', 'debug')
    #flash('different message', 'different')
    #flash('uncategorized message')
    #if redis.get("counter"):
    #    c = int(redis.get("counter"))
    #else:
    #    c = 1
    #redis.set("counter", c+1)
    #return render_template('index.html') #, counter = c+1)
    with open(app.config['NODE_CONFIG'], 'r') as read_file:
        data = json.load(read_file)
    for s in data['strips']:
        for value in s:
            strips.append(value)
    for p in data['plugs']:
        for value in p:
            debug = debug + value
            if p[value]["strip"] in plugs:
                plugs[ p[value]["strip"] ][ p[value]["id"]-1 ] = p[value]
            else:
                plugs[ p[value]["strip"] ] = [default,default,default,default,default,default]
                plugs[ p[value]["strip"] ][ p[value]["id"]-1 ] = p[value]
    return render_template('index.html',strips=strips,plugs=plugs,debug=debug)