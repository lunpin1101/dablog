#!/usr/bin/python3

import json, numpy, os

top=3000
rootdir = '/home/lunpin/anom/unsw_nb15/out'
dablog, baseline = 'dablog', 'baseline'
threshold, dirs = 0.1, {dablog: '2020-10-21_dablog_k706_ipqhr', baseline: '2020-10-21_deeplog_k706_ipqhr'} # 304 keys, 5K
TP, FP = {}, {}
rTP, rFP = {}, {}
labels = {}

# read labels
labels = json.load (open (os.path.join (rootdir, dirs [dablog], 'labels'), 'r'))
lengths = json.load (open (os.path.join (rootdir, dirs [dablog], 'subjectlengths'), 'r'))

# read subject ranks
for model in dirs:
    TP [model] = {}
    FP [model] = {}
    for line in open (os.path.join (rootdir, dirs [model], 'subjectranks'), 'r'):
        line = json.loads (line)
        if len (line ['label']) > 0: TP [model][line ['subject']] = line
        else: FP [model][line ['subject']] = line
        labels.setdefault (line ['subject'], '')
    rTP [model] = sorted (TP [model].values (), key=lambda obj: obj ['rank'])
    rFP [model] = sorted (FP [model].values (), key=lambda obj: obj ['rank'])

if True: # useless information here       

    targets = [] 
    for obj in rTP [baseline]:
        if obj ['rank'] <= threshold: continue
        subject = obj ['subject']
        if subject in TP [dablog] and TP [dablog][subject]['rank'] > threshold:
            targets.append ([subject, lengths [subject], labels [subject]])
    print ('Common TP (', len (targets), ')')
    for line in targets [: top]: print (line)

    targets = [] 
    for obj in rFP [baseline]:
        if obj ['rank'] <= threshold: continue
        subject = obj ['subject']
        if subject in FP [dablog] and FP [dablog][subject]['rank'] > threshold:
            targets.append ([subject, lengths [subject], labels [subject]])
    print ('Common FP (', len (targets), ')')
    for line in targets [: top]: print (line)
    with open ('commonfps', 'wt') as fout:
        fout.write ('\n'.join ([item [0] for item in targets]) + '\n')

    targets = [] 
    for obj in rTP [baseline]:
        if obj ['rank'] > threshold: break
        subject = obj ['subject']
        if subject not in TP [dablog] or TP [dablog][subject]['rank'] <= threshold:
            targets.append ([subject, lengths [subject], labels [subject]])
    print ('Common FN (', len (targets), ')') 
    for line in targets [: top]: print (line)
    with open ('commonfns', 'wt') as fout:
        fout.write ('\n'.join ([item [0] for item in targets]) + '\n')

    targets = []      
    for obj in rFP [dablog]:
        if obj ['rank'] <= threshold: continue
        subject = obj ['subject']
        if subject not in FP [baseline] or FP [baseline][subject]['rank'] <= threshold:
            targets.append ([subject, FP [dablog][subject]['rank'], lengths [subject], labels [subject]])
    print ('FP in DabLog but TN in Baseline (', len (targets), ')', numpy.mean ([item [1] for item in targets]))    
    targets = sorted (targets, key=lambda obj: obj [1], reverse=True)
    for line in targets [: top]: print (line)
    with open ('dablogfps', 'wt') as fout:
        fout.write ('\n'.join ([item [0] for item in targets]) + '\n')

    targets = []
    for obj in rTP [baseline]:
        if obj ['rank'] <= threshold: continue
        subject = obj ['subject']
        if subject not in TP [dablog] or TP [dablog][subject]['rank'] <= threshold:
            if subject not in TP [dablog]: targets.append ([subject, 0.0, TP [baseline][subject]['rank'], lengths [subject], labels [subject]])
            else: targets.append ([subject, TP [dablog][subject]['rank'], TP [baseline][subject]['rank'], lengths [subject], labels [subject]])
    print ('FN in DabLog but TP in Baseline (', len (targets), ')')
    for line in targets [: top]: print (line)
    with open ('dablogfns', 'wt') as fout:
        fout.write ('\n'.join ([item [0] for item in targets]) + '\n')

# filter TP in DabLog but FN in Baseline
targets = []       
for obj in rTP [dablog]:
    if obj ['rank'] <= threshold: continue
    subject = obj ['subject']
    if subject not in TP [baseline] or TP [baseline][subject]['rank'] <= threshold:
        targets.append ([subject, TP [dablog][subject]['rank'], TP [baseline][subject]['rank'], lengths [subject], labels [subject]])
print ('TP in DabLog but FN in Baseline (', len (targets), ')')
targets = sorted (targets, key=lambda obj: obj [1], reverse=True)
for line in targets [: top]: print (line)
with open ('dablogtps', 'wt') as fout:
    fout.write ('\n'.join ([item [0] for item in targets]) + '\n')

# filter TN in DabLog but FP in Baseline
targets = []
for obj in rFP [baseline]:
    if obj ['rank'] <= threshold: continue
    subject = obj ['subject']
    if subject not in FP [dablog] or FP [dablog][subject]['rank'] <= threshold:
        r = FP [dablog][subject]['rank'] if subject in FP [dablog] else None
        targets.append ([subject, r, FP [baseline][subject]['rank'], lengths [subject], labels [subject]])
print ('TN in DabLog but FP in Baseline (', len (targets), ')', numpy.mean ([item [2] for item in targets]))
targets = sorted (targets, key=lambda obj: obj [2], reverse=True)
for line in targets [: top]: print (line)
with open ('dablogtns', 'wt') as fout:
    fout.write ('\n'.join ([item [0] for item in targets]) + '\n')



print ('avg length:', numpy.mean ([item [3] for item in targets]))
print ('min length:', min ([item [3] for item in targets]))

