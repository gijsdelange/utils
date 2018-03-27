#mpl_plot_data
#namespace = globals()
import time
import os
import sys
import qt
import matplotlib.pyplot as plt
import numpy as np

read_settings = qt.scripts['read_settings']

if type(args[0])==type('') or type(args[0])==type(0):
    loaddatafile=True
    timestr=args[0]
    if type(args[0])==type(0):
        timestr='%s'%args[0]


    kw = kwargs.copy()
    ts = time.localtime()
    datestr = kw.pop('datestr','%d%02d%02d'%(ts.tm_year,ts.tm_mon,ts.tm_mday))
    basedir = 'D:/qtlab/data/'+datestr
    dirlist = os.listdir(basedir)
    found_data = False
    for dirstr in dirlist:
        #print type(dirstr)
        #print dirstr.find(timestr)
        if dirstr.find(timestr)>-1:
            datdir = os.path.join(basedir,dirstr)
            print 'found data: ',datdir
            found_data = True
            break
    if not found_data:
        print 'Data file not found'
        sys.exit()





else: #Data object given as argument
    loaddatafile=False
    kw = kwargs.copy()
    dat = args[0]
    timestr=dat._timemark
    datestr = dat._datemark
    dirstr = dat.get_time_name()
    datdir = dat.get_dir()
    settings=[]

traces = kwargs.pop('traces',None)
norm = kw.pop('norm', False)

if not kw.pop('append',False):
    plt.figure(datestr+'_'+timestr, figsize=(8,4))
    pname = datestr+'_'+timestr
    plt.cla()
    nlines = 0
    ax = plt.gca()
else:
    ax = plt.gca()
    nlines = len(ax.get_lines())+1

if not kw.pop('tickoffset',0):
    ax.ticklabel_format(useOffset=False)

if traces==None:
    pname = '%s'%(timestr)
    if loaddatafile==True:
        print os.path.join(datdir,os.path.split(datdir)[1]+'.dat')
        dat = qt.Data(os.path.join(datdir,os.path.split(datdir)[1]+'.dat'), name =pname)
        settings = read_settings(os.path.join(datdir,os.path.split(datdir)[1]+'.set'))
    xy = dat.get_data()
    valdim = kw.pop('valdim',0)
    kw['valdim'] = valdim
    if type(valdim)==type([]):
        #print np.shape(xy)
        y=xy[:,(dat.get_ncoordinates()+np.array(valdim)).tolist()]
        print '1',y
    else:
        #one trace
        y = np.array([xy[:,dat.get_ncoordinates()+valdim]]).transpose()
        valdim = [valdim]
        #print '1',np.shape(y),y[:,0]
    if norm:
        y/=np.average(y[:20])
    ylab = dat.get_values()
    x=xy[:,kw.pop('coordim',0)]
    kk=0
    offset = kw.pop('offset',0.)
    labs = kw.pop('labs','')
    if type(labs) == type({}):
        lab = ' %s: %s'%(labs['instr'],settings[labs['instr']][labs['par']])
    else:
        lab = ''

    print ylab
    ylab = dat.get_values()
    xlab = dat.get_dimensions()[0]['name']
    for vdim in valdim:
        print kk
        plt.plot(x,y[:,kk]+(kk+1)*offset, label = pname+'_'+ylab[vdim]['name']+lab)
        kk+=1
    ylab = ylab[vdim]['name']
else:
    pname = '%s'%(timestr)
    flist = os.listdir(datdir)
    kk=0
    fs2plot = []
    cmap = plt.get_cmap('spectral')


    crange = (1.*np.arange(nlines+len(traces)))/(nlines+len(traces))
    dat = qt.Data(os.path.join(datdir,os.path.split(datdir)[1]+'.dat'), name =pname)
    # dat2d = qt.Data(name='spec2d_T1')
    # dat2d.add_coordinate('F (MHz)')
    # dat2d.add_coordinate('delay (ns)')
    # dat2d.add_value('S21 ch1')
    # #dat2d.add_value('S21 ch2')
    # dat2d.create_file(filepath = datdir)
    labs = kw.pop('labs',len(traces)*[''])


    valdim = kw.pop('valdim',1)
    offset = kw.pop('offset',0)
    plt.subplots_adjust(right=0.8,left=0.1)
    for ntrace in traces:

        for fl in flist:
            if (fl.find('%s_'%ntrace) ==0) and (fl.find('.dat')):
                fs2plot+=[fl]
                print 'plotting: ',fl
                pname = '%s_%s'%(ntrace,timestr)
                dat = qt.Data(os.path.join(datdir,fl), name =pname)

                settings = read_settings(os.path.join(datdir,fl)[:-4]+'.set')
                xy = dat.get_data()
                print np.shape(xy)
                if np.shape(xy)==(0L,):
                    print 'data not yet ready, skipping!!!'
                    break
                ylab = dat.get_dimensions()[1]['name']
                xlab = dat.get_dimensions()[0]['name']
                x=xy[:,kw.pop('coordim',0)]

                y=xy[:,valdim]
                print type(labs)

                if type(labs) == type({}):
                    lab = ' %s: %s'%(labs['instr'],settings[labs['instr']][labs['par']])
                else:
                    lab = ': '+labs[kk]

                if norm:
                    print 'norm'
                    y = y/np.average(y[:20])
                plt.plot(x,y+(kk+1)*offset,label = pname[:-7]+lab, color = kw.pop('color',cmap(crange[kk])))
                #dat2d.add_data_point(x,xy[:,1],xy[:,2])
                #dat2d.new_block()
                kk+=1

                break

plt.xlim((min(x),max(x)))
plt.xlabel(xlab)
plt.ylabel(ylab)
title = kw.pop('title',datestr+': '+dirstr)
if title != datestr+': '+dirstr:
    title += '\n'+ dat.get_filepath()
plt.title(title, fontsize = 'small')
#plt.legend(loc = kw.pop('loc',2),fontsize='x-small')
box = ax.get_position()
#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
plt.subplots_adjust(left=0.15,right=0.75)
# Put a legend to the right of the current axis
if kw.pop('legend', True):
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),fontsize='x-small')
plt.savefig(os.path.join(datdir,dirstr+kw.pop('name','')+'_mplot.png'))
#print fs2plot
co = {}
(co['x'],co['y'],co['settings'], co['figloc'], co['dat']) =  (x,y,settings,os.path.join(datdir,dirstr+'_mplot.png'),dat)
set_return(co)     