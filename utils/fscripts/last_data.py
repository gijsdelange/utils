#find_last_data
import time
import os
kw = kwargs
ts = time.localtime()
datestr = kw.pop('datestr','%d%02d%02d'%(ts.tm_year,ts.tm_mon,ts.tm_mday))
basedir = 'D:/qtlab/data/'+datestr
dirlist = os.listdir(basedir)
dirlist.sort()
ts = dirlist[-1][:6]

set_return('%s'%ts)