#remove_all_plots
import matplotlib.pyplot as plt
import numpy as np
ax = plt.axes()

ls = ax.get_lines()
lines = [ls[kk] for kk in range(len(ls))]
for l in lines:
    l.remove()
plt.draw()