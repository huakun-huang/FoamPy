import sys, os
import numpy as np
sys.path.append('/mnt/d/Codes/others/FoamPy')

import matplotlib.pyplot as plt
import figurePlot as ft
import foam as of

def plot(figureName, time, location, expAsh, expZhe, labels):
    data = np.loadtxt('../postProcessing/'+location+'/'+time+'/line_U.xy')
    expA = np.loadtxt('exptData/'+expAsh)
    expZ = np.loadtxt('exptData/'+expZhe)
    xrange=[0, 0.4]   # x axis range
    yrange=[0, 1.2]   # y axis range
  
    xtickStep = 0.1
    xminorStep = 0.05
  
    ytickStep = 0.2
    yminorStep = 0.1
  
    ticksStep = [xtickStep, xminorStep, 
             ytickStep, yminorStep, 
             xrange[0], xrange[1],
             yrange[0], yrange[1]]
             
    xyLabel=['$\\mathrm{\\it{y/B}}$', '$\\mathrm{\\it{u/U_0}}$']

    moveCoeff=[0.2, 0.25]
    tightCoeff=[0.9, 0.17, 0.96, 0.2]

    fontSize = 24

    width = 8.2
    height = 6.0
    fig, ax=plt.subplots(1,figsize=(width,height), dpi=600)
    
    plt.text(0.3, 1.1, labels)
    
    plt.plot(expA[:,0], expA[:,1], 's', label='$\\mathrm{Ash}$', markeredgecolor='b', markerfacecolor='none',  markersize=6)
    plt.plot(expZ[:,0], expZ[:,1], 'o', label='$\\mathrm{Zhe}$', markeredgecolor='r', markerfacecolor='none',  markersize=6)
    plt.plot(data[:,0]/0.04, data[:,1]/7.9, color='k', label='$\\mathrm{SSTCDLM}$', linewidth=1.75)
    
    ft.figureProperty(fontSize, ticksStep, moveCoeff, tightCoeff, xyLabel, ax, plt)
    ft.save(figureName, plt)
    plt.close()
    

time = of.getLatestTime('../postProcessing/v1Graph', True)
for n in range(8):
    figureName = 'v'+repr(n+1)
    expA = 'Ashv'+repr(n+1)
    expZ = 'Zhev'+repr(n+1)
    location = 'v'+repr(n+1)+'Graph'
    label = '$\\mathrm{\\it{x/B='+repr(n+1)+'}}$'
    plot(figureName, time, location, expA, expZ, label)

