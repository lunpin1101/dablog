#!/usr/bin/python3
import json, matplotlib, numpy, os
matplotlib.use ('Agg')
import matplotlib.pyplot



def main ():


    plotMetric ('logkeys101asiaccs', 'F1 Score', [
        ['DabLog', '2020-02-27_3'],
        ['Baseline', '2020-02-27_1'],
        ['Frequency', 'logkey.2'], 
    ])

    plotMetric ('logkeys101psuthesis', 'F1 Score', [
        ['Proposed DabLog', '2020-02-27_3'],
        ['Baseline Predictor', '2020-02-27_1'],
        ['Top-Frequency Model', 'logkey.2'], 
    ])
    
    plotModel ('dablog101', '2020-02-27_3')
    plotModel ('dablog304', '2020-02-29_9')
    plotMetric ('perdablog', 'F1 Score', [
        [None, '2020-02-27_3'],
        [None, '2020-02-27_7'],
        [None, '2020-02-27_11'],
        [None, '2020-02-27_15'],
        [None, '2020-02-27_19'],
    ])
 
    
    
    plotModel ('baseline101', '2020-02-27_1')
    plotModel ('baseline304', '2020-02-29_2')



    plotMetric ('logkeys31', 'F1 Score', [
        ['DabLog', '2020-04-15_10'],
        #['DabLog (5K)', '2020-04-15_3'],
        ['Baseline', '2020-04-15_9'],
        #['Baseline (5K)', '2020-04-15_1'],
        ['Frequency', 'logkey.0'],
    ])            

    
    plotMetric ('logkeys101', 'F1 Score', [
        ['DabLog', '2020-02-27_3'],
        #['DabLog (5K)', '2020-04-15_7'],
        ['Baseline', '2020-02-27_1'],
        #['Baseline (5K)', '2020-02-28_1'], 
        ['Frequency', 'logkey.2'], 
    ])
    


    plotMetric ('logkeys304', 'F1 Score', [
        ['DabLog', '2020-02-29_9'],
        #['DabLog (5K)', '2020-04-15_8'],
        ['Baseline', '2020-02-29_2'],
        #['Baseline (5K)', '2020-02-29_1'],
        ['Frequencey', 'logkey.3'],
    ])



    plotMetric ('recall', 'Recall', [
        ['DabLog: 101 keys', '2020-02-27_3'],
        ['DabLog: 304 keys', '2020-02-29_9'],
        ['Baseline: 101 keys', '2020-02-27_1'],
        ['Baseline: 304 keys', '2020-02-29_2'],
    ], head=5, tail=20)



    plotMetric ('precision', 'Precision', [
        ['DabLog: 101 keys', '2020-02-27_3'],
        ['DabLog: 304 keys', '2020-02-29_9'],
        ['Baseline: 101 keys', '2020-02-27_1'],
        ['Baseline: 304 keys', '2020-02-29_2'],
    ], head=5, tail=20)

  
    
#    plotMetric ('epochs', 'F1 Score', [
#        ['DabLog: 8 epochs', '2020-04-15_5'],
#        ['DabLog: 16 epochs', '2020-02-26_16'],
#        ['DabLog 32 epochs', '2020-02-26_18'],
#        ['DabLog: 64 epochs', '2020-02-26_12'],
#        ['DabLog: 128 epochs', '2020-02-26_14'],
#        ['Baseline: 8 epochs', '2020-02-26_10'], 
#    ])



#    plotMetric ('mimick31', 'F1 Score', [
#        ['DabLog: Rank', '2020-04-15_3'],
#        ['DabLog+M: Rank', '2020-04-15_4'],
#        ['DabLog: Double', '2020-04-15_3d'],
#        ['DabLog+M: Double', '2020-04-15_4d'],
#    ])



#    plotMetric ('mimick101', 'F1 Score', [
#        ['DabLog: Rank', '2020-02-27_3'],
#        ['DabLog+M: Rank', '2020-02-27_4'],
#        ['DabLog: Double', '2020-02-27_3d'],
#        ['DabLog+M: Double', '2020-02-27_4d'],
#    ])            



#    plotMetric ('mimick304', 'F1 Score', [
#        ['DabLog: Rank', '2020-02-29_9'],
#        ['DabLog+M: Rank', '2020-02-29_5'],
#        ['DabLog: Double', '2020-02-29_9d'],
#        ['DabLog+M: Double', '2020-02-29_5d'],
#    ])



def plotMetric (filepath, metric, items, rootdir='/media/lunpin/ext-drive/bizon/anom/sosp2009/exp', filename='rank.0.0.metric', head=0, tail=999):
    legends = [item [0] for item in items]
    directories = [item [1] for item in items]
    metrics = getMetrics (directories, rootdir, filename)
    metric = [[legends [i], metrics [i][metric]] for i in range (0, len (legends))]
    savePlot (filepath, metric, head, tail)



def plotModel (filepath, directory, rootdir='/home/lunpin/anom/sosp2009/exp', filename='rank.0.0.metric', head=0, tail=999):
    metric = getMetrics ([directory], rootdir, filename) [0]
    items = ['F1 Score', 'FP Rate', 'Precision', 'Recall']
    metric = [[item, metric [item]] for item in items]
    savePlot (filepath, metric, head, tail)
    


def savePlot (filepath, arrays, head=0, tail=999):
    print ('[', filepath, ']')
    legend = ['ko', 'ks', 'k^', 'kv', 'kD', 'k*']
    styles = ['k-', 'k:', 'k:', 'k:', 'k:', 'k:']
    fig = matplotlib.pyplot.figure ()
    ax = fig.add_subplot (1, 1, 1)
    xAxis = [i for i in range (0, len (arrays [0][1]))] [head: tail]
    lw, ms = 2.5, 10
    def abstract (index, array): return [array [i] for i in range (4 * index + 1, len (array), int (len (array) / 5))]
    for i in range (0, min (len (legend), len (arrays))):
        # draw line
        label, array = arrays [i]
        if array is None: continue
        array = array [head: tail]
        xdata = numpy.array (abstract (i, xAxis)) / 100
        ydata = abstract (i, array)
        ax.plot (xdata, ydata, legend [i], label=label, ms=ms)
        xdata = numpy.array (xAxis) / 100
        ydata = array
        ax.plot (xdata, ydata, styles [i], lw=lw)
        # stat line
        peak = max (array)
        index = array.index (peak)
        area = sum (array) / 100
        print ('   ', label, '( peak', peak, 'at', index, ') ( AUC', area, ')')
    matplotlib.pyplot.legend (fontsize=14)
    fig.tight_layout ()
    matplotlib.pyplot.savefig ('.'.join ([filepath, 'png']), dpi=128)
    matplotlib.pyplot.close (fig)


def getMetrics (directories, rootdir='/home/lunpin/anom/sosp2009/exp', filename='rank.0.0.metric'):
    mm = ['FP Rate', 'FN Rate', 'Recall', 'Precision', 'F1 Score', 'Accuracy']
    metrics = []
    for directory in directories:
        filepath = os.path.join (rootdir, directory, filename)
        try: data = open (filepath, 'r').read ()
        except: metrics.append ({m: None for m in mm}); continue
        data = data.replace ('}{', '}\n{')
        data = data.split ('\n')
        dm, metric = {}, {}
        for obj in data:
            obj = json.loads (obj)
            for key in obj: dm [key] = obj [key]
        length = len (dm ['TP'])
        for m in mm: metric [m] = [0] * length
        for i in range (0, length):
            tp, fp, tn, fn = dm ['TP'][i], dm ['FP'][i], dm ['TN'][i], dm ['FN'][i]
            metric [mm [0]][i] = fp / (fp + tn)                             # fpr
            metric [mm [1]][i] = fn / (fn + tp)                             # fnr
            metric [mm [2]][i] = tp / (tp + fn)                             # recall
            metric [mm [3]][i] = tp / (tp + fp) if tp + fp > 0 else 0.0     # precision
            metric [mm [4]][i] = 2 * tp / (2 * tp + fp + fn)                # f1
            metric [mm [5]][i] = (tp + tn) / (tp + fn + fp + tn)            # accuracy
        metrics.append (metric)
    return metrics

if __name__ == '__main__': main ()

