import sys, os
import numpy as np
sys.path.append('/mnt/d/Codes/others/FoamPy')

import matplotlib.pyplot as plt
import figurePlot as ft
import foam as of

def plot(figureName, probeNum):
    data = np.loadtxt('../postProcessing/probes/0.56816/p')
    x = data[:,0]
    y = data[:,probeNum]/(0.5*10*10*1.1716)
    
    minY = min(y)
    maxX = max(x)
    maxY = max(y)
    minX = min(x)
    
    xrange=[minX, maxX]   # x axis range
    yrange=[minY, maxY]   # y axis range
  
    xtickStep = round((maxX-minX)/5., 2)
    xminorStep = xtickStep/2.
  
    ytickStep = round((maxY-minY)/5., 2)
    yminorStep = ytickStep/2.
  
    ticksStep = [xtickStep, xminorStep, 
             ytickStep, yminorStep, 
             xrange[0], xrange[1],
             yrange[0], yrange[1]]
             
    xyLabel=['$\\mathrm{\\it{t}} [s]$', '$\\mathrm{\\it{C_p}}$']

    moveCoeff=[0.2, 0.0025]
    tightCoeff=[0.9, 0.17, 0.96, 0.2]

    fontSize = 24

    width = 8.2
    height = 6.0
    fig, ax=plt.subplots(1,figsize=(width,height), dpi=600)
    
    plt.plot(x, y, color='k', label='$\\mathrm{Machine \\ Learning}$', linewidth=1.75)
    
    ft.figureProperty(fontSize, ticksStep, moveCoeff, tightCoeff, xyLabel, ax, plt, 2)
    ft.save(figureName, plt)
    plt.close()


for n in range(1,7):
    figure = 'p'+repr(n)
    plot(figure, n) 
   