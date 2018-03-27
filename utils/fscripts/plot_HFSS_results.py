# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 17:49:18 2015

@author: Gijs
"""
import numpy as np
import pickle

import matplotlib.pyplot as plt
try:
    fpath, = args
except:
    print 'use as script'
    fpath = r'D:\Simulations\HFSS_results\20150616\183543 - resonator_length'
    fpath = r'D:\Simulations\HFSS_results\20150616\172109 - resonator_length'
    fpath = r'D:\Simulations\HFSS_results\20150617\130754 - resonator_length'
    fpath = r'D:\Simulations\HFSS_results\20150617\140807 - resonator_length'
    fpath = r'D:\Simulations\HFSS_results\20150617\142754 - Lumped Inductance' #l = 8.6mm
    #fpath = r'D:\Simulations\HFSS_results\20150617\150759 - Lumped Inductance'
    #fpath = r'D:\Simulations\HFSS_results\20150617\154719 - Lumped Inductance'
    fpath = r'D:\Simulations\HFSS_results\20150617\183441 - Resonator length' #change inductance with length
    fpath = r'D:\Simulations\HFSS_results\20150617\185550 - Resonator length' #change inductance with length
    ### A bug made the actual length in sims twice longer!
    #fpath = r'D:\Simulations\HFSS_results\20150617\203303 - Lumped Inductance' #l = 0.01
    fpath = r'D:\Simulations\HFSS_results\20150618\102556 - Lumped Inductance' #l=0.009
    fpath = r'D:\Simulations\HFSS_results\20150618\112031 - Lumped Inductance' # l= 0.0085
    fpath = r'D:\Simulations\HFSS_results\20150618\122613 - Resonator length'# resonator length with inductance=> f too low
    fpath = r'D:\Simulations\HFSS_results\20150618\131719 - Resonator length' # #
    #fpath = r'D:\Simulations\HFSS_results\20150618\133809 - Resonator length'
    fpath = r'D:\Simulations\HFSS_results\20150619\222304 - Resonator length' #direction is 90 (0.65 mm is wrong)
    fpath = r'D:\Simulations\HFSS_results\20150619\223156 - Resonator length' #direction is 0
    fpath = r'D:\Simulations\HFSS_results\20150619\224732 - Resonator length' #shortmeander
    fpath = r'D:\Simulations\HFSS_results\20150620\221805 - Resonator length'
    fpath = r'D:\Simulations\HFSS_results\20150622\095306 - Resonator length' # new geometry
    fpath = r'D:\Simulations\HFSS_results\20150622\122032 - Resonator length'
    fpath = r'D:\Simulations\HFSS_results\20150622\130401 - Lumped Inductance'
    fpath = r'D:\Simulations\HFSS_results\20150622\133151 - Lumped Inductance'
    fpath = r'D:\Simulations\HFSS_results\20150622\141141 - Dipole length'
    fpath = r'D:\Simulations\HFSS_results\20150622\141448 - Dipole length'
res = pickle.load(open(fpath+r'/'+fpath[46:]+'.pickle','r'))


vals = res['vals'].keys()
vals.sort()
nmodes = len(res['vals'][vals[0]]['Q']['val'])
fs = np.zeros([len(vals),nmodes])
Qs = np.zeros([len(vals),nmodes])
nbends = np.zeros([len(vals)])
for kk,val in enumerate(vals):
    Q_ = res['vals'][val]['Q']['val']
    inds = Q_.argsort()
    Qs[kk,:] = Q_[inds]
    fs[kk,:] = res['vals'][val]['fres']['val'][inds]
    nbends =  res['vals'][val]['n_bends']

plt.figure('eigmode_results_'+res['sweepname'])
plt.clf()
plt.subplot(211)
plt.title(fpath+'\nR=0.001, width = 1 $\mu$m')
plt.plot(np.array(vals),Qs, 'o-')
plt.ylabel('Q')
plt.yscale('log')
#plt.xscale('log')
plt.subplot(212)
plt.plot(np.array(vals),fs, 'o-')
plt.ylabel('f (GHz)')
plt.xlabel('%s (%s)'%(res['sweepname'],res['setval_unit']))
#plt.xscale('log')
plt.tight_layout()
plt.savefig(fpath+r'/%s.pdf'%res['sweepname'])

import lmfit