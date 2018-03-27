# combine last# files in one plot
import time
import os
import qt
nfile, = args
kw = kwargs.copy()
mpl_plot_data = qt.scripts['mpl_plot_data']
find_data_folder = qt.scripts['find_data_folder']
ts = time.localtime()
datestr = kw.pop('datestr','%d%02d%02d'%(ts.tm_year,ts.tm_mon,ts.tm_mday))
kw['datestr'] = datestr
basedir = 'D:/qtlab/data/'+datestr
dirlist = os.listdir(basedir)
dirlist.sort()
offset = kw.pop('offset',0)
fname = dirlist[-nfile]
datdir,nfiles = find_data_folder(fname[:6],datestr= datestr)
print 'plotting: ',fname
labs = kw.pop('labs','')
if labs=='':
    pass
else:
    kw['labs'] = labs
if nfiles>1:
    mpl_plot_data(fname[:6], traces = range(1,nfiles+1), append=False,**kw)
else:    
    mpl_plot_data(fname[:6], append=False,**kw)
print range(1,nfiles)[::-1]    
pind=0
for nn in range(1,nfile)[::-1]:
    fname = dirlist[-nn]
    datdir,nfiles = find_data_folder(fname[:6],datestr= datestr)
    print 'plotting: ',fname
    try:
        
        if nfiles>1:
            mpl_plot_data(fname[:6], traces = range(1,nfiles+1),offset=offset*pind, append=True,**kw)
            pind+=1
        else:   
            print 'this'
            pind+=1
            mpl_plot_data(fname[:6], append=True,offset=offset*pind,**kw)
    except:
        print 'file empty, skipping!'
