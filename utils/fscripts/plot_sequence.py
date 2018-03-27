#check wfms
wfs = MSQ.generate_AWG_measurement_waveform()
colors = ['r','b','g']
ch=1
plt.figure('waveforms')
plt.clf()
for wf in wfs:
    kk = 0
    for ach in wf:
        
        ax = plt.subplot(311+kk)
        plt.plot(ach,label='ch%s_%s'%(ch,kk))
        kk+=1
        plt.ylim(-1.2,1.2)
curs = add_cursor(ax,[None,None])
plt.legend(fontsize='small')
