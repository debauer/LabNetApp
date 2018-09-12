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
        if not plugs[plugName].getStripId() in st:
            #pass
            st.append( plugs[plugName].getStripId())
    return st

def getStripNamesSorted():
    listOfStrips = []
    for n in nodes:
        stripList = nodes[n].getStripNames()
        print(stripList)
        for s in stripList:
            listOfStrips.append(s)
    listOfStrips.sort()
    return listOfStrips

def getAllPlugsJson():
    data = {}
    for plugName in plugs:
        stripName = plugs[plugName].getStripId()
        if not stripName in data.keys():
            data[stripName] = []
        data[stripName] = plugs[plugName].getData()
    return data


load_definition_file("nodeConfig/mainv2.json")


print()
print(getOnlyActiveStripNamesSorted())

print(getStripNamesSorted())
print(getAllPlugsJson()['14-door'])