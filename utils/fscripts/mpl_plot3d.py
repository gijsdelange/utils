#spec2d,
# args: either timestr or data object
import matplotlib.pyplot as plt
import os
import numpy as np
import pickle
import sys
import qt
import time

try:
    spec2d, = args
    kw = kwargs.copy()
except:
    pass
    kw={}
collection = {}    
#print type('')
add_cursor = qt.scripts['add_cursor']
moving_average = qt.scripts['moving_average']
if type(spec2d)==type('') or type(spec2d)==type(1):
    #print 'string data'
    timestr = spec2d
    if type(timestr) == type(1):
        timestr='%s'%timestr
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
            
            
            spec2d = qt.Data(os.path.join(datdir,os.path.split(datdir)[1]+'.dat'), name=os.path.split(datdir)[1][7:])
            spec2d._timemark = timestr
            nbl = spec2d.get_nblocks()
            #print nbl
            break
elif type(spec2d).__name__=='Data':
    timestr=spec2d._timemark
    datestr=spec2d._datemark
if type(spec2d)==type(''):
    print 'data not found!!!'
if not kw.pop('append',False):
    fig = plt.figure(timestr+'_3dplot',figsize=(8,5))
    plt.clf()
    ax = plt.subplot(111)
else:
    ax = plt.axes()

plt.title(kw.pop('title',''))

mdat = spec2d.get_data()
fpath = os.path.split(spec2d.get_filepath())[0]
nbl = spec2d.get_nblocks()
#print 'nbl: ',nbl
valcors = np.shape(mdat)[1]
ntr = np.shape(mdat)[0]/nbl
try:
    mdat = mdat.reshape(nbl,ntr,valcors)
except:
    
    nbl-=1
    ntr = np.shape(mdat)[0]/nbl
    mdat = mdat.reshape(nbl,ntr,valcors)
    print 'data not ready, removing last block: ', nbl,ntr, np.shape(mdat)



convert_x = kw.pop('convert_x',False)
convert_y = kw.pop('convert_y',False)
if convert_x:
    mdat[:,:,1] = convert_x(mdat[:,:,1])
if convert_y:
    mdat[:,:,0] = convert_y(mdat[:,:,0])
collection['x'] = mdat[:,0,1]
collection['y'] = mdat[0,:,0]


dx = mdat[1,0,1]- mdat[0,0,1]
dy = mdat[0,1,0]- mdat[0,0,0]    
#print dx,dy
#print 'x: ',mdat[0,0,1],mdat[-1,0,1], dx, np.shape(slice(mdat[0,0,1]-dx/2., mdat[-1,0,1]+dx/2., dx))    
#print 'y: ',mdat[0,0,0],mdat[0,-1,0], dy, np.shape(slice(mdat[0,0,0]-dy/2., mdat[0,-1,0]+dy/2., dy))

valdim = kw.pop('valdim',2)
y, x = np.mgrid[slice(mdat[0,0,1]-dx/2., mdat[-1,0,1]+dx, dx),
                slice(mdat[0,0,0]-dy/2., mdat[0,-1,0]+dy, dy)]
ylab = spec2d.get_dimensions()[1]['name']
xlab = spec2d.get_dimensions()[0]['name']
clab = spec2d.get_dimensions()[valdim]['name']
z = mdat[:,:,valdim]
#print 'x',np.shape(x)
#print 'y',np.shape(y)
#print 'z',np.shape(z)
shz = np.shape(z)
x=x[0:shz[0]+1,0:shz[1]+1]
y=y[0:shz[0]+1,0:shz[1]+1]
#print 'x',np.shape(x)
#print 'y',np.shape(y)
#print 'z',np.shape(z)
if kw.pop('log',False):
    z = 10*np.log(z**2/50)/np.log(10);clab =  'log(' + clab +')'# take the log
mov_avg = kw.pop('mov_avg',[False,0])
if mov_avg[0]:
    zavg = z
    for ii in range(len(zavg)):
        
        zavg[ii]= moving_average(np.arange(len(zavg[ii])),zavg[ii],mov_avg[1])
    z=zavg
if kw.pop('norm',False):
    avg = (np.average(z[:,:20],1)+np.average(z[:,-20:],1))/2.
    z = ((z.transpose()-avg)*avg).transpose();
    clab =  'Normalized ' + clab  #Normalize        
if kw.pop('norm_div',False):
    avg = (np.average(z[:,:20],1)+np.average(z[:,-20:],1))/2.
    z = ((z.transpose())/avg).transpose();
    clab =  'Normalized ' + clab  #Normalize
    
cmap = plt.get_cmap(kw.pop('cmap','spectral'))
#print type(y)
alpha = kw.pop('alpha',1)
if kw.pop('transpose',False):
    im = plt.pcolormesh(y.transpose(), x.transpose(), z.transpose(), cmap=cmap, alpha=alpha, rasterized = kw.pop('rasterized',False))
    plt.xlabel(ylab)
    plt.ylabel(xlab)
    if kw.pop('cursor',False):
        cursor = add_cursor(ax,(y.transpose(), x.transpose(), z.transpose()))
    else:
        cursor=None
    #plt.clim(0.11,1.17)
    plt.xlim((mdat[0,0,1], mdat[-1,0,1]))
    plt.ylim((mdat[0,0,0], mdat[0,-1,0]))

else:

    im = plt.pcolormesh(x, y, z, cmap=cmap,alpha=alpha, rasterized = kw.pop('rasterized',False))
    if kw.pop('cursor',False):
        cursor = add_cursor(ax,(x, y, z))
    else:
        cursor=None
    plt.xlabel(xlab)
    plt.ylabel(ylab)

    #plt.clim(0.11,1.17)
    plt.ylim((mdat[0,0,1], mdat[-1,0,1]))
    plt.xlim((mdat[0,0,0], mdat[0,-1,0]))
#print 'xlim',(mdat[0,0,0], mdat[0,-1,0])
xcor = (min([mdat[0,0,1], mdat[-1,0,1]]))
#print 'xcor',xcor
tycor=kw.pop('tycor',7.8)
plt.text(xcor,tycor,datestr+': '+spec2d._timemark, fontsize='x-small')
if kw.pop('cbar',True):
    cbar = plt.colorbar()
    cbar.set_label(clab,rotation = -90, labelpad = 20)
else:
    cbar= None
collection['cbar'] = cbar
collection['cursor'] = cursor
collection['xyz']=(x,y,z)
collection['imax']=im

clim = kw.pop('clim',False)
if clim:
    plt.clim(clim)
#ppath = os.path.join(fpath,'p3d_'+timestr+'_'+datestr+spec2d.get_name())+'.png'
ppath = os.path.join(fpath,spec2d.get_name()+'_plot3D.png')
title = kw.pop('title',spec2d.get_time_name()) + '\n'+spec2d.get_filepath()
plt.title(title,fontsize='small')
if kw.pop('saveplot',True):
    plt.savefig(ppath)
h0 = datestr+'_'+timestr+'\n'
h1 = 'x from %s to %s in %s steps\n'%(mdat[0,0,0],mdat[0,-1,0],len(mdat[0,:,0]))
h2 = 'y from %s to %s in %s steps\n'%(mdat[0,0,1],mdat[-1,0,1],len(mdat[:,0,0]))
if kw.pop('saveplotdata',False):
    np.savetxt(os.path.join(fpath,datestr+'_'+timestr+'_'+spec2d.get_name())+'.txt',z, header=h0+h1+h2)
#plt.ioff()
#pickle.dump(ax, file(os.path.join(fpath,spec2d.get_time_name())+'.pickle', 'w'))
#plt.ion()
#ax = pickle.load(file(os.path.join(fpath,spec2d.get_time_name())+'.pickle')))
collection['path'] = ppath
collection['ax'] = ax
set_return(collection)


