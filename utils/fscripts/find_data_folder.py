#find_data
import time,os
timestr, = args
kw = kwargs
ts = time.localtime()
datestr = kw.pop('datestr','%d%02d%02d'%(ts.tm_year,ts.tm_mon,ts.tm_mday))
basedir = 'D:/qtlab/data/'+datestr
dirlist = os.listdir(basedir)

for dirstr in dirlist:
    #print type(dirstr)
    #print dirstr.find(timestr)
    if dirstr.find(timestr)>-1:
        datdir = os.path.join(basedir,dirstr)
        print 'found data: ',datdir
        break
filelist = os.listdir(datdir)
nfiles = 0
for fl in filelist:
    if fl.find('_')<4 and fl.find('_')>-1:
        if fl[-4:] == '.dat':
            nfiles +=1
print 'nfiles: ',nfiles
set_return((datdir,nfiles))