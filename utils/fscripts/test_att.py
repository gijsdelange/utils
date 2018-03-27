import qt
import matplotlib.pyplot as plt
import numpy as np
from time import time
VATT = qt.instruments['VATT']
HM = qt.instruments['HM']
ATS = qt.instruments['ATS']
def set_att_and_probe(att):
    VATT.set_attenuation(att)
    
    if att >80:
        ATS.set_ch1_range(1)
    elif 50<att<=80:
        ATS.set_ch1_range(1)
    else:
        ATS.set_ch1_range(1)
    ATS.configure_board()
    qt.msleep(0.3)
    t0 = time()
    s21 = 0.+0.j
    s21 += HM.probe(1, mtype='COMP')
    dat = ATS.get_data()[0]
    print 't: ',time()-t0,'s, att: ',att,', ATSrange: ',ATS.get_ch1_range(),', max: ',np.max(dat)
    return np.abs(s21)
atts = range(0,120,10)
amptest = [set_att_and_probe(att) for att in atts]

plt.figure('amptest')

plt.plot(atts, 20*np.log(amptest)/np.log(10))