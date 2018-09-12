#!/usr/bin/python
from flask import Flask, render_template, flash, request, redirect, url_for, session, escape
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from labnetapp import app, socketio, store
from os import listdir
from os.path import isfile, join
import os, json

from nodeConfig import *

def getOnlyActiveStripNamesSorted():
    st = []
    for plug_id in plugs:
        if not plugs[plug_id].getStripId() in st:
            #pass
            st.append(plugs[plug_id].getStripId())
    return st

def getStripNamesSorted():
    list_of_strips = []
    for n in nodes:
        strip_list = nodes[n].getStripNames()
        for s in strip_list:
            list_of_strips.append(s)
    list_of_strips.sort()
    return list_of_strips

def getAllPlugsJson():
    data = {}
    for plug_id in plugs:
        strip_id = plugs[plug_id].getStripId()
        if not strip_id in data.keys():
            data[strip_id] = []
            #plugs[plugId].getData()
        data[strip_id].append(plugs[plug_id].getData())
        sorted(data[strip_id], key=lambda x:sorted(x.keys()))
    return data

# /steckdosen
# status der Steckdosen kommt aus KeyValue
# wenn kein status vorhanden sind sie grau
# beim bootup der application sollte an alle nodes ein "gib mir mal deine steckdosen stati pls" gesendet werden.
# Dann ist wenige sekunden nach startup die app aktualisiert.
@app.route('/steckdosen')
def steckdosen():
    debug = ""
    #print(getAllPlugsJson())
    return render_template('steckdosen.html',strips=getOnlyActiveStripNamesSorted(),plugs=getAllPlugsJson(),debug=debug)


@app.route('/config')
def nodeconfig():
    f = open("nodeConfig/mainv2.json", 'r').read()
    #print(getAllPlugsJson())
    return f