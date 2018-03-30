#x,y,z = args
import numpy as np
import matplotlib.pyplot as plt
import os
import utils.fscripts as fscripts
print('ik doe nu iets')
moving_average = fscripts.scripts['moving_average']
x,y,z = args
kw = kwargs
dx = x[1]- x[0]
dy = y[1]-y[0]
coll_outp = {}
if kw.pop('log',0):
    z= np.log(z)/np.log(10)
title = kw.pop('title','')

y, x = np.mgrid[slice(x[0]-dx/2, x[-1]+dx, dx),
                slice(y[0]-dy/2, y[-1]+dy, dy)]
#print('x,y: ',np.shape(y),np.shape(x))

cmap = plt.get_cmap(kw.pop('cmap','spectral'))
coll_outp['cmap']=cmap
figname = kw.pop('figname','mplot3d'+title)
add_cursor = fscripts.scripts['add_cursor']
nrm = kw.pop('norm',False) #['method', args]
clab = kw.pop('clab','')
if nrm:
    kernel = nrm[1]
    avg = (np.average(z[:,:kernel])+np.average(z[:,-kernel:],1))/2.
    z = ((z.transpose())/avg).transpose();
    clab =  'Normalized ' + clab  #Normalize
if not kw.pop('append',False):
    plt.figure(figname)
    plt.clf()
mov_avg = kw.pop('mov_avg',[False,0,0])
if mov_avg[0]:
    try:
        axis = mov_avg[2]
    except:
        axis=0
        
    if axis==1:
        zavg = z.transpose()
    else:
        zavg = z
    #print 'ma axis: ',axis
    for ii in range(len(zavg)):
        
        zavg[ii]= moving_average(np.arange(len(zavg[ii])),zavg[ii],mov_avg[1])
    
    if axis==1:
        z = zavg.transpose()
    else:
        z=zavg   
shz = np.shape(z)
#print 'shz: ',shz
ax = kw.pop('ax', plt.gca())
if kw.pop('contour',False):
    x=x[0:shz[1],0:shz[0]]
    y=y[0:shz[1],0:shz[0]]
    plt.contour(x, y, z.transpose(),20)
else:
    x=x[0:shz[1]+1,0:shz[0]+1]
    y=y[0:shz[1]+1,0:shz[0]+1]
    
    if kw.pop('transpose', False):
        print('transpose')
        im = ax.pcolormesh(y.transpose(),x.transpose(), z, cmap=cmap)
    else:
        im = ax.pcolormesh(x, y, z.transpose(), cmap=cmap)

coll_outp['ax'] = ax
if kw.pop('cursor',False):
    curs = add_cursor(ax,[x,y,z.transpose()])
else:
    curs=None
coll_outp['cursor'] = curs
coll_outp['imax'] = im
xlab=kw.pop('xlab','x')
ylab=kw.pop('ylab','y')
clab=kw.pop('clab','z')
plt.title(title)
if kw.pop('cbar',True):
    cbar = plt.colorbar(mappable = im)
    cbar.set_label(clab, rotation = -90)
else:
    cbar=None
coll_outp['cbar'] = cbar
plt.xlabel(xlab)
plt.ylabel(ylab)
clim = kw.pop('clim',False)
if clim:
    
    im.set_clim(clim)
datdir = kw.pop('datdir','')
if datdir is not '':
    #print datdir
    plt.savefig(os.path.join(datdir,figname+'.png'))
set_return(coll_outp)