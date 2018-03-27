#Loads data
#Args = timestr, traces
#traces : Which traces to take.
#
#Output dictionary = 'Data', 'Array'
#Data is the full Data object
#Array is the data within the Data object
import qt
import numpy as np
import os

find_data = qt.scripts['find_data_folder']
timestr, traces = args
kw = kwargs

datdir = find_data(timestr, **kw)[0]
pname = '%s'%(timestr)
#print (datdir)
if traces != None:
    app = '%s_'%traces[0]
else:
    app=''
dat = qt.Data(os.path.join(datdir,app+os.path.split(datdir)[1]+'.dat'),name = os.path.split(datdir)[1])
xy = dat.get_reshaped_data()
#print np.shape(xy)
valdim = kw.pop('valdim',0)
#x=xy[:,kw.pop('coordim',0)]
#y=xy[:,(dat.get_ncoordinates()+np.array(valdim)).tolist()]
output = {'Data':dat, 'Array':xy}
set_return(output)