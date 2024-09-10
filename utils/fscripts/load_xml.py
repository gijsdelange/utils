import xmltodict
from math import radians, cos, sin, asin, sqrt
import time,os
import numpy as np
import matplotlib.pyplot as plt
import scripts


def moving_average(x, N):
    return np.convolve(np.array(N*[np.average(x[:N])]+x.tolist()+N*[np.average(x[-N:])]), np.ones((N,))/N)[int((3*N/2-1)):-3*int(N/2)]

fname = '2020-07-23-104600.tcx'#'2020-07-20-095400.tcx'#'2020-07-23-104600.tcx'
ptitle = 'Test'
fpath = r"D:\Onedrives\OneDrive\Documenten\Hardlopen\Activities//"
try:
    fname,ptitle,fpath, = args
except:
    fname = fname
    ptitle = ptitle
    fpath = fpath

tcx = xmltodict.parse(open(fpath+fname,'rb'))
laps = tcx['TrainingCenterDatabase']['Activities']['Activity']['Lap']

def rename_tcx(fpath):
    flist = os.listdir(fpath)
    for fil in flist:
        if len(fil) == 22:
            oldname = os.path.join(fpath,fil)
            tcx = xmltodict.parse(open(oldname,'rb'))
            Id = tcx['TrainingCenterDatabase']['Activities']['Activity']['Id']
            print(Id)
            ts = time.strptime(Id,'%Y-%m-%dT%H:%M:%S.000Z')
            print(ts)
            newname = time.strftime('%Y-%m-%d-%H%M%S',ts)+'.TCX'
            print('renaming: ', fil,' to: ', newname)
            os.rename(oldname,os.path.join(fpath,newname))
def smooth(dat,n_avg):
    if False:
        fft_v = np.fft.fft(dat)
        lenv =  len(dat)
        sigma = lenv/2./n_avg
        print('averaging: ',n_avg)
        n_g =  1./(np.sqrt(2*np.pi)*sigma)
        ker =np.exp(-(np.arange(lenv/2+1)/(2.*sigma))**2).tolist()
        fft_vf = fft_v*np.array(ker[:-1]+ker[::-1][:-1])       
        smthv_tot = np.fft.ifft(fft_vf)
        retval = np.abs(smthv_tot)
    else:
        print(dat)
        retval = moving_average(np.array(dat),n_avg)
    return retval            
#stophere            

ts_tot=[]
t_tot = []
dx_tot=[]
x_tot=[]
hra_tot =[]
hrm_tot =[]
pos_tot =[]
alt_tot = []
cad_tot = []
speed_tot = []

n_lap =[]
t_lap =[]
dx_lap =[]
hrm_lap =[]
hra_lap =[]
cal_lap = []
pos_lap =[]
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
if type(laps)!=list:
    laps=[laps]
    
for lap in laps[:]:
    n_lap +=[nn]
    t_lap +=[float(lap["TotalTimeSeconds"])]
    dx_lap +=[float(lap["DistanceMeters"])]
    #hrm_lap +=[float(lap["MaximumHeartRateBpm"]['Value'])]
    hra_lap +=[float(lap["AverageHeartRateBpm"]['Value'])]
    #cal_lap +=[float(lap["Calories"])]
    nn+=1
    if type(lap["Track"])==type([]):
        print('list')
        trackpoints = []
        for lp in lap["Track"]:
            trackpoints += lp['Trackpoint']
    else:
        print('dict')
        trackpoints = lap["Track"]['Trackpoint']
    kk=0
    for tp in trackpoints[:]:
        print('last_time',last_time)
        print('tp: ',tp)
        if tp=='Time':
            pass
        
        elif last_time == tp['Time']:
            pass
        else:    
            if True:#if True:#
                
                #print tp
                #print tp['AltitudeMeters']
                try:
                    cad_tot += [2*float(tp['Extensions']['ns3:TPX']['ns3:RunCadence'])]
                    
                    #print('cadence added')
                except:
                    pass
                try:
                    speed_tot+=[3.6*float(tp['Extensions']['ns3:TPX']['ns3:Speed'])]
                except:
                    try:
                        del speed_tot
                    except:
                        pass
                try:
                    alt_tot+=[float(tp['AltitudeMeters'])]
                
                    #print 'ok1'
                    pos_tot +=[[ float(tp['Position']['LatitudeDegrees']), float(tp['Position']['LongitudeDegrees']) ]]
                    #print 'ok2'
                    #tp=tp['Trackpoint'][0]
                    hrm_tot +=[float(tp['HeartRateBpm']['Value'])]
                    #print 'ok3'
                    x_tot +=[float(tp['DistanceMeters'])]
                    
                    #print(tp['Time'])
                    #print len(t_tot), len(dx_tot) 
                    try:
                        ts = time.strptime(tp['Time'],'%Y-%m-%dT%H:%M:%SZ')
                    except:
                        ts = time.strptime(tp['Time'],'%Y-%m-%dT%H:%M:%S.000Z')
                    ts_tot += [ts]
                    #print('ok51')
                    t_tot += [ts.tm_hour*3600 + ts.tm_min*60 + ts.tm_sec]
                    #print len(t_tot), len(dx_tot) 
                    #print('added')    
                    kk+=1
                except:
                    pass
            
            last_time = tp['Time']
            #print(len(t_tot), len(dx_tot), len(pos_tot) ,kk)
dx_tot = np.diff(1.*np.array(x_tot))

from scipy.signal import savgol_filter
t_tot = np.array(t_tot)-t_tot[0]        
pos_tot = np.array(pos_tot)
delta_t = np.average(np.diff(t_tot))
window = 2*int(np.round(17/delta_t)/2)+1

print('window = ', window)
order = 1

def smooth_pos(pos_tot):
    pos_tot = np.array(pos_tot)
    sm_pos = 0*pos_tot
    
    sm_pos[:,0] = savgol_filter(pos_tot[:,0], window, order)
    sm_pos[:,1] = savgol_filter(pos_tot[:,1], window, order)
    return sm_pos

def get_dx_tot(pos_tot):
    print('pos_tot = ', len(pos_tot))
    
    sm_pos = smooth_pos(pos_tot)
    dx_tot = np.zeros(len(pos_tot)-1)
    for kk in range(len(sm_pos)-1):
        lat1 = sm_pos[kk,0]
        lon1 = sm_pos[kk,1]
        lat2 = sm_pos[kk+1,0]
        lon2 = sm_pos[kk+1,1]
        dx_tot[kk] = haversine(lon1, lat1, lon2, lat2)
    return dx_tot


dx_tot = get_dx_tot(pos_tot)

#dt_arr, dx_tot = get_ndiff(t_tot, dx_tot, 4)
#print (dt_arr)

v_tot = 3.6*dx_tot/np.diff(1.*t_tot)
#print('v_tot ',v_tot)
#v_tot = dx_tot/dt_arr
v_tot = v_tot[:int(len(v_tot)/2)*2]
t_tot = t_tot[:int(len(v_tot))+1]
hrm_tot = hrm_tot[:len(v_tot)]
plt.figure('Overview: %s'%fname, figsize=(8,10))
plt.clf()

ax = plt.subplot(511)
plt.title(ptitle+': '+fname)
plt.plot(t_tot[:(len(v_tot))],v_tot,'.',label = 'raw v')
try:    
    v_tot_sp = np.array(speed_tot)
    plt.plot(t_tot[:(len(v_tot_sp))],v_tot_sp,'.',label = 'raw v speed')
except:    
    pass


n_avg = 6
smthv_tot = smooth(v_tot,n_avg)
plt.plot(t_tot[:(len(v_tot))],smthv_tot,'-',label = 'smooth v')      
plt.legend(fontsize='xx-small')

plt.subplot(512, sharex = ax)
plt.plot(t_tot[:(len(v_tot))],hrm_tot,'.')    

smthr_tot = smooth(hrm_tot,n_avg)
plt.plot(t_tot[:(len(v_tot))],smthr_tot,'-', label = 'HR')    
plt.legend(fontsize='xx-small')
hrdiffs = np.abs(np.diff(hrm_tot))<2
hr2diffs = [False]+list(np.abs(np.diff(hrdiffs))<2)
hrselector = np.array([False]+ list(hr2diffs*hrdiffs))

#vdiffs = np.array([False]+ list(np.abs(np.diff(smthv_tot))<0.2))

vselector = np.array([False]+ list(np.abs(np.diff(smthv_tot))<0.5))
vminselector = smthv_tot>0
t_selector = (t_tot<1900)*(t_tot>660) # boven limiet is zodat alleen gekeken wordt naar HS en v in frisse toestand
print(len(t_tot), len(t_selector))
selector = hrselector*vselector*vminselector*t_selector[:len(vselector)]

plt.plot(t_tot[:len(vselector)][selector], smthr_tot[:len(selector)][selector], '.')
plt.subplot(511)
plt.plot(t_tot[:len(vselector)][selector], smthv_tot[:len(selector)][selector], label = 'selected')
plt.legend()
plt.ylim(4,16)

#break_
plt.subplot(513)
print(len(smthv_tot), len(selector))
print(len(hrm_tot), len(selector))
plt.plot(smthv_tot[:len(selector)][selector], np.array(hrm_tot)[:len(selector)][selector],'.-',label = 'HR vs V')
plt.plot(smthv_tot[:len(selector)][selector][0], np.array(hrm_tot)[:len(selector)][selector][0],'g.')
plt.ylim((130,200))
plt.legend(fontsize='xx-small') 
plt.savefig(fpath+fname[:-3]+'png')
after = [smthv_tot[:len(selector)][selector],np.array(hrm_tot)[:len(selector)][selector]]
print(len(t_tot),len(v_tot),len(alt_tot))
results = {'tot':{'ts_tot':ts_tot,
            't_tot':t_tot,
            'x_tot':x_tot,
            'dx_tot':dx_tot,
            'hra_tot':hra_tot,
            'hrm_tot':hrm_tot,
            'pos_tot':pos_tot,
            'alt_tot':alt_tot,
            'smth_v':smthv_tot,
            'smth_hr':smthr_tot,
            'cad_tot':cad_tot},
            'laps':{'n_lap':n_lap,
            't_lap':t_lap,
            'dx_lap':dx_lap,
            'hrm_lap':hrm_lap,
            'hra_lap':hra_lap,
            'cal_lap':cal_lap,
            'pos_lap':pos_lap}}
plt.subplot(514)
print('laltot: ',len(alt_tot))
print('lttot: ',len(t_tot))
if 0:
    try:
        try:
            plt.plot(t_tot[:],alt_tot[:],'-',label = 'altitude')
        except:
            plt.plot(t_tot[:],alt_tot[:-1],'-',label = 'altitude')
    except:
        pass
if 1:
    try:
        plt.plot(t_tot[:-1],(dx_tot[:]),'.',label = 'dx')
        plt.plot(t_tot[:-1],np.diff(x_tot[:]),'.',label = 'dx_distance')
    except:
        plt.plot(t_tot[:],(dx_tot[:]),'.',label = 'dx')
plt.legend(fontsize='xx-small')
plt.subplot(515)
sm_pos = smooth_pos(pos_tot)
plt.plot(np.array(pos_tot[:,1]),np.array(pos_tot[:,0]), '.')
plt.plot(np.array(pos_tot[0,1]),np.array(pos_tot[0,0]),'go')
plt.plot(np.array(pos_tot[-1,1]),np.array(pos_tot[-1,0]),'ro')
plt.plot(np.array(sm_pos[:,1]),np.array(sm_pos[:,0]),'-')
try:
    set_return((after,results,tcx))
except:
    print('executed as script')