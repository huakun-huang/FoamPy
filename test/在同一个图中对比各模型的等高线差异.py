import sys, os
import numpy as np
sys.path.append('/mnt/d/Codes/others/FoamPy')

import matplotlib.pyplot as plt
import figurePlot as ft
import foam as of


df = np.loadtxt('Fidelity/velocity/velocity.csv', delimiter=',', skiprows=2)
xf = df[:,0]/0.04
zf = df[:,2]/0.04
Uxf = df[:,3]/8.9

dm = np.loadtxt('ML/velocity/velocity.csv', delimiter=',', skiprows=2)
xm = dm[:,0]/0.04
zm = dm[:,2]/0.04
Uxm = dm[:,3]/8.9

dr = np.loadtxt('RANS/velocity/velocity.csv', delimiter=',', skiprows=2)
xr = dr[:,0]/0.04
zr = dr[:,2]/0.04
Uxr = dr[:,3]/8.9



xrange=[0, 8]   # x axis range
yrange=[0, 0.6]   # y axis range
  
xtickStep = 2
xminorStep = 1
  
ytickStep = 0.1
yminorStep = 0.05
  
ticksStep = [xtickStep, xminorStep, 
             ytickStep, yminorStep, 
             xrange[0], xrange[1],
             yrange[0], yrange[1]]
             
xyLabel=['$\\mathrm{\\it{r/D}}$', '$\\mathrm{\\it{z/D}}$']

moveCoeff=[0.0002, 0.00025]
tightCoeff=[0.9, 0.17, 0.96, 0.2]

fontSize = 24

width = 8.2
height = 6.0
fig, ax=plt.subplots(1,figsize=(width,height), dpi=600)

Range =[xrange[0], xrange[1],yrange[0], yrange[1]]

#ft.isolinePlot(fig, ax, xf, zf, Range, Uxf, 15)
levels = [0.2,  0.4,  0.6, 0.8, 1.0]

color = ('r', 'b', 'k', 
         'm', 'g')
ft.isolinePlot(fig, ax, xm, zm, Range, Uxm, levels, color, 'solid', True)
ft.isolinePlot(fig, ax, xf, zf, Range, Uxf, levels, color, 'dashed', False)
ft.isolinePlot(fig, ax, xr, zr, Range, Uxr, levels, color, 'dashdot', False)

ft.figureProperty(fontSize, ticksStep, moveCoeff, tightCoeff, xyLabel, ax, plt, 3)
ft.save('velocity', plt)
