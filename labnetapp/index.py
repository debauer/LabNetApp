#!/usr/bin/python
from flask import Flask, render_template, flash, request, redirect, url_for, session, escape
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from labnetapp import app, socketio, store 
from os import listdir
from os.path import isfile, join
import os, json

@app.route('/', methods=('GET', 'POST'))
@app.route('/index')
def index():
    return render_template('index.html')