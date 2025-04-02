import sys, os
import numpy as np
sys.path.append('D:\\Codes\\others\\FoamPy')

import matplotlib.pyplot as plt
import figurePlot as ft
import foam as of

time = of.getLatestTime('../postProcessing/line1', True)

data = np.loadtxt('../postProcessing/line1/'+time+'/line_U.xy')
exp = np.loadtxt('exp.txt')

xrange=[0, 0.5]   # x axis range
yrange=[0, 1.4]   # y axis range
  
xtickStep = 0.1
xminorStep = 0.05
  
ytickStep = 0.2
yminorStep = 0.1
  
ticksStep = [xtickStep, xminorStep, 
             ytickStep, yminorStep, 
             xrange[0], xrange[1],
             yrange[0], yrange[1]]
             
xyLabel=['$\\mathrm{\\it{r/D}}$', '$\\mathrm{\\it{u/U_0}}$']

moveCoeff=[0.2, 0.25]
tightCoeff=[0.9, 0.17, 0.96, 0.2]

fontSize = 24

width = 8.2
height = 6.0
fig, ax=plt.subplots(1,figsize=(width,height), dpi=600)

plt.plot(data[:,0]/0.006, data[:,3]/-272, color='k', label='Present', linewidth=1.75)
plt.plot(exp[:,0], exp[:,1], 's', markeredgecolor='b', markerfacecolor='none', label='Exp', markersize=6)

ft.figureProperty(fontSize, ticksStep, moveCoeff, tightCoeff, xyLabel, ax, plt, 1)
ft.save('velocity_out', plt)

