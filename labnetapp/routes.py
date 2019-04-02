from flask import Flask, request
from labnetapp import app
from collections import deque
from nodeConfig import *
from labnetapp.can import reqRittalStatusFromAll

@app.route('/steckdosen')
def steckdosen():
    debug = ""
    print(getOnlyActiveStripNamesSortedJson())
    return render_template('powerplugsOverview.html',strips=getOnlyActiveStripNamesSortedJson(),plugs=getAllPlugsJson(),debug=debug)

@app.route('/', methods=('GET', 'POST'))
@app.route('/index')
def index():
    return render_template('index.html')