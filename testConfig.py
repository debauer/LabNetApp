from os import listdir
from os.path import isfile, join
import os, json

from nodeConfig import *

def printStuff():
    for k in nodes.keys():
        print(nodes[k].getStripNames())
        #for o in nodes[k].getStrips():
        #    print(o.getName())
    for k in strips.keys():
        print(strips[k].getPlugNames())

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
        data[stripName] = plugs[plugName].getData()
    return data


buildUpObjects("nodeConfig/main.json")


print()
print(getOnlyActiveStripNamesSorted())

#print(getStripNamesSorted())
#print(getAllPlugsJson()['14-door'])