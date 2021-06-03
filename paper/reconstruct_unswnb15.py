#!/usr/bin/python3

import gzip, json, os

N = 20 
dablog, baseline = 'dablog', 'baseline'
threshold, dirs = 0.1, {dablog: '2020-10-21_dablog_k706_ipqhr', baseline: '2020-10-21_deeplog_k706_ipqhr'}
blocks = {
    dablog: [
        '149.171.126.18-34',  # TP in DabLog, FN in Baseline
        '149.171.126.18-35',  # TP in DabLog, FN in Baseline
        '149.171.126.18-44',  # TP in DabLog, FN in Baseline
        '149.171.126.18-195', # FN in DabLog, TP in Baseline 
        '149.171.126.18-226', # FN in DabLog, TP in Baseline
        '149.171.126.3-527',  # TN in DabLog, FP in Baseline
    ], 
    baseline: [
        '149.171.126.18-34',  # TP in DabLog, FN in Baseline
        '149.171.126.18-35',  # TP in DabLog, FN in Baseline
        '149.171.126.18-44',  # TP in DabLog, FN in Baseline
        '149.171.126.18-195', # FN in DabLog, TP in Baseline 
        '149.171.126.18-226', # FN in DabLog, TP in Baseline
        '149.171.126.3-527',  # TN in DabLog, FP in Baseline
    ],
}

# read decode-book
decode = {}
for model in dirs:
    filename = dirs [model] + '.metadata'
    if os.path.exists (filename): metadata = open (filename, 'r')
    metadata = open (dirs [model] + '.metadata', 'r')
    metadata.readline ()
    decode [model] = json.loads (metadata.readline ())

# baseline FP
for block in blocks [baseline]:                                 
    print ('\033[92m', baseline, block, '\033[0m')
    for line in open (os.path.join (baseline, block + '.predict'), 'r'):
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
for block in blocks [dablog]:
    print ('\33[92m', dablog, block, '\033[0m')
    for line in open (os.path.join (dablog, block + '.predict'), 'r'):
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

# reconstrct most-frequent common fp
if True:
    predictfilepath = 'commonfps.predict.gz'
    # predictfilepath = 'dablogfps.predict.gz'
    sequencefilepath = '/home/lunpin/anom/unsw_nb15/out/frequency_k706/sequences'
    keyfilepath = '/home/lunpin/anom/unsw_nb15/out/frequency_k706/keys'
    abnormalseq = {}
    abnormalkey = {}
    sequences = {}
    keys = json.loads (open (keyfilepath, 'rt').read ())
    for i, line in enumerate (open (sequencefilepath, 'rt')):
        if i == 0: continue
        elif i == 1: sequences = json.loads (line)
        else: break
    print (sequences.keys ())
    print (len (sequences ['trains']))
    print (len (sequences ['normals']))
    print (len (sequences ['abnormals']))
    for line in gzip.open (predictfilepath, 'rt'):
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
        abseq = str ('\n'.join ([x for x in X if '<' not in x and len (x.strip ()) > 0]))
        abkey = X [maxindex]
        abnormalseq.setdefault (abseq, 0)
        abnormalseq [abseq] += 1
        abnormalkey.setdefault (abkey, 0)
        abnormalkey [abkey] += 1

    print ('deg. of ab. seq:', len (abnormalseq))
    print ('size of ab. seq:', sum ([abnormalseq [s] for s in abnormalseq]))
    print ('max of ab.seq:', max ([abnormalseq [s] for s in abnormalseq]))
    normal_occ, abnormal_occ, train_occ = 0, 0, 0
    notfound = 0
    for seq in abnormalseq:
        if seq in sequences ['normals']: normal_occ += sequences ['normals'][seq]
        if seq in sequences ['abnormals']: abnormal_occ += sequences ['abnormals'][seq]
        if seq in sequences ['trains']: train_occ += sequences ['trains'][seq]
        if seq not in sequences ['normals'] and seq not in sequences ['abnormals'] and seq not in sequences ['trains']: 
            #print (seq.replace ('\n', '----'))
            notfound +=1
    print ('max in train:', max ([sequences ['trains'][seq] for seq in abnormalseq if seq in sequences ['trains']]))
    print ('train occ of ab. seqs:', train_occ)
    print ('normal occ of ab. seqs:', normal_occ)
    print ('abnormal occ of ab. seqs:', abnormal_occ)
    print ('notfound', notfound)
   
    abnormalkey = sorted (abnormalkey.items (), key=lambda item: item [1], reverse=True)
    print ('deq. of ab. key:', len (abnormalkey))
    for key in abnormalkey [: 10]:
        print (key, 'ab-exc:', key [0] in keys ['abnormals'] and key [0] not in keys ['trains'] and key [0] not in keys ['normals'])


