import numpy as np
pi,log = np.pi, np.log
e_ = 1.6e-19
h = 6.62e-34
phi_0 = 2.e-15
hbar = h/2/np.pi
k_B = 1.38e-23
eps_0 = 8.854e-12
mu_0 = 4*np.pi*1e-7

def VtodBm(V):
    '''
    Converts voltage in 50 Ohm to dBm
    '''
    P=(V**2)/50/np.sqrt(2.)
    return 10*np.log(P/1e-3)/np.log(10)

def photon_number(eps, kappa):
    '''
    steady state photon number from drive strenghth eps_d and kappa 
    '''
    n_bar = (2*eps/kappa)**2 #kappa=2pi * decay rate
    return n_bar

def dBm2nbar(P, f0, Ql, Qi):
    '''
    Calculates n_bar for hangers form the power in the feedline
    '''
    Pin = 10**(P/10.)*1e-3
    
    Pres = (1-(1.*Ql/Qi)**2)*Pin
    print Pres
    n_in = Pres/(h*f0)/(f0/Ql)
    return n_in
    
def C_to_Ec(C):
    '''
    returns Ec in GHz from the capacitance
    '''
    return e_**2/2/C/h/1e9

def Ic_to_Ej(Ic):
    '''
    returns Ej in GHz from Ic 
    '''
    return Ic*phi_0/2/pi/h/1e9

def EjEc_to_f(Ej,Ec): 
    '''
    Calculates transmon f_ge from Ec and Ej
    '''
    return np.sqrt(8*Ej*Ec)
def IctoLj(Ic):
    return phi_0/2/np.pi/Ic
    
def IcC_to_f(Ic,C):
    '''
    Calculates transmon f_ge from Ic and C
    '''
    Ec = C_to_Ec(C)
    Ej = Ic_to_Ej(Ic)
    return EjEc_to_f(Ej,Ec)
    