import matplotlib.pyplot as plt
import os
import numpy as np
import pickle
try:
    spec2d, = args
    kw = kwargs
except:
    pass
    kw={}
fig = plt.figure('3dplot_traces')
plt.clf()
ax = plt.subplot(111)
mdat = spec2d.get_data()
fpath = os.path.split(spec2d.get_filepath())[0]
nbl = spec2d.get_nblocks()
valcors = np.shape(mdat)[1]
ntr = np.shape(mdat)[0]/nbl
mdat = mdat.reshape(nbl,ntr,valcors)
dx = mdat[1,0,1]- mdat[0,0,1]
dy = mdat[0,1,0]- mdat[0,0,0]
valdim = kw.pop('valdim',2)
y, x = np.mgrid[slice(mdat[0,0,1], mdat[-1,0,1]+dx, dx),
                slice(mdat[0,0,0], mdat[0,-1,0]+dy, dy)]
ylab = spec2d.get_dimensions()[1]['name']
xlab = spec2d.get_dimensions()[0]['name']
clab = spec2d.get_dimensions()[valdim]['name']
z = mdat[:,:,valdim]
z = (z.transpose()/np.average(z[:,:40],1)).transpose() #Normalize
#z = 10*np.log(z**2/50)/np.log(10);clab =  'log(' + clab +')'# take the log
cmap = plt.get_cmap('spectral')

kk=0
#print c_ind
xa = mdat[0,:,0]
ya = mdat[:,0,1]
drange=kw.pop('range',[0,len(z)])
drange=range(drange[0],drange[1])
c_ind = np.arange(1.*len(drange))/len(drange)
incr = kw.pop('incr',0.)
for z_i in z[drange]:
    #print len(x)
    #print cmap(c_ind[kk])
    plt.plot(xa,z_i+kk*incr,color=cmap(c_ind[kk]),label = '%s: %s'%(kk,ya[kk]));kk+=1
plt.legend(loc = kw.pop('loc',1),fontsize=kw.pop('fsize','x-small'))
plt.xlabel(xlab)
plt.ylabel(clab)

#plt.clim(0.11,1.17)
#plt.ylim((mdat[0,0,1], mdat[-1,0,1]))
#plt.xlim((mdat[0,0,0], mdat[0,-1,0]))
plt.title(spec2d.get_time_name())
#cbar = plt.colorbar()
#cbar.set_label(clab)
plt.savefig(os.path.join(fpath,spec2d.get_name())+'_traces.png')
#plt.ioff()
#pickle.dump(ax, file(os.path.join(fpath,spec2d.get_time_name())+'.pickle', 'w'))
#plt.ion()
#ax = pickle.load(file(os.path.join(fpath,spec2d.get_time_name())+'.pickle')))


