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

if app.config['FEATURE']["influxdb"]:
    from labnetapp import canMetrics
    msgMetrics = deque([])

msgTX = deque([])
msgRX = deque([])

bus = None
  
def print (asd):
    syslog.syslog(str(asd))

def connectCan():
    global bus
    if app.config['FEATURE']['can']:
        try:
            bus = can.ThreadSafeBus(app.config['CAN']['interface'], bustype=app.config['CAN']['type'], bitrate=500000, receive_own_messages=True)
            # can_buffer = can.BufferedReader()
            # notifier = can.Notifier(bus, [can_buffer], timeout=0.1)
            print("CAN bus connected")
            return True
        except BaseException as e:
            # print("CAN bus error: %s" % e)
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
                if app.config['FEATURE']["influxdb"]:
                    msgMetrics.append(message)
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

def rxToMetrics():
    metric = canMetrics.canMetrics(app.config['INFLUXDB'])
    prctl.set_name("rxToMetrics")
    ts = time.time()
    while True:
        if(ts+1 < time.time()):
            metric.calc()
            ts=ts+1
        try:
            if len(msgMetrics) > 0:
                message = msgMetrics.pop()
                if message is not None:
                    obj = canObj.canObj()
                    obj.readMsg(message)
                    metric.put(obj)
        except Exception as err:
            print("rxToMetrics" + " " + str(err))

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

# APP 
# /steckdosen
@app.route('/steckdosen')
def steckdosen():
    debug = ""
    print(getOnlyActiveStripNamesSortedJson())
    return render_template('powerplugsOverview.html',strips=getOnlyActiveStripNamesSortedJson(),plugs=getAllPlugsJson(),debug=debug)

@app.route('/', methods=('GET', 'POST'))
@app.route('/index')
def index():
    return render_template('index.html')

def reqRittalStatusFromAll():
    bus.send(can.Message(extended_id=True, arbitration_id=0x00000001, data=b"ASDF1234"))


ret = connectCan()
if isinstance(ret, BaseException):
    print("CAN bus error: %s" % ret)
    sys.exit(1)

if app.config['FEATURE']['can']:
    def start_threads():
        loadConfig()

        # working who sends received can signals to frontend
        thread_rxToSocket = Greenlet.spawn(rxToSocket)

        # real Threads!!! No Frontend stuff here!
        if app.config['FEATURE']["influxdb"]:
            start_new_thread(rxToMetrics, ())
        start_new_thread(canRx, ())
        start_new_thread(canTx, ())
        time.sleep(0.3)

        reqRittalStatusFromAll()

