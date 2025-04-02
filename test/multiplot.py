import math as mt
import numpy as np
import matplotlib.pyplot as plt
import math as mt
import os
from matplotlib import rcParams

import matplotlib.pyplot as plt
import figurePlot as ft
import foam as of

def twoPlot():
    time = of.getLatestTime('processor0')
    data1 = np.loadtxt('./postProcessing/sets/'+time+'/inlet_p_U.xy')
    data2 = np.loadtxt('./postProcessing/sets/'+time+'/axial_p_U.xy')
    
    Lc = 25.4e-3
    Uc = 340
    p0 = 1e5
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 6))
    
    #first figurePlot
    ax1.plot(data1[:,0]/Lc, -data1[:,4]/Uc, color=ft.cls(1), linewidth=3)
    ax2.plot(data1[:,0]/Lc, data1[:,1]/p0, color=ft.cls(2), linewidth=3)
    
    xyRange = [0, 0.5, 0, 4]
    xyLabel=['$\\mathrm{\\it{r/D}}$ \n $\\mathrm{(a)}$', '$\\mathrm{\\it{U/Uc}}$']
    ft.plot(ax1, plt, xyRange, xyLabel=xyLabel)
    
    xyRange = [0, 0.5, 0, 8]
    xyLabel=['$\\mathrm{\\it{r/D}}$ \n $\\mathrm{(b)}$', '$\\mathrm{\\it{p/p_0}}$']
    ft.plot(ax2, plt, xyRange, xyLabel=xyLabel)
    
    plt.savefig('supersonic.png', bbox_inches='tight')
    plt.close()

def fourPlot():
    time = of.getLatestTime('processor0')
    data1 = np.loadtxt('./postProcessing/sets/'+time+'/inlet_p_U.xy')
    data2 = np.loadtxt('./postProcessing/sets/'+time+'/axial_p_U.xy')
    
    Lc = 25.4e-3
    Uc = 340
    p0 = 1.4e5 

    fig, axs = plt.subplots(2, 2, figsize=(8, 6))
    ax1 = axs[0,0]
    ax2 = axs[0,1]
    ax3 = axs[1,0]
    ax4 = axs[1,1]
    
    #first figurePlot
    ax1.plot(data1[:,0]/Lc, -data1[:,4]/Uc, color=ft.cls(2), linewidth=1.75)
    ax2.plot(data1[:,0]/Lc, data1[:,1]/p0, color=ft.cls(2), linewidth=1.75)
    ax3.plot(data2[:,0]/Lc, -data2[:,4]/Uc, color=ft.cls(2), linewidth=1.75)
    ax4.plot(data2[:,0]/Lc, data2[:,1]/p0, color=ft.cls(2), linewidth=1.75)

    fontSize = 14
    xyRange = [0, 0.5, 0, 2]
    xyLabel=['$\\mathrm{\\it{r/D}}$ \n $\\mathrm{(a)}$', '$\\mathrm{\\it{U/Uc}}$']
    ft.plot(ax1, plt, xyRange, xyLabel=xyLabel, lenSize=fontSize)
    
    xyRange = [0, 0.5, 0, 8]
    xyLabel=['$\\mathrm{\\it{r/D}}$ \n $\\mathrm{(b)}$', '$\\mathrm{\\it{p/p_a}}$']
    ft.plot(ax2, plt, xyRange, xyLabel=xyLabel, lenSize=fontSize) 

    xyRange = [0, 3, 0, 4]
    xyLabel=['$\\mathrm{\\it{H/D}}$ \n $\\mathrm{(c)}$', '$\\mathrm{\\it{U/U_c}}$']
    ft.plot(ax3, plt, xyRange, xyLabel=xyLabel, lenSize=fontSize)    

    xyRange = [0, 5, 0, 8]
    xyLabel=['$\\mathrm{\\it{H/D}}$ \n $\\mathrm{(d)}$', '$\\mathrm{\\it{p/p_a}}$']
    ft.plot(ax4, plt, xyRange, xyLabel=xyLabel, lenSize=fontSize)  

    plt.savefig('supersonic.png', bbox_inches='tight')
    plt.close()    
    
fourPlot()
fourPlot()    
