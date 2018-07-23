#!/usr/bin/python
import  os
from flask import Flask, render_template, flash, request, redirect, url_for, session, escape
from labnetapp import app, csv_wrapper
from os import listdir
from os.path import isfile, join
from operator import itemgetter



def get_log_list(d):
    ff = [ f for f in listdir(d) if isfile(join(d,f)) ]
    files = []
    for f in ff:
        stat = os.stat(d+"/"+f)
        #timeString  = time.strftime("%d.%m.%Y", time.localtime(stat[ST_MTIME]))
        timeString  = f.replace(".csv", "")
        files.append({"name":f, "date": timeString})
        files = sorted(files, key=itemgetter('name'), reverse=True)
    return files

def get_log(day):
    log = []
    l = []
    log = csv_wrapper.get_file(app.config['CAN_LOG_FOLDER']+"/"+day+".csv")
    for a in log:
        l.append({"status": a[0],"date": a[1],"banks": a[2],"pressure": a[3],"message": a[4]})
    return l

@app.route('/log', methods=('GET', 'POST'))
def log():
    log_list = get_log_list(app.config['CAN_LOG_FOLDER'])
    log = get_log(log_list[0]['name'].replace(".csv",""))
    print(log_list[0]['name'].replace(".csv",""))
    return render_template('logs.html', log = log, log_list = log_list, day = log_list[0]['name'].replace(".csv",""))

@app.route('/log/<day>', methods=('GET', 'POST'))
def logByDay(day):
    log = get_log(day)
    log_list = get_log_list(app.config['CAN_LOG_FOLDER'])
    return render_template('logs.html', log = log, log_list = log_list, day = day)