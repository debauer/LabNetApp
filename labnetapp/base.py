#!/usr/bin/python

import os, json, sys, can, time, gevent, logging, syslog, prctl
from flask import Flask, render_template, flash, request, redirect, url_for, session, escape
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from labnetapp import app, socketio, canObj
from os import listdir
from os.path import isfile, join
from collections import deque
from _thread import start_new_thread
from binascii import unhexlify, hexlify
from gevent import Greenlet
from flask import request

from nodeConfig import *

def print (asd):
	syslog.syslog(str(asd))

msgTX = deque([])
msgRX = deque([])
bus = None

def getOnlyActiveStripNamesSortedJson():
    data = {}
    for plug_id in plugs:
        if not plugs[plug_id].getStripId() in data.keys():
            #pass
            id = plugs[plug_id].getStripId()
            data[id] = {}
            data[id]["stripId"] = strips[id].getId()
            data[id]["displayText"] = strips[id].getData()["displayText"]  
            data[id]["location"] = strips[id].getData()["location"]  
    return data

def getOnlyActiveStripNamesSorted():
    st = []
    for plug_id in plugs:
        if not plugs[plug_id].getStripId() in st:
            #pass
            st.append(plugs[plug_id].getStripId())
    return st

def getStripNamesSortedJson():
    data = {}
    for n in nodes:
        strip_list = nodes[n].getStripNames()
        for s in strip_list:
            if not s in data.keys():
                data[s] = {}
                data[s]["stripId"] = strips[s].getId()
                data[s]["displayText"] = strips[s].getData()["displayText"]
                data[s]["location"] = strips[s].getData()["location"]
    return data 

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


def connectCan():
    global bus
    if app.config['FEATURE']['can']:
        try:
            #bus = can.interface.Bus(app.config['CAN']['interface'], bustype=app.config['CAN']['type'])
            bus = can.ThreadSafeBus('ws://192.168.1.11:54701/',
                                    bustype='remote', bitrate=500000, receive_own_messages=True)
            #can_buffer = can.BufferedReader()
            #notifier = can.Notifier(bus, [can_buffer], timeout=0.1)
            print("CAN bus connected")
            return True
        except BaseException as e:
            #print("CAN bus error: %s" % e)
            return e


            #sys.exit(1)


### RX #####


def canRx():
    prctl.set_name("canRx")
    while True:
        try:
            message = bus.recv(1)
#            print(message)
            if message is not None:
                msgRX.append(message)
            else:
                time.sleep(0.1)
        #except can.interfaces.remote.protocol.RemoteError as err:
        #   print("canRx",err)
        #   pass
        except Exception as err:
            if "1006" in str(err):
#                print("canRX 1006")
                connectCan()
            else:
                print("canRx" + str( err))


def rxToSocket():
    prctl.set_name("rxToSocket")
    while True:
        dbg = ""
        try:
            if len(msgRX) > 0:
                message = msgRX.pop()
                if message is not None:
                    obj = canObj.canObj()
                    obj.readMsg(message)
                    if obj.arbitration()["eventName"] == "rittal status":
                        print(message)
                    if obj.arbitration()["eventName"] == "rittal status" and obj.arbitration()["msgType"] == 0x04:
                        #print(obj.arbitration()["eventName"])
                        #print(obj.arbitration()["msgType"])
                        adress = obj.handle_power_hub_message()
                        print(adress)
                        plug_nr = 1
                        for plug_address in adress["plugAddresses"]:
                            if plug_address == 1 or plug_address == 0:
                                plug_id = get_plug_id_by_adress(
                                    plug_nr, adress["stripAddress"], adress["nodeAddress"])
                                strip_id = get_strip_id_by_adress(
                                    adress["stripAddress"], adress["nodeAddress"])
                                if plug_address == 1:
                                    status = "on"
                                    if plug_id in plugs.keys():
                                        plugs[plug_id].setOn()
                                elif plug_address == 0:
                                    status = "off"
                                    if plug_id in plugs.keys():
                                        plugs[plug_id].setOff()
                                if plug_id:
                                    #print("found: " + plugName + " " + stripName)
                                    #print({'leiste': stripName,'plug':  plugName,'status':  status})
                                    print({'leiste': strip_id, 'plug':  plug_id,'status':  status})
                                    socketio.emit('plugStatus', { 'plugId':  plug_id,'status':  status}, broadcast=True)
                                    
                            plug_nr += 1
            else:
                gevent.sleep(0.1)
        except IndexError as err:
#            print("indexerror:" + err)
            pass
        except Exception as err:
            print("rxToSocket" + " " + str(err) + " " +str(dbg))
            pass

### TX #####


def canTx():
    prctl.set_name("canTx")
    while True:
        time.sleep(0.1)
        try:
            # 01 F 01 031     00 0C 01 02 02 02 02 02
            obj = msgTX.pop()
            #if app.config['FEATURE']['can']:
            #
            #print("Sending CAN message with arbitration id %s and data %s" % (format(obj["id"], '#04x'), hexlify(obj["data"])))
            bus.send(can.Message(extended_id=True,
                            arbitration_id=obj["id"], data=obj["data"]))
            #print("Sending CAN message with arbitration id %s and data %s" % (format(obj["id"], '#04x'), hexlify(obj["data"])))
        except IndexError:
#            print("canTx: indexError")
            pass
        except Exception as err:
            print("canTx " + str(err))
            connectCan()
            pass

# API

@app.route('/plug/<id>/power', methods=['POST'])
def postFoo(id):
    print(request.data.decode("utf-8"))
    dataDict = json.loads(request.data.decode("utf-8"))
    print(id + dataDict["state"])
    obj = canObj.canObj()
    msg = obj.genPlugChangeMsg(get_plug_adress_by_id(id), dataDict["state"])
    #print(msg)
    msgTX.append(msg)
    return "OK"
    #if status == "on":
    #    store.update("rittal_"+message["leiste"]+"_"+message["plug"], "off")
    #    socketio.emit('plugStatus',{'leiste': message["leiste"],'plug':  message["plug"],'status':  "off"},broadcast=True, namespace='/labnet')
    #else:
    #    store.update("rittal_"+message["leiste"]+"_"+message["plug"], "on")
    #    socketio.emit('plugStatus',{'leiste': message["leiste"],'plug':  message["plug"],'status':  "on"},broadcast=True, namespace='/labnet')

@socketio.on('connect')
def onConnect():
    socketio.emit('plugStatusList', getAllPlugsJson() , broadcast=True)
    
@socketio.on('fetchPlugList')
def onConnect():
    socketio.emit('plugStatusList', getAllPlugsJson() , broadcast=True)

@socketio.on('setPlugPower')
def setPlugPower(message):
    #print(message)
    obj = canObj.canObj()
    if message["status"] == "off":
        newStatus = "on"
    else:
        newStatus = "off"
    msg = obj.genPlugChangeMsg(get_plug_adress_by_id(message["plugId"]), newStatus)
    #print(msg)
    msgTX.append(msg)
    #if message["status"] == "on":
    #    store.update("rittal_"+message["leiste"]+"_"+message["plug"], "off")
    #    socketio.emit('plugStatus',{'leiste': message["leiste"],'plug':  message["plug"],'status':  "off"},broadcast=True, namespace='/labnet')
    #else:
    #    store.update("rittal_"+message["leiste"]+"_"+message["plug"], "on")
    #    socketio.emit('plugStatus',{'leiste': message["leiste"],'plug':  message["plug"],'status':  "on"},broadcast=True, namespace='/labnet')

# APP 
# /steckdosen
@app.route('/steckdosen')
def steckdosen():
    debug = ""
    print(getOnlyActiveStripNamesSortedJson())
    return render_template('powerplugsOverview.html',strips=getOnlyActiveStripNamesSortedJson(),plugs=getAllPlugsJson(),debug=debug)

# API
# returns the complete labnet config file 
@app.route('/config')
def nodeConfig():
    f = open("nodeConfig/mainv2.json", 'r').read()
    #print(getAllPlugsJson())
    return f

# API
# reloads config
@app.route('/configreload')
def nodeConfigReload():
    loadConfig()
    reqRittalStatusFromAll()
    return "OK"


@app.route('/', methods=('GET', 'POST'))
@app.route('/index')
def index():
    return render_template('index.html')

def reqRittalStatusFromAll():
    #  EVENT_GlOBAL_RITTAL_UPDATE 0x000001
    #  TT_EVENT_GLOBAL      0x00
    bus.send(can.Message(extended_id=True, arbitration_id=0x00000001, data=b"ASDF1234"))

def loadConfig():
    print("loadConfig: destroyObjects()")
    destroyObjects()
    print("loadConfig: load_definition_file(\"nodeConfig/mainv2.json\")")
    load_definition_file("nodeConfig/mainv2.json")

ret = connectCan()
if isinstance(ret, BaseException):
    print("CAN bus error: %s" % ret)
    sys.exit(1)

if app.config['FEATURE']['can']:
    def start_threads():
        loadConfig()
        #thread_rx  = Greenlet.spawn(canRx)
        #thread_tx = Greenlet.spawn(canTx)
        #thread_rx          = threading.Thread(target=canRx)
        #thread_rx.daemon   = False
        #thread_rx.start()

        # working who sends received can signals to frontend
        thread_rxToSocket = Greenlet.spawn(rxToSocket)
        #thread_rx          = threading.Thread(target=rxToSocket)
        #thread_rx.daemon   = False
        #thread_rx.start()

        # real Threads!!! No Frontend stuff here!
        start_new_thread(canRx, ())
        start_new_thread(canTx, ())
        time.sleep(0.3)

        reqRittalStatusFromAll()

#        logging.getLogger('socketio').setLevel(logging.DEBUG)
#        logging.getLogger('engineio').setLevel(logging.DEBUG)
#        logging.getLogger('gevent').setLevel(logging.DEBUG)
#        ll = logging.getLogger().manager.loggerDict.keys()
#        for l in ll:
#            print("set log of " + l + " on DEBUG")
#           logging.getLogger(l).setLevel(logging.DEBUG)

