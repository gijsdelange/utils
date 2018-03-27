# Finds peaks using mean. Especially useful for sweeps with a well-defined mean and are not close-ups of peaks.
# args = Data or timestr
# trace = None : Which trace to use
# datestr : The date of the file
# smoothing = 1e6 : Frequency length to smooth over
# percentile = 70 : Percentile in which to average over. Higher percentile results in more points being counted
# threshold = 7 : Number of standard deviations a point needs to be from the mean to be considered a peak.
# peakrange = 1e6 : Range in which to search for a peak and which is skipped after a peak is found
# plot = False : Whether to plot results or not.
#output: 'peaks', 'dips', which give the indices of the peaks and dips respectively
# If insufficient peaks are found, a solution is to change smoothing depending on the linewidth, or lower the percentile and/or threshold



import qt
from qt import Data
import sys
import numpy as np
from matplotlib import pyplot as plt


dat,=args
kw = kwargs
trace = kw.pop('trace',None)
datestr = kw.pop('datestr','')
thresholdsd = kw.pop('threshold',7)
percentile = kw.pop('percentile',70)
smoothlength = kw.pop('smoothing',10e5)


load_data = qt.scripts['load_data']
print_data_info = qt.scripts['print_data_info']
moving_average = qt.scripts['moving_average']

if type(dat) == type('') or type(dat) == type(1):
    timestr = '%s'%dat
    if datestr != '':
        dat=load_data(timestr,[trace],datestr=datestr)['Data']
    else:
        dat=load_data(timestr,[trace])['Data']
elif type(dat).__name__!='Data':
    print 'must give data file or timestr'
    sys.exit()
#print dat1[:,0]
df = np.diff(dat[:,0])[0]
N = int(smoothlength/df)
datsmooth=moving_average(dat[:,0], dat[:,1], N)
length = len(datsmooth)
#a = datsmooth
# peaks = np.r_[True, a[1:] < a[:-1]] & np.r_[a[:-1] < a[1:], True]
# print peaks



#Finding peaks
percval = np.percentile(datsmooth,percentile)
datperc = datsmooth[datsmooth < percval]
percmean = np.mean(datperc)
sd = np.std(datperc)
threshold = percmean + thresholdsd * sd

thresholdlst = np.arange(datsmooth.size)[datsmooth > threshold]
datthreshold = datsmooth[thresholdlst]
print thresholdlst
kk=0
inpeak = False
peakranges=[]
peaks=[]
if len(thresholdlst) != 0:
    for i in thresholdlst:
        if inpeak==False:
            inpeak = True
            kk=i+1
            peakfmin = kk
            peakfmax = kk
        else:
            if kk == i:
                kk+=1
                peakfmax = kk
            else:
                inpeak=False
                peakranges.append([peakfmin,peakfmax])

    peakranges.append([peakfmin,peakfmax-1])
    print [(elem[0],elem[1]) for elem in peakranges]
    #peaks = [datthreshold[elem[0]:elem[1]] for elem in peakranges]
    peaks=[elem[0]+np.argmax(dat[elem[0]:elem[1],1]) for elem in peakranges]
    print peaks


#Finding dips
percval = np.percentile(datsmooth,100-percentile)
datperc = datsmooth[datsmooth > percval]
percmean = np.mean(datperc)
sd = np.std(datperc)
threshold = percmean - thresholdsd * sd
#Determine dips
thresholdlst = np.arange(datsmooth.size)[datsmooth < threshold]
datthreshold = datsmooth[thresholdlst]

print thresholdlst
kk=0
indip = False
dipranges=[]
dips=[]
if len(thresholdlst) != 0:
    for i in thresholdlst:
        if indip==False:
            indip = True
            kk=i+1
            dipfmin = kk
            dipfmax = kk
        else:
            if kk == i:
                kk+=1
                dipfmax = kk
            else:
                indip=False
                dipranges.append([dipfmin,dipfmax])

    dipranges.append([dipfmin,dipfmax-1])
    print [(elem[0],elem[1]) for elem in dipranges]
    #dips = [datthreshold[elem[0]:elem[1]] for elem in dipranges]
    dips=[elem[0]+np.argmin(dat[elem[0]:elem[1],1]) for elem in dipranges]
    print dips

if kw.pop('plot',False):
    plt.figure('testscript')
    plt.clf()
    plt.plot(dat[:,1])
    plt.plot(datsmooth)
    #plt.plot([np.mean(datsmooth)]*len(datsmooth))
    plt.plot([percmean]*length)
    plt.plot([threshold]*length)
    plt.plot(datthreshold,'o')
    plt.plot(peaks,dat[peaks],'o')
    plt.plot(dips,dat[dips],'o')
    plt.ylim(0,1.1)
    plt.show()


set_return({'peaks':peaks,'dips':dips})