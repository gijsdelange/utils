#Calculates the number of photons present in a resonator
# input Pin, f, Ql, Qc, T in dBm, GHz,#,#,K
#Returns {n_P, n_Thermal}
#n_P is the number of photons present due to input power
#n_Thermal is the number of photons present due to thermal excitations
from utils import physcon as pc
import numpy as np
hbar, k_B = pc.hbar, pc.k_B
Pin, f, Ql, Qc, T = args
omega = 2.*np.pi*f*1e9
n_Thermal = 1./(np.exp(hbar*omega/k_B/T)-1.)
n_P = 4./hbar/omega**2*Ql**2/Qc*10**(Pin/10.)/1.e3
set_return({'n_P':n_P, 'n_Thermal':n_Thermal})