import time
import qt
import os
ts = time.localtime()
timestr, = args
kw = kwargs
datestr = kw.pop('datestr','%d%02d%02d'%(ts.tm_year,ts.tm_mon,ts.tm_mday))
datfol = qt.scripts['find_data_folder'](timestr, datestr = datestr)
datname = os.path.split(datfol)[1]
execfile(os.path.join(datfol,'process_data.py'))
plt.savefig(os.path.join(datfol,datname+'_processed.png'))