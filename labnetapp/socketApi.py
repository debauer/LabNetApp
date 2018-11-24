from flask import Flask, request
from labnetapp import app, socketio
from collections import deque
from nodeConfig import *
from labnetapp.base import reqRittalStatusFromAll

@socketio.on('connect')
def onConnect():
    socketio.emit('plugStatusList', getAllPlugsJson() , broadcast=True)
    
@socketio.on('fetchPlugList')
def onConnect():
    socketio.emit('plugStatusList', getAllPlugsJson() , broadcast=True)

@socketio.on('setPlugPower')
def setPlugPower(message):
    obj = canObj.canObj()
    if message["status"] == "off":
        newStatus = "on"
    else:
        newStatus = "off"
    msg = obj.genPlugChangeMsg(get_plug_adress_by_id(message["plugId"]), newStatus)
    base.msgTX.append(msg)