import sys, os
import numpy as np
sys.path.append('/mnt/d/Codes/others/FoamPy')
sys.path.append('/home/hhk/Codes/others/FoamPy')

import matplotlib.pyplot as plt
import figurePlot as ft
import foam as of

def contours():
    data = np.loadtxt('cuttingPlate.csv', delimiter=',', skiprows=1)
    lc = 0.017 #m
    Ma = 0.3
    Uc = 340*Ma
    p0 = 101325
    rhoc = 1.1716
    T0 = 298
    
    r = data[:,3]/lc
    z = data[:,5]/lc
    T = data[:,8]/T0
    Ux = data[:, 9]/Uc
    Uz = data[:,11]/Uc
    dialation= data[:,13]*lc/Uc
    k = data[:, 18]
    p = (data[:, 22]-p0)/(0.5*Uc*Uc*rhoc)
    rho = data[:,23]/rhoc
    
    mag=[]
    for mm in range(len(Ux)):
        value = Ux[mm]**2+Uz[mm]**2
        mag.append(value**0.5)

    xyLabel=['$\\mathrm{\\it{r/D}}$', '$\\mathrm{\\it{z/D}}$']
    fig, ax=plt.subplots(1,figsize=(8.2,4.0), dpi=600)
    Range =[0, 6, 0, 1]
    legendlabel = '$\\mathrm{\\it{C_p}}$'
    level = []
    direction = 'vertical'
    skip = 2
    for n in range(16):
        level.append(round(n*0.2, 2))
    lenSize = 20
    ft.contourPlot(fig, ax, r, z, Range, p, level, direction, skip, lenSize, legendlabel)
    
    ft.plot(ax, plt, Range, xyLabel, [0,0], lenSize)
    plt.savefig('Ma_03_Q3000_Cp.pdf', bbox_inches='tight')
    plt.close()
    
    ################ rho ###############################
    xyLabel=['$\\mathrm{\\it{r/D}}$', '$\\mathrm{\\it{z/D}}$']
    fig, ax=plt.subplots(1,figsize=(8.2,4.0), dpi=600)
    Range =[0, 6, 0, 1]
    legendlabel = '$\\mathrm{\\it{\\rho/\\rho_{0}}}$'
    level = []
    direction = 'vertical'
    skip = 3
    for n in range(21):
        num = round(n*0.02+0.8,2)
        level.append(num)
    lenSize = 20
    ft.contourPlot(fig, ax, r, z, Range, rho, level, direction, skip, lenSize, legendlabel)
    
    ft.plot(ax, plt, Range, xyLabel, [0,0], lenSize)
    plt.savefig('Ma_03_Q3000_rho.pdf', bbox_inches='tight')    
    
    ################ U ###############################
    xyLabel=['$\\mathrm{\\it{r/D}}$', '$\\mathrm{\\it{z/D}}$']
    fig, ax=plt.subplots(1,figsize=(8.2,4.0), dpi=600)
    Range =[0, 4, 0, 0.25]
    legendlabel = '$\\mathrm{\\it{U_{mag}/U_{c}}}$'
    level = []
    direction = 'vertical'
    skip = 3
    for n in range(21):
        num = round(n*0.06,2)
        level.append(num)
    lenSize = 20
    ft.contourPlot(fig, ax, r, z, Range, mag, level, direction, skip, lenSize, legendlabel)
    
    ft.plot(ax, plt, Range, xyLabel, [0,0], lenSize)
    plt.savefig('Ma_03_Q3000_U.pdf', bbox_inches='tight') 

contours()
contours()


