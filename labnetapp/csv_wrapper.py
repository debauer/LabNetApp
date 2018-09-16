# <!-- NOT IN USAGE UNTIL NOW!!! d.bauer -->

#!/usr/bin/env python3
import csv
import redis, os
import os.path

def get_file(f):
    fff = []
    if os.path.isfile(f):
        with open(f, mode='r') as ff:
            reader = csv.reader(ff, delimiter=',')
            for row in reader:
                fff.append(row);
        return fff
    else: 
        return fff