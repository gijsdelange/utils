import matplotlib.pyplot as plt
import numpy as np
import time


    

def live_plot(xs, ys, ax = plt.gca(), fig = plt.gcf(), replace_last = True, c = 'b', label = ''):
    
    if replace_last:     
        line = ax.get_lines()[-1]
        line.set_xdata(xs)
        line.set_ydata(ys)
    else:
        ax.plot(xs, ys, color = c, label = label)
    ax.relim(visible_only=True)
    ax.autoscale_view();
    fig.canvas.draw()
    QtGui.QGuiApplication.processEvents()