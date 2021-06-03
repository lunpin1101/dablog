#!/usr/bin/python3

import json, os

N = 20 
dablog, baseline = 'dablog', 'baseline'
#threshold, dirs = 0.2, {dablog: '2020-02-27_3', baseline: '2020-02-27_1'} # 101 keys
#threshold, dirs = 0.06, {dablog: '2020-02-29_9', baseline: '2020-02-29_2'} # 304 keys
threshold, dirs = 0.06, {dablog: '2020-04-15_8', baseline: '2020-02-29_1'} # 304 keys, 5K
#blocks = {dablog: 'blk_-9134333392518302881', baseline: 'blk_-3547984959929874282'} # DabLog's TP, Baseline's FP
#blocks = {dablog: 'blk_6937712548866091907', baseline: None} # DabLog's FP 1
#blocks = {dablog: 'blk_-5966861501708083020', baseline: None} # DabLog's FP 2
#blocks = {dablog: 'blk_36665758775198953', baseline: None} # DabLog's FP 3
#blocks = {dablog: 'blk_-733866046148122932', baseline: None} # DabLog's FP 4
blocks = {dablog: 'blk_4134457199716564933', baseline: None} # DabLog's FP 5

# 5k keys 304 keys
blocks = {dablog: 'blk_-6342748197145120596', baseline: 'blk_-9078659237827651009'}

# read decode-book
decode = {}
for model in dirs:
    filename = dirs [model] + '.metadata'
    if os.path.exists (filename): metadata = open (filename, 'r')
    metadata = open (dirs [model] + '.metadata', 'r')
    metadata.readline ()
    decode [model] = json.loads (metadata.readline ())

# baseline FP    
if blocks [baseline] is not None:
    for line in open (blocks [baseline] + '.predict', 'r'):
        line = json.loads (line)
        YP = line ['P'][line ['X'][-1]]
        SP = sorted (line ['P'], reverse=True)
        tops = SP [: N]
        rank = SP.index (YP) / len (SP)
        if rank < threshold: continue
        X = [decode [baseline][str (x)] for x in line ['X']]
        for evt in X [: -1]: print ('X =', evt)
        print ('Y =', X [-1])
        print ('Rank =', rank, 'P =', YP)
        print ('Tops =')
        for top in tops:
            evt = line ['P'].index (top)
            print ('{:06.4f}'.format (top), decode [baseline][str (evt)])
        print ('--------------------------------')

# dablog TP
for line in open (blocks [dablog] + '.predict', 'r'):
    line = json.loads (line)
    P = line ['P'][:: -1]
    X = [decode [dablog][str (x)] for x in line ['X']]
    Ranks, Probs = [], []
    maxrank = 0.0
    maxindex = 0
    for i in range (0, len (X)):
        x = line ['X'] [i]
        YP = P [i][x]
        SP = sorted (P [i], reverse=True)
        rank = SP.index (YP) / len (SP)
        Ranks.append (rank)
        Probs.append (YP)
        if rank > maxrank:
            maxrank = rank
            maxindex = i
    if maxrank < threshold: continue
    for i in range (0, len (X)):
        if i == maxindex: print ('\033[91m', end='')
        else: print ('\033[0m', end='')
        print ('{:06.4f}'.format (Ranks [i]), '{:06.4f}'.format (Probs [i]), X [i])
    print ('Error at index', maxindex, 'tops =')
    tops = sorted (P [maxindex], reverse=True) [: N]
    for top in tops:
        index = P [maxindex].index (top)
        print ('{:06.4f}'.format (top), decode [dablog][str (index)])
    print ('--------------------------------')

