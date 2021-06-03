#!/usr/bin/python3

import json, os

top=10
rootdir = '/home/lunpin/anom/sosp2009/exp'
filename = 'subjectranks'
dablog, baseline = 'dablog', 'baseline'
#threshold, dirs = 0.09, {dablog: '2020-02-27_3', baseline: '2020-02-27_1'} # 101 keys
#threshold, dirs = 0.06, {dablog: '2020-02-29_9', baseline: '2020-02-29_2'} # 304 keys
threshold, dirs = 0.6, {dablog: '2020-04-15_8', baseline: '2020-02-29_1'} # 304 keys, 5K
TP, FP = {}, {}
rTP, rFP = {}, {}

# read subject ranks
for model in dirs:
    TP [model] = {}
    FP [model] = {}
    for line in open (os.path.join (rootdir, dirs [model], filename), 'r'):
        line = json.loads (line)
        if line ['label'] in ['Abnormal', 'abnormal']: TP [model][line ['subject']] = line
        else: FP [model][line ['subject']] = line
    rTP [model] = sorted (TP [model].values (), key=lambda obj: obj ['rank'])
    rFP [model] = sorted (FP [model].values (), key=lambda obj: obj ['rank'])

if True: # useless information here       
    targets = [] 
    for obj in rTP [baseline]:
        if obj ['rank'] <= threshold: continue
        subject = obj ['subject']
        if subject in TP [dablog] and TP [dablog][subject]['rank'] > threshold:
            targets.append (subject)
    print ('Common TP (', len (targets), ')')
    for line in targets [: top]: print (line)
    targets = [] 
    for obj in rFP [baseline]:
        if obj ['rank'] <= threshold: continue
        subject = obj ['subject']
        if subject in FP [dablog] and FP [dablog][subject]['rank'] > threshold:
            targets.append (obj)
    print ('Common FP (', len (targets), ')')
    targets = [] 
    for obj in rTP [baseline]:
        if obj ['rank'] > threshold: break
        subject = obj ['subject']
        if subject not in TP [dablog] or TP [dablog][subject]['rank'] <= threshold:
            targets.append (obj)
    print ('Common FN (', len (targets) + 78, ')') # 78 absolute false negatives, see exp/[date]/false_negatives
    targets = []      
    for obj in rFP [dablog]:
        if obj ['rank'] <= threshold: continue
        subject = obj ['subject']
        if subject not in FP [baseline] or FP [baseline][subject]['rank'] <= threshold:
            targets.append ([subject, FP [dablog][subject]['rank']]) #, FP [baseline][subject]['rank']])
    print ('FP in DabLog but TN in Baseline (', len (targets), ')')    
    targets = sorted (targets, key=lambda obj: obj [1], reverse=True)
    for line in targets [: top]: print (line)
    targets = []
    for obj in rTP [baseline]:
        if obj ['rank'] <= threshold: continue
        subject = obj ['subject']
        if subject not in TP [dablog] or TP [dablog][subject]['rank'] <= threshold:
            targets.append ([subject, TP [dablog][subject]['rank'], TP [baseline][subject]['rank']])
    print ('FN in DabLog but TP in Baseline (', len (targets), ')')

# filter TP in DabLog but FN in Baseline
targets = []       
for obj in rTP [dablog]:
    if obj ['rank'] <= threshold: continue
    subject = obj ['subject']
    if subject not in TP [baseline] or TP [baseline][subject]['rank'] <= threshold:
        targets.append ([subject, TP [dablog][subject]['rank'], TP [baseline][subject]['rank']])
print ('TP in DabLog but FN in Baseline (', len (targets), ')')
targets = sorted (targets, key=lambda obj: obj [1], reverse=True)
for line in targets [: top]: print (line)

# filter TN in DabLog but FP in Baseline
targets = []
for obj in rFP [baseline]:
    if obj ['rank'] <= threshold: continue
    subject = obj ['subject']
    if subject not in FP [dablog] or FP [dablog][subject]['rank'] <= threshold:
        r = FP [dablog][subject]['rank'] if subject in FP [dablog] else None
        targets.append ([subject, r, FP [baseline][subject]['rank']])
print ('TN in DabLog but FP in Baseline (', len (targets), ')')
targets = sorted (targets, key=lambda obj: obj [2], reverse=True)
for line in targets [: top]: print (line)

