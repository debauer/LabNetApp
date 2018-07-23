#!/usr/bin/python
from flask import Flask, render_template, flash, request, redirect, url_for, session, escape
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from labnetapp import app, socketio, store 
from os import listdir
from os.path import isfile, join
import os, json


@socketio.on('sendButton', namespace='/labnet')
def test_message(message):
    print(message)
    if message["status"] == "on":  
        store.update("rittal_"+message["leiste"]+"_"+message["plug"], "off")
        emit('plugStatus',{'leiste': message["leiste"],'plug':  message["plug"],'status':  "off"},broadcast=True, namespace='/labnet')
    else:
        store.update("rittal_"+message["leiste"]+"_"+message["plug"], "on")
        emit('plugStatus',{'leiste': message["leiste"],'plug':  message["plug"],'status':  "on"},broadcast=True, namespace='/labnet')
    

@app.route('/', methods=('GET', 'POST'))
@app.route('/index')
def index():
    strips = []
    plugs={}
    debug = ""
    default = {"name": "unused","description": "unused","onOff": 0, "onOn": 1,"default": 0,"changeable": 0}
    with open(app.config['NODE_CONFIG'], 'r') as read_file:
        data = json.load(read_file)
    for s in data['strips']:
        for value in s:
            strips.append(value)
    for p in data['plugs']:
        for value in p:
            strip = p[value]["strip"]
            id = p[value]["id"]
            debug = debug + value
            if not strip in plugs:
                plugs[ strip ] = [default,default,default,default,default,default]
            plugs[ strip ][ id-1 ] = p[value]
            sv = store.select("rittal_"+strip+"_"+str(id))
            #print("rittal_"+strip+"_"+str(id))
            if sv != "empty":
                plugs[ strip ][ id-1 ]["status"] = sv
            else:
                plugs[ strip ][ id-1 ]["status"] = "unknown"
    return render_template('index.html',strips=strips,plugs=plugs,debug=debug)