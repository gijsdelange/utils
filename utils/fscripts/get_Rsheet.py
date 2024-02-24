# -*- coding: utf-8 -*-
"""
Created on Tue Dec 01 18:31:53 2015

@author: Gijs de Lange 
@e-mail: gijs.de.l@gmail.com
"""
import numpy as np
from scipy.optimize import fmin 

Rvm, Rhm = args # measurted values for Rh, Rv
print('calculating')
def vanderPauw(Rs,Rv,Rh):
    return np.exp(-np.pi*Rh/Rs) + np.exp(-np.pi*Rv/Rs)

def objective(Rs,Rv,Rh):
    return np.abs(vanderPauw(Rs,Rv,Rh) - 1)**2
    
def R_sheet(Rv,Rh):
    '''
    returns sheet resistance from measure Rh and Rv
    '''
    return fmin(objective, (Rv+Rh)/2, args = (Rv,Rh))[0]

 

set_return(R_sheet(Rvm,Rhm))