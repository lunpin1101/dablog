#!/usr/bin/python3
import json, matplotlib, numpy, os
matplotlib.use ('Agg')
import matplotlib.pyplot



def main ():

    tail=50
    plotModel ('dablog-k706-hhr', ['2020-10-19_dablog_k706_iphhr', '2020-10-20_dablog_k706_iphhr', '2020-10-21_dablog_k706_iphhr'], tail=tail)
    plotModel ('dablog-k366-hhr', ['2020-10-19_dablog_k366_iphhr', '2020-10-20_dablog_k366_iphhr', '2020-10-21_dablog_k366_iphhr'], tail=tail)
    plotModel ('dablog-k706-qhr', ['2020-10-19_dablog_k706_ipqhr', '2020-10-20_dablog_k706_ipqhr', '2020-10-21_dablog_k706_ipqhr'], tail=tail)
    plotModel ('dablog-k366-qhr', ['2020-10-19_dablog_k366_ipqhr', '2020-10-20_dablog_k366_ipqhr', '2020-10-21_dablog_k366_ipqhr'], tail=tail)
    
    plotModel ('deeplog-k706-hhr', ['2020-10-19_deeplog_k706_iphhr', '2020-10-20_deeplog_k706_iphhr', '2020-10-21_deeplog_k706_iphhr'], tail=tail)
    plotModel ('deeplog-k366-hhr', ['2020-10-19_deeplog_k366_iphhr', '2020-10-20_deeplog_k366_iphhr', '2020-10-21_deeplog_k366_iphhr'], tail=tail)
    plotModel ('deeplog-k706-qhr', ['2020-10-19_deeplog_k706_ipqhr', '2020-10-20_deeplog_k706_ipqhr', '2020-10-21_deeplog_k706_ipqhr'], tail=tail)
    plotModel ('deeplog-k366-qhr', ['2020-10-19_deeplog_k366_ipqhr', '2020-10-20_deeplog_k366_ipqhr', '2020-10-21_deeplog_k366_ipqhr'], tail=tail)
    
    plotMetric ('unswnb15dablogf1curve', 'F1 Score', [
        ['706 Keys, Quarter Hour', ['2020-10-19_dablog_k706_ipqhr', '2020-10-20_dablog_k706_ipqhr', '2020-10-21_dablog_k706_ipqhr']],
        ['366 Keys, Quarter Hour', ['2020-10-19_dablog_k366_ipqhr', '2020-10-20_dablog_k366_ipqhr', '2020-10-21_dablog_k366_ipqhr']],
        ['706 Keys, Half Hour', ['2020-10-19_dablog_k706_iphhr', '2020-10-20_dablog_k706_iphhr', '2020-10-21_dablog_k706_iphhr']],
        ['366 Keys, Half Hour', ['2020-10-19_dablog_k366_iphhr', '2020-10-20_dablog_k366_iphhr', '2020-10-21_dablog_k366_iphhr']]],
        tail=tail
    )
    plotMetric ('unswnb15deeplogf1curve', 'F1 Score', [
        ['706 Keys, Quarter Hour', ['2020-10-19_deeplog_k706_ipqhr', '2020-10-20_deeplog_k706_ipqhr', '2020-10-21_deeplog_k706_ipqhr']],
        ['366 Keys, Quarter Hour', ['2020-10-19_deeplog_k366_ipqhr', '2020-10-20_deeplog_k366_ipqhr', '2020-10-21_deeplog_k366_ipqhr']],
        ['706 Keys, Half Hour', ['2020-10-19_deeplog_k706_iphhr', '2020-10-20_deeplog_k706_iphhr', '2020-10-21_deeplog_k706_iphhr']],
        ['366 Keys, Half Hour', ['2020-10-19_deeplog_k366_iphhr', '2020-10-20_deeplog_k366_iphhr', '2020-10-21_deeplog_k366_iphhr']]],
        tail=tail
    )
    plotMetric ('unswnb15comparison_k706', 'F1 Score', [
        ['Proposed Dablog', ['2020-10-19_dablog_k706_ipqhr', '2020-10-20_dablog_k706_ipqhr', '2020-10-21_dablog_k706_ipqhr']],
        ['Baseline Predictor', ['2020-10-19_deeplog_k706_ipqhr', '2020-10-20_deeplog_k706_ipqhr', '2020-10-21_deeplog_k706_ipqhr']],
        ['Top-Frequency Model', ['frequency_k706']]],
        tail=tail
    )
    plotMetric ('unswnb15comparison_k366', 'F1 Score', [
        ['Proposed Dablog', ['2020-10-19_dablog_k366_ipqhr', '2020-10-20_dablog_k366_ipqhr', '2020-10-21_dablog_k366_ipqhr']],
        ['Baseline Predictor', ['2020-10-19_deeplog_k366_ipqhr', '2020-10-20_deeplog_k366_ipqhr', '2020-10-21_deeplog_k366_ipqhr']],
        ['Top-Frequency Model', ['frequency_k706']]],
        tail=tail
    )
    plotMetric ('unswnb15comparison_psuthesis', 'F1 Score', [
        ['Proposed Dablog', ['2020-10-19_dablog_k706_ipqhr', '2020-10-20_dablog_k706_ipqhr', '2020-10-21_dablog_k706_ipqhr']],
        ['Baseline Predictor', ['2020-10-19_deeplog_k706_ipqhr', '2020-10-20_deeplog_k706_ipqhr', '2020-10-21_deeplog_k706_ipqhr']],
        ['Top-Frequency Model', ['frequency_k706']]],
        tail=tail
    )



def plotMetric (filepath, metric, items, rootdir='/home/lunpin/anom/unsw_nb15/out', filename='rank.metric', head=0, tail=100):
    legends = [item [0] for item in items]
    directories = [item [1] for item in items]
    metrics = [getMetrics (dirs, rootdir, filename, merge=True) [0] for dirs in directories]
    metric = [[legends [i], metrics [i][metric]] for i in range (0, len (legends))]
    savePlot (filepath, metric, head, tail)



def plotModel (filepath, directories, rootdir='/home/lunpin/anom/unsw_nb15/out', filename='rank.metric', head=0, tail=100):
    if not isinstance (directories, list): directories = [directories]
    metric = getMetrics (directories, rootdir, filename, merge=True) [0]
    items = ['F1 Score', 'FP Rate', 'Precision', 'Recall']
    metric = [[item, metric [item]] for item in items]
    savePlot (filepath, metric, head, tail)
    


def savePlot (filepath, arrays, head=0, tail=100):
    print ('[', filepath, ']')
    legend = ['ko', 'ks', 'k^', 'kv', 'kD', 'k*']
    styles = ['k-', 'k:', 'k:', 'k:', 'k:', 'k:']
    fig = matplotlib.pyplot.figure ()
    ax = fig.add_subplot (1, 1, 1)
    xAxis = [i for i in range (0, len (arrays [0][1]))]
    lw, ms = 2.5, 10
    def abstract (index, array): return [array [i] for i in range (4 * index + 1, len (array), int (len (array) / 5))]
    for i in range (0, min (len (legend), len (arrays))):
        # draw line
        label, array = arrays [i]
        if array is None: continue
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
    # scale
    xmin, xmax = matplotlib.pyplot.xlim ()
    matplotlib.pyplot.xlim (head/100, tail/100)
    matplotlib.pyplot.ylim (0.0, 1.0)
    #basesize = 4
    #fig.set_size_inches(basesize, basesize)
    # finalize
    matplotlib.pyplot.legend (fontsize=14)
    fig.tight_layout ()
    matplotlib.pyplot.savefig ('.'.join ([filepath, 'png']), dpi=128)
    matplotlib.pyplot.close (fig)


def getMetrics (directories, rootdir='/home/lunpin/anom/unsw_nb15/out', filename='rank.metric', merge=False):
    mm = ['FP Rate', 'FN Rate', 'Recall', 'Precision', 'F1 Score', 'Accuracy']
    datas = [] 
    for directory in directories:
        filepath = os.path.join (rootdir, directory, filename)
        try: data = open (filepath, 'rt').read ()
        except Exception as e: print (e); continue
        data = data.replace ('}{', '}\n{')
        data = data.split ('\n')
        dm = {}
        for obj in data:
            obj = json.loads (obj)
            for key in obj: dm [key] = obj [key]
        datas.append (dm)
    length = len (datas [0]['TP'])
    if merge: 
        datamerge = {}
        for item in ['TP', 'FP', 'TN', 'FN']:
            datamerge [item] = [0] * length
            for dm in datas:
                for i in range (0, length):
                    datamerge [item][i] += dm [item][i]
        datas = [datamerge]
    metrics = []
    for dm in datas:
        metric = {}
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

