# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 15:42:45 2016

@author: gijsd
"""
import matplotlib.pyplot as plt
import numpy as np

shots,bins = args
clim = kwargs.pop('clim', False)
cmap = kwargs.pop('cmap', 'Greys')
ax = kwargs.pop('ax', None)

if ax:
    pass
else:
    plt.subplot(111)
H, xedges, yedges = np.histogram2d(np.real(shots), np.imag(shots),bins)

extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]];
print extent
ax.imshow(np.rot90(H), interpolation='nearest',cmap=cmap, extent=extent)
set_return(H)            