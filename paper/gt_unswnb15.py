#!/usr/bin/python3
import datetime

window = 15
sourcefile = '/home/lunpin/anom/unsw_nb15/csv/NUSW-NB15_GT.csv'

for count, line in enumerate (open (sourcefile, 'rt')):
    if count == 0: continue
    try:
        ts = int (line [: line.find (',')])
        dt = datetime.datetime.fromtimestamp (ts)
        addon = '/'.join ([str (dt.day), str (dt.hour), str (dt.minute//window)])
        line = line.strip () + ',' + addon
        print (line)
    except: pass



