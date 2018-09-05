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
    data = getAllPlugsJson()
    for plugName in plugs:
        if not plugs[plugName].getStrip() in st:
            #pass
            st.append( plugs[plugName].getStrip())
    return st

def getStripNamesSorted():
    listOfStrips = []
    for n in nodes:
        stripList = nodes[n].getStripNames()
        for s in stripList:
            listOfStrips.append(s) 
    listOfStrips.sort()
    return listOfStrips  

def getAllPlugsJson():
    data = {}
    for plugName in plugs:
        stripName = plugs[plugName].getStrip()
        if not stripName in data.keys():
            data[stripName] = []
            #plugs[plugName].getData()
        data[stripName].append(plugs[plugName].getData())
        sorted(data[stripName], key=lambda x:sorted(x.keys()))
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