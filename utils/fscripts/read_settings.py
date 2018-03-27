# get_settings for data file
import time
import qt,os
filepath, =args
kw = kwargs
ts = time.localtime()
datestr = kw.pop('datestr','%d%02d%02d'%(ts.tm_year,ts.tm_mon,ts.tm_mday))
if len(filepath) == 6:
    filepath = qt.scripts['find_data_folder'](filepath,datestr = datestr)[0]
    apptr = kw.pop('trace', '')
    
    if apptr != '':
        apptr = '%s_'%apptr  
        #print apptr    
        #print type(apptr)
        #print os.path.split(filepath)[1]
    filepath+='\\' + apptr+os.path.split(filepath)[1]+'.set'   
    #print filepath
f = open(filepath,'r')
fc = f.readlines()
f.close()
#print fc
setdic = {}
kk=0
while kk<len(fc):
    insf = 'Instrument: '
    found = fc[kk].find(insf)
    if found >-1:
        instr = fc[kk][found+len(insf):fc[kk].find('\n')]
        kk+=1
        setdic[instr]={}
        #print  kk,fc[kk].find('\t'),(fc[kk].find('\t')>-1)
    
        while (fc[kk].find('\t')>-1):
            key = fc[kk][1:fc[kk].find(': ')]
            #print  kk,len(fc),fc[kk][fc[kk].find(': ')+2:-1]
            try:
                #print 'not bla'
                setdic[instr][key] = float(fc[kk][fc[kk].find(': ')+2:-1])
            except:
                #print 'BLA'
                setdic[instr][key] = fc[kk][fc[kk].find(': ')+2:-1]
            kk+=1
            if kk==(len(fc)-1):
                break
            #print (fc[kk].find('\t')>-1)
    else:
        kk+=1
f.close()
set_return(setdic)            
        