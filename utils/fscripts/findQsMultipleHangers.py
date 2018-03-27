import pickle
# Hangers = [{'descr':'500nm','devno':1,'f':3.9465,'Ql':17500, 'R':5.7e3},# 0
            # {'descr':'500nm GATE','devno':12,'f':4.4921,'Ql':13200,'R':6.2e3},# 1
            # {'descr':'500nm SQUID','devno':3,'f': 4.9484,'Ql':12200,'R':3.5e3},# 2
            # {'descr':'200nm GATE','devno':4,'f': 5.93601,'Ql':7200,'R':3.07e3},# 3
            # {'descr':'200nm SQUID','devno':11,'f': 6.50057,'Ql':7100,'R':2.2e3},  # 4          
            # {'descr':'200nm','devno':2,'f': 6.892,'Ql':5400,'R':3.03e3},# 5
            # {'descr':'100 nm SQUID','devno':7,'f': 7.9505,'Ql':4600,'R':1.4e3},# 6            
            # {'descr':'100nm GATE no wire','devno':8,'f': 8.4404,'Ql':3700,'R':None},# 7            
            # {'descr':'100nm','devno':9,'f': 8.9534,'Ql':3400,'R':2.6e3},#8
            # {'descr':'50nm','devno':5,'f': 10.388,'Ql':None,'R':None},#9
            # {'descr':'50nm','devno':6,'f': 10.878,'Ql':None,'R':None},
            # {1:0,12:1,3:2,4:3,11:4,2:5,7:6,8:7,9:8,5:9,6:10}]# 10

frange = 50e-3 #GHz
devs = [12]
#pvals = np.linspace(-20,0,11)#21)        
HM.set_RF_power(-60)    
for dev in devs:
    hanger = Hangers[Hangers[-1][dev]]
    f = hanger['f'] #GHz
    #fvals = np.linspace(f-frange/2., f + frange/2.,501)*1e9
    fr = find_resonance(f*1e9,5e6,251,dip = True)
    hanger['f']=fr[-2]['f0'].value
    hanger['Ql']=fr[-2]['Q'].value
    hanger['Qi']=fr[-2]['Qi'].value
    hanger['Qc']=fr[-2]['Qc'].value
    plt.close()
    f = open(r'D:\qtlab\data\2DNWTransmon_collection\Hangers.pickle', 'wb')
    pickle.dump(Hangers,f)
    f.close()