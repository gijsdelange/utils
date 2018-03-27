#remove_last_line
import matplotlib.pyplot as plt
import numpy as np
ax = plt.axes()

ls = ax.get_lines()
lines = [ls[kk] for kk in range(len(ls))]

lines[-1].remove()
plt.draw()