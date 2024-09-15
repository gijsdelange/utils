import xmltodict
from math import radians, cos, sin, asin, sqrt
import time,os
import numpy as np
import matplotlib.pyplot as plt
import shutil
from garmin_fit_sdk import Decoder, Stream
import datetime



def moving_average(x, N):
    return np.convolve(np.array(N*[np.average(x[:N])]+x.tolist()+N*[np.average(x[-N:])]), np.ones((N,))/N)[int((3*N/2-1)):-3*int(N/2)]

fname = '2024-09-10-081145.fit'#'2020-07-23-104600.fit'#'2020-07-20-095400.tcx'#'2020-07-23-104600.tcx'
ptitle = 'Test'
fpath = r'D:/Onedrives/OneDrive/Documenten/Hardlopen/Activities/'
try:
    fname,ptitle,fpath, = args
except:
    fname = fname
    ptitle = ptitle
    fpath = fpath

filepath = os.path.join(fpath, fname)
print(filepath)

lap_keys = {#'timestamp', 
            # 'start_time':1, 
            'start_position_lat':[1/(2**32/360), 'start lat'],
            'start_position_long':[1/(2**32/360), 'start long'],
            'end_position_lat':[1/(2**32/360), 'end lat'],
            'end_position_long':[1/(2**32/360), 'end long'],
            'total_elapsed_time':[1, 'lap time (s)'] ,
            'total_distance':[1e-3, 'total_distance (km)'], 
            'enhanced_avg_speed':[3.6, 'speed (km/h)'],  
            'message_index':[1, 'lap_index'], 
            'avg_power':[1, 'Power (W)'], 
            'total_calories': [1, 'total calories (cal)'],
            'total_ascent':[1, 'total_ascend'], 
            'total_descent':[1, 'total_descent'], 
            'normalized_power':[1, 'Norm. Power (W)'], 
            'avg_vertical_oscillation':[0.1, 'avg. vertical oscillation (cm)'], 
            'avg_stance_time_percent':[1, 'avg. gct percentage (%)'], 
            'avg_stance_time':[1, 'gct (ms)'], 
            'avg_vertical_ratio':[1, 'avg. vertical ratio'], 
            'avg_stance_time_balance':[1, 'avg. gct balance (%)'], 
            'avg_step_length':[1e-3, 'avg. stride distance (m)'], 
            'enhanced_avg_respiration_rate':[1, 'avg. respiration rate (breath/min)'], 
            'avg_heart_rate':[1, 'avg. HR (bpm)'], 
            'max_heart_rate':[1, 'HR_max (bpm)'], 
            'avg_cadence':[2, 'avg. cadence (steps/min)'], 
            'total_strides':[1, 'total strides'], 
            'avg_running_cadence':[2, 'avg. running cadence (steps/min)']}
#print(lap_keys)
record_keys = {#'timestamp':[1, 'timestamp'], 
                'position_lat':[1/(2**32/360), 'lat'], 
                'position_long':[1/(2**32/360), 'long'], 
                'distance':[1e-3, 'distance'], 
                'accumulated_power':[1, 'acc. power (W)'], 
                'enhanced_speed':[3.6, 'speed (km/h)'], 
                'enhanced_altitude':[1, 'alt. (m)'],
                'power':[1, 'power (W)'], 
                'vertical_oscillation':[0.1, 'vertical oscillation (cm)'], 
                'stance_time_percent':[1, 'gct (%)'], 
                'stance_time':[1, 'gct (ms)'], 
                'vertical_ratio':[1, 'vertical ratio'], 
                'stance_time_balance':[1, 'gct balance (%)'], 
                'step_length':[1e-3, 'stride length (m)'], 
                'heart_rate':[1, 'HR (bpm)'], 
                'cadence':[2, 'cadence (steps/min)'] }
def get_lap_data(fitfile):
    lapmesgs = fitfile['lap_mesgs']
    nlaps = len(lapmesgs)    
    times = (nlaps*2-1)*[None]
    times[::2] = [lapmesgs[kk]['start_time'] for kk in range(nlaps)]
    times[1::2] = times[2::2]
    datadict = {'start times (s)':times}
    stimes = (nlaps*2-1)*[None]
    stimes[::2] = [lapmesgs[kk]['total_elapsed_time'] for kk in range(nlaps)]
    stimes[1::2] = stimes[2::2]
    datadict = {'lap times (s)':np.array(stimes)}
    for key in lap_keys.keys():
        
        lapdat = (nlaps*2-1)*[None]
        try:
            lapdat[::2] = [lap_keys[key][0]*lapmesgs[kk][key] for kk in range(nlaps)]
        except:
            for kk in range(nlaps):
                try:
                    lapdat[2*kk] = lap_keys[key][0]*lapmesgs[kk][key]
                except:
                    pass
        lapdat[1::2] = lapdat[2::2]
        datadict[lap_keys[key][1]] = lapdat
    return datadict

def get_record_data(fitfile):
    recmesgs = fitfile['record_mesgs']
    nrecs = len(recmesgs)        
    times = [recmesgs[kk]['timestamp'] for kk in range(nrecs)]
    datadict = {'timestamps':times}
    stimes = [(recmesgs[kk]['timestamp']-recmesgs[0]['timestamp']).seconds for kk in range(nrecs)]
    datadict = {'times':np.array(stimes)}
    for key in record_keys.keys():  
        dat = []
        for kk in range(nrecs):
            try:
                dat += [record_keys[key][0]*recmesgs[kk][key] ]
            except:
                dat += [None]
                
        datadict[record_keys[key][1]] = dat
    return datadict
# tcx = xmltodict.parse(open(fpath+fname,'rb'))
# laps = tcx['TrainingCenterDatabase']['Activities']['Activity']['Lap']

# def rename_tcx(fpath):
#     flist = os.listdir(fpath)
#     for fil in flist:
#         if len(fil) == 22:
#             oldname = os.path.join(fpath,fil)
#             tcx = xmltodict.parse(open(oldname,'rb'))
#             Id = tcx['TrainingCenterDatabase']['Activities']['Activity']['Id']
#             print(Id)
#             ts = time.strptime(Id,'%Y-%m-%dT%H:%M:%S.000Z')
#             print(ts)
#             newname = time.strftime('%Y-%m-%d-%H%M%S',ts)+'.TCX'
#             print('renaming: ', fil,' to: ', newname)
#             os.rename(oldname,os.path.join(fpath,newname))
def smooth(dat,n_avg):
    if False:
        fft_v = np.fft.fft(dat)
        lenv =  len(dat)
        sigma = lenv/2./n_avg
        
        n_g =  1./(np.sqrt(2*np.pi)*sigma)
        ker =np.exp(-(np.arange(lenv/2+1)/(2.*sigma))**2).tolist()
        fft_vf = fft_v*np.array(ker[:-1]+ker[::-1][:-1])       
        smthv_tot = np.fft.ifft(fft_vf)
        retval = np.abs(smthv_tot)
    else:
        
        retval = moving_average(np.array(dat),n_avg)
    return retval            
           
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
stream = Stream.from_file(filepath)
decoder = Decoder(stream)
messages, errors = decoder.read()
VO2max = (messages['140'][0][7]/65536.0 * 3.5 * 10.0) / 10.0
lap_data = get_lap_data(messages)
record_data = get_record_data(messages)

ts_tot = []
t_tot = record_data['times']

x_tot = record_data['distance']
hrm_tot = record_data['HR (bpm)']
pos_tot = [[record_data['lat'][kk], record_data['long'][kk]] for kk in range(len(record_data['lat']))]
alt_tot = record_data['alt. (m)']
cad_tot = record_data['cadence (steps/min)']
speed_tot = record_data['speed (km/h)']

n_lap =[]
t_lap = lap_data['lap time (s)']
dx_lap = lap_data['total_distance (km)']
hra_lap = lap_data['avg. HR (bpm)']
hrm_lap = lap_data['HR_max (bpm)']
cal_lap = lap_data['total calories (cal)']
gct_lap = lap_data['gct (ms)']
pos_lap = [[lap_data['end lat'][kk], lap_data['end long'][kk]] for kk in range(len(lap_data['end lat']))]


dx_tot = np.diff(1.*np.array(x_tot))

from scipy.signal import savgol_filter
t_tot = np.array(t_tot)-t_tot[0]        
pos_tot = np.array(pos_tot)
delta_t = np.average(np.diff(t_tot))
window = 2*int(np.round(17/delta_t)/2)+1

#print('window = ', window)
order = 1

def smooth_pos(pos_tot):
    pos_tot = np.array(pos_tot)
    sm_pos = 0*pos_tot
    
    sm_pos[:,0] = savgol_filter(pos_tot[:,0], window, order)
    sm_pos[:,1] = savgol_filter(pos_tot[:,1], window, order)
    return sm_pos

def get_dx_tot(pos_tot):
    #print('pos_tot = ', len(pos_tot))
    
    sm_pos = smooth_pos(pos_tot)
    dx_tot = np.zeros(len(pos_tot)-1)
    for kk in range(len(sm_pos)-1):
        lat1 = sm_pos[kk,0]
        lon1 = sm_pos[kk,1]
        lat2 = sm_pos[kk+1,0]
        lon2 = sm_pos[kk+1,1]
        dx_tot[kk] = haversine(lon1, lat1, lon2, lat2)
    return dx_tot

nselector = (pos_tot!=None)[:,0]
pos_tot = pos_tot[nselector,:]
dx_tot = get_dx_tot(pos_tot)
x_tot = np.array(x_tot)[nselector]
#dt_arr, dx_tot = get_ndiff(t_tot, dx_tot, 4)
#print (dt_arr)

v_tot = 3.6*dx_tot/np.diff(1.*t_tot[nselector])
#print('v_tot ',v_tot)
#v_tot = dx_tot/dt_arr
#v_tot = v_tot[:int(len(v_tot)/2)*2]
#t_tot = t_tot[:int(len(v_tot))+1]
t_tot = t_tot[nselector]

hrm_tot = np.array(hrm_tot)[nselector]
print(len(t_tot), len(v_tot), len(hrm_tot))


plt.figure('Overview: %s'%fname, figsize=(8,10))
plt.clf()

ax = plt.subplot(511)
plt.title(ptitle+': '+fname+ '\n VO2max: %.2f'%(VO2max))
plt.plot(t_tot[1:],v_tot,'.',label = 'raw v')

try:    
    v_tot_sp = np.array(speed_tot)[selector]
    plt.plot(t_tot[1:],v_tot_sp,'.',label = 'raw v speed')
except:    
    pass


n_avg = 6
smthv_tot = smooth(v_tot,n_avg)
plt.plot(t_tot[1:],smthv_tot,'-',label = 'smooth v')      
plt.legend(fontsize='xx-small')

plt.subplot(512, sharex = ax)
plt.plot(t_tot,hrm_tot,'.')    

smthr_tot = smooth(hrm_tot,n_avg)
plt.plot(t_tot,smthr_tot,'-', label = 'HR')    
plt.legend(fontsize='xx-small')
hrdiffs = np.abs(np.diff(hrm_tot))<2
hr2diffs = [False]+list(np.abs(np.diff(hrdiffs))<2)
hrselector = np.array([False]+ list(hr2diffs*hrdiffs))

#vdiffs = np.array([False]+ list(np.abs(np.diff(smthv_tot))<0.2))

vselector = np.array([False]+ list(np.abs(np.diff(smthv_tot))<0.5))
vminselector = smthv_tot>0
t_selector = (t_tot<1900)*(t_tot>300) # boven limiet is zodat alleen gekeken wordt naar HS en v in frisse toestand
#print(len(t_tot), len(t_selector))
#print('[hrselector, vselector, vminselector, t_selector]')
#print([len(sel) for sel in [hrselector, vselector, vminselector, t_selector]])
selector = hrselector[1:]*vselector*vminselector*t_selector[1:]

plt.plot(t_tot[1:][selector], smthr_tot[1:][selector], '.')
plt.subplot(511)
plt.plot(t_tot[1:][selector], smthv_tot[selector], label = 'selected')
plt.legend()
plt.ylim(4,16)

#break_
plt.subplot(513)
#print(len(smthv_tot), len(selector))
#print(len(hrm_tot), len(selector))
plt.plot(smthv_tot[:len(selector)][selector], np.array(hrm_tot)[:len(selector)][selector],'.-',label = 'HR vs V')
plt.plot(smthv_tot[:len(selector)][selector][0], np.array(hrm_tot)[:len(selector)][selector][0],'g.')
plt.ylim((115,200))
plt.legend(fontsize='xx-small') 
plt.savefig(fpath+fname[:-3]+'png')
after = [smthv_tot[:len(selector)][selector],np.array(hrm_tot)[:len(selector)][selector]]
#print(len(t_tot),len(v_tot),len(alt_tot))
results = {'tot':{'ts_tot':ts_tot,
                't_tot':t_tot,
                'x_tot':x_tot,
                'dx_tot':dx_tot,
               #'hra_tot':hra_tot,
                'hrm_tot':hrm_tot,
                'pos_tot':pos_tot,
                'alt_tot':np.array(alt_tot)[nselector],
                'smth_v':smthv_tot,
                'smth_hr':smthr_tot,
                'cad_tot':np.array(cad_tot)[nselector]},
           
            'laps':{'n_lap':n_lap,
                't_lap':t_lap,
                'dx_lap':dx_lap,
                'hrm_lap':hrm_lap,
                'hra_lap':hra_lap,
                'cal_lap':cal_lap,
                'gct_lap':gct_lap,
                'pos_lap':pos_lap},
            'VO2max':VO2max}
plt.subplot(514)
#print('laltot: ',len(alt_tot))
#print('lttot: ',len(t_tot))
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
        
        plt.plot(t_tot[1:],np.diff(x_tot[:])*1e3,'.',label = 'dx_distance')
        plt.plot(t_tot[1:],(dx_tot[:]),'.',label = 'dx')
    except:
        plt.plot(t_tot[1:],(dx_tot[:]),'.',label = 'dx')
plt.legend(fontsize='xx-small')
plt.subplot(515)
sm_pos = smooth_pos(pos_tot)
plt.plot(np.array(pos_tot[:,1]),np.array(pos_tot[:,0]), '.')
plt.plot(np.array(pos_tot[0,1]),np.array(pos_tot[0,0]),'go')
plt.plot(np.array(pos_tot[-1,1]),np.array(pos_tot[-1,0]),'ro')
plt.plot(np.array(sm_pos[:,1]),np.array(sm_pos[:,0]),'-')
try:
    set_return((after,results,messages, lap_data, record_data))
except:
    print('executed as script')