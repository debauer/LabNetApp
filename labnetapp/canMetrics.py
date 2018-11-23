#!/usr/bin/python
import time

from labnetapp import app, canObj


from influxdb import InfluxDBClient
from influxdb import SeriesHelper

influxInstance = InfluxDBClient(
    app.config["INFLUXDB"]["server"], 
    8086, 
    app.config["INFLUXDB"]["username"], 
    app.config["INFLUXDB"]["password"], 
    app.config["INFLUXDB"]["database"])

mps = 0 #messages per seconds
mtps = [] #message types per seconds

class canMetrics:

    class MySeriesHelper(SeriesHelper):
        class Meta:
            client = influxInstance
            series_name = 'labnet_msg'
            fields = ['per_sec']
            tags = ['server']
            bulk_size = 1
            autocommit = True

    def __init__(self, conf):
        pass

    def __str__(self):
        return "influxdb metric class"

    def put(self, obj): 
        global mps
        mps = mps + 1 


    ## call every 60s
    def calc(self):
        global mps
        self.MySeriesHelper(server=app.config['NAME'], per_sec=mps)
        mps = 0


