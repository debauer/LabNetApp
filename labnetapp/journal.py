#!/usr/bin/env python3
import os, time
from flask import Flask, render_template, flash, request, redirect, url_for, session, escape
from labnetapp import app
from labnetapp import csv_wrapper
from os.path import isfile, join
from operator import itemgetter

def get_journal_list(d):
    ff = [ f for f in os.listdir(d) if isfile(join(d,f)) ]
    files = []
    for f in ff:
        stat = os.stat(d+"/"+f)
        timeString  = f.replace(".csv", "")
        files.append({"name":f, "date": timeString})
        files = sorted(files, key=itemgetter('name'), reverse=True)
    return files

def get_journal(day):
    j = []
    journal = csv_wrapper.get_file(app.config['JOURNAL_FOLDER']+"/"+day+".csv")
    for a in journal:
        log = get_log(a[16])
        j.append({"start": a[0],
            "end": a[1],
            "w1": a[2],
            "w2": a[3],
            "h1": a[4],
            "h2": a[5],
            "tAussen": a[6],
            "tGas": a[7],
            "pGasStart": a[8],
            "pGasEnd": a[9],
            "menge": a[10],
            "preis": a[11],
            "zollmenge": a[12],
            "schlauchvolumen": a[13],
            "error_txt": a[14],
            "error_nr": a[15],
            "id": a[16], 
            "log": log
            })
    return j


def get_log(jid):
    j = []
    log = csv_wrapper.get_file(app.config['JOURNAL_LOG_FOLDER']+"/"+jid+".csv")
    for a in log:
        j.append({"status": a[0],"time": a[1],"banks": a[2],"amount": a[3],"txt": a[4]})
    return j

@app.route('/journal/<day>', methods=('GET', 'POST'))
def journalByDay(day):
    return render_template('journal.html', 
        journal = get_journal(day), 
        journal_list = get_journal_list(app.config['JOURNAL_FOLDER']), 
        day = day)

@app.route('/journal', methods=('GET', 'POST'))
def journal():
    journal_list = get_journal_list(app.config['JOURNAL_FOLDER'])
    day = journal_list[0]['name'].replace(".csv","")
    return redirect("/journal/"+day)
