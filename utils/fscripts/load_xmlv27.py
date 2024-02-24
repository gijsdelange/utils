import xmltodict
from math import radians, cos, sin, asin, sqrt
import time,os
import numpy as np
import matplotlib.pyplot as plt
import scripts


def moving_average(x, N):
    return np.convolve(np.array(N*[np.average(x[:N])]+x.tolist()+N*[np.average(x[-N:])]), np.ones((N,))/N)[(3*N/2-1):-3*N/2]

fname = 'activity_434564776.tcx'
ptitle = 'Ries'
fpath = "D:\\gijsdelange\\My Documents\\Hardlopen\\Activities\\Ries\\"
try:
    fname,ptitle,fpath, = args
except:
    fname = fname
    ptitle = ptitle
    fpath = fpath

tcx = xmltodict.parse(open(fpath+fname,'r'))
laps = tcx['TrainingCenterDatabase']['Activities']['Activity']['Lap']

def rename_tcx(fpath):
    flist = os.listdir(fpath)
    for fil in flist:
        if len(fil) == 22:
            oldname = os.path.join(fpath,fil)
            tcx = xmltodict.parse(open(oldname,'r'))
            Id = tcx['TrainingCenterDatabase']['Activities']['Activity']['Id']
            print Id
            ts = time.strptime(Id,'%Y-%m-%dT%H:%M:%S.000Z')
            print ts
            newname = time.strftime('%Y-%m-%d-%H%M%S',ts)+'.TCX'
            print 'renaming: ', fil,' to: ', newname
            os.rename(oldname,os.path.join(fpath,newname))
def smooth(dat,n_avg):
    if False:
        fft_v = np.fft.fft(dat)
        lenv =  len(dat)
        sigma = lenv/2./n_avg
        print 'averaging: ',n_avg
        n_g =  1./(np.sqrt(2*np.pi)*sigma)
        ker =np.exp(-(np.arange(lenv/2+1)/(2.*sigma))**2).tolist()
        fft_vf = fft_v*np.array(ker[:-1]+ker[::-1][:-1])       
        smthv_tot = np.fft.ifft(fft_vf)
        retval = np.abs(smthv_tot)
    else:
        print dat
        retval = moving_average(np.array(dat),n_avg)
    return retval            
#stophere            

ts_tot=[]
t_tot = []
dx_tot=[]
hra_tot =[]
hrm_tot =[]
pos_tot =[]
alt_tot = []
cad_tot = []

n_lap =[]
t_lap =[]
dx_lap =[]
hrm_lap =[]
hra_lap =[]
cal_lap = []
pos_lap =[]
cad_lap = []
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 

    # 6367 km is the radius of the Earth
    km = 6367 * c
    return 1e3*km
nn=0
last_time = ''
for lap in laps[:]:
    n_lap +=[nn]
    t_lap +=[float(lap["TotalTimeSeconds"])]
    dx_lap +=[float(lap["DistanceMeters"])]
    #hrm_lap +=[float(lap["MaximumHeartRateBpm"]['Value'])]
    #hra_lap +=[float(lap["AverageHeartRateBpm"]['Value'])]
    #cal_lap +=[float(lap["Calories"])]
    nn+=1
    if type(lap["Track"])==type([]):
        print 'list'
        trackpoints = []
        for lp in lap["Track"]:
            trackpoints += lp['Trackpoint']
    else:
        print 'dict'
        trackpoints = lap["Track"]['Trackpoint']
    kk=0
    for tp in trackpoints[:]:
        print 'last_time',last_time
        print 'tp: ',tp
        if tp=='Time':
            pass
        
        elif last_time == tp['Time']:
            pass
        else:    
            if True:#if True:#
                
                #print tp
                #print tp['AltitudeMeters']
                try:
                    cad_tot += [float(tp['Extensions']['RunCadence'])]
                    print('cadence added')
                    
                try:
                    alt_tot+=[float(tp['AltitudeMeters'])]
                
                    #print 'ok1'
                    pos_tot +=[[ float(tp['Position']['LatitudeDegrees']), float(tp['Position']['LongitudeDegrees']) ]]
                    #print 'ok2'
                    #tp=tp['Trackpoint'][0]
                    hrm_tot +=[float(tp['HeartRateBpm']['Value'])]
                    #print 'ok3'
                    dx_tot +=[float(tp['DistanceMeters'])]
                    
                    print  tp['Time']
                    #print len(t_tot), len(dx_tot) 
                    try:
                        ts = time.strptime(tp['Time'],'%Y-%m-%dT%H:%M:%SZ')
                    except:
                        ts = time.strptime(tp['Time'],'%Y-%m-%dT%H:%M:%S.000Z')
                    ts_tot += [ts]
                    print 'ok51'
                    t_tot += [ts.tm_hour*3600 + ts.tm_min*60 + ts.tm_sec]
                    #print len(t_tot), len(dx_tot) 
                    print 'added'    
                    kk+=1
                except:
                    pass
            
            last_time = tp['Time']
            print len(t_tot), len(dx_tot), len(pos_tot) ,kk
t_tot = np.array(t_tot)-t_tot[0]        
pos_tot = np.array(pos_tot)
v_tot = 3.6*np.diff(1.*np.array(dx_tot))/np.diff(1.*t_tot)
v_tot = v_tot[:(len(v_tot)/2)*2]
t_tot = t_tot[:len(v_tot)+1]
hrm_tot = hrm_tot[:len(v_tot)]
plt.figure('Overview: %s'%fname, figsize=(8,10))
plt.clf()

plt.subplot(511)
plt.title(ptitle+': '+fname)
plt.plot(t_tot[1:],v_tot,'.',label = 'raw v')
n_avg = 20

smthv_tot = smooth(v_tot,n_avg)
plt.plot(t_tot[1:],smthv_tot,'-',label = 'smooth v')      
plt.legend(fontsize='xx-small')
  
plt.subplot(512)
plt.plot(t_tot[1:],hrm_tot,'.')    

smthr_tot = smooth(hrm_tot,n_avg)
plt.plot(t_tot[1:],smthr_tot,'-', label = 'HR')    
plt.legend(fontsize='xx-small')
hrselector = np.abs(np.diff(hrm_tot))<2
vselector = np.abs(np.diff(smthv_tot))<0.2
vminselector = smthv_tot[1:]>6
t_selector = (t_tot<1800)*(t_tot>240) # boven limiet is zodat alleen gekeken wordt naar HS en v in frisse toestand
selector = hrselector*vselector*vminselector*t_selector[1:-1]
plt.subplot(511)
#plt.plot(t_tot[1:],4*selector+10)
plt.ylim(4,16)
plt.subplot(513)
plt.plot(smthv_tot[selector],np.array(hrm_tot)[selector],'.-',label = 'HR vs V')
plt.ylim((130,200))
plt.legend(fontsize='xx-small') 
plt.savefig(fpath+fname[:-3]+'png')
after = [smthv_tot[selector],np.array(hrm_tot)[selector]]
print len(t_tot),len(v_tot),len(alt_tot)
results = {'tot':{'ts_tot':ts_tot,
            't_tot':t_tot,
            'dx_tot':dx_tot,
            'hra_tot':hra_tot,
            'hrm_tot':hrm_tot,
            'pos_tot':pos_tot,
            'alt_tot':alt_tot,
            'smth_v':smthv_tot,
            'smth_hr':smthr_tot,
            'cad_tot': cad_tot},
            'laps':{'n_lap':n_lap,
            't_lap':t_lap,
            'dx_lap':dx_lap,
            'hrm_lap':hrm_lap,
            'hra_lap':hra_lap,
            'cal_lap':cal_lap,
            'pos_lap':pos_lap}}
plt.subplot(514)
print 'laltot: ',len(alt_tot)
print 'lttot: ',len(t_tot)
try:
    try:
        plt.plot(t_tot[:],alt_tot[:],'-',label = 'altitude')
    except:
        plt.plot(t_tot[:],alt_tot[:-1],'-',label = 'altitude')
except:
    pass
plt.legend(fontsize='xx-small')
plt.subplot(515)
plt.plot(np.array(pos_tot[:,1]),np.array(pos_tot[:,0]))
plt.plot(np.array(pos_tot[0,1]),np.array(pos_tot[0,0]),'go')
plt.plot(np.array(pos_tot[-1,1]),np.array(pos_tot[-1,0]),'ro')
try:
    set_return((after,results,tcx))
except:
    print 'executed as script'