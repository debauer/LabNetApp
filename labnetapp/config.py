##!/usr/bin/python
#from flask import Flask, render_template, flash, request, redirect, url_for, session, escape
#from labnetapp import app
#from werkzeug import secure_filename
#import redis, os
#from os import listdir
#from os.path import isfile, join
#import os.path
#import time
#from stat import *
#import csv, threading
#from operator import itemgetter
#from subprocess import *
#import json
#
#ALLOWED_EXTENSIONS = set(['json'])
#
#status = {}
#status["load"] = False
#status["text"] = ""
#status["file"] = ""
#status["flash-class"] = "success"
# 
#def allowed_file(filename):
#    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
#
#def upload(request):
#    f = request.files['file']
#    if f and allowed_file(f.filename):
#        filename = secure_filename(f.filename)
#        f.save(os.path.join(app.config['NODE_CONFIG_FOLDER'], filename))
#        flash(filename + ' uploadet', 'info')
#        return redirect(url_for('configs'))
#    else:
#        flash('file has no valid format', 'critical')
#
#
#def get_file(d):
#    ff = [ f for f in listdir(d) if isfile(join(d,f)) ]
#    files = []
#    for f in ff:
#        stat = os.stat(d+"/"+f)
#        files.append({"name":f, "date": time.asctime(time.localtime(stat[ST_MTIME]))})
#        files = sorted(files, key=itemgetter('date'), reverse=True)
#    return files
#
#
## läd config aus file und schreibt sie an die HW raus. 
## background thread der darauf wartet das status["load"] true wird
#def loadConfigWorker():
#    while(True):
#        if(status["load"]):
#            if(status["file"] != ""):
#                conf = json.loads(open(app.config['NODE_CONFIG_FOLDER'] + "/" + status["file"]).read())
#                for p in conf['parameter']:
#                    labnet.send("paramter "+str(conf['parameter'][p]["adresse"])+" "+str(conf['parameter'][p]["value"]))
#            status["load"] = False
#
#
#def loadConfigFlash():
#    if(status["load"]):
#        flash(status["text"], status["flash-class"])
#
#@app.route('/config', methods=('GET', 'POST'))
#def configs():
#    loadConfigFlash()
#    ac = open(app.config['NODE_CONFIG_FOLDER']+"/main.json", 'r')
#    active_config = ac.read()
#    active_config = active_config.replace("\n","<br>")
#    active_config = active_config.replace("\t","&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
#    files = get_file(app.config['NODE_CONFIG_FOLDER'])
#    if request.method == 'POST':
#        return upload(request)
#    return render_template('configs.html',files=files, active_config=active_config)
#
#@app.route('/config/show/<filename>', methods=('GET', 'POST'))
#def showConfig(filename):
#    loadConfigFlash()
#    ac = open(app.config['NODE_CONFIG_FOLDER'] + "/" + filename, 'r')
#    active_config = ac.read()
#    active_config = active_config.replace("\n","<br>")
#    active_config = active_config.replace("\t","&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
#    files = get_file(app.config['NODE_CONFIG_FOLDER'])
#    return render_template('configs.html',files=files, active_config=active_config, filename=filename)
#
#@app.route('/config/delete/<filename>', methods=('GET', 'POST'))
#def deleteConfig(filename):
#    if(filename == "factory.json" or filename == "default.json"):
#        flash("you can not delete " + filename, 'warning')
#        return redirect(url_for('configs'))
#    else:
#        os.remove(app.config['NODE_CONFIG_FOLDER']+"/"+filename)
#        flash(filename + ' deleted', 'warning')
#        return redirect(url_for('configs'))
#
#@app.route('/config/load/<filename>', methods=('GET', 'POST'))
#def loadConfig(filename):
#    status["load"] = True
#    status["file"] = filename
#    status["text"] = "Start saving config" 
#    return redirect(url_for('configs'))
#
#load_config_worker            = threading.Thread(target=loadConfigWorker)
#load_config_worker.daemon     = True
#load_config_worker.start()#