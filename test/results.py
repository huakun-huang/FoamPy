import math as mt
import numpy as np
import matplotlib.pyplot as plt
import math as mt
import os
from matplotlib import rcParams

import matplotlib.pyplot as plt
import figurePlot as ft
import foam as of

def validate(ax):
    times = of.getLatestTime()
    data = np.loadtxt('postProcessing/center/0.7/line_Ma_U_grad(U).xy')
    x = data[:,0]-0.5
    Ux = data[:,2]
    gradUx = data[:,5]
    Ma = data[:,1]
    
    #A = 0.1+x^2
    gradAx = 2*x
    A = 0.1+x**2
    
    axs=[]
    b1 = A*0
    MaTheory = []
    for mn in range(len(A)):
        M2 = 1 + Ux[mn]/A[mn]*gradAx[mn]/gradUx[mn]
        if M2<0:
            #print(M2, x[mn])
            continue
        MaTheory.append((M2)**0.5)
        axs.append(x[mn])
    
    ax.plot(axs, MaTheory, linestyle=ft.ls(1), color=ft.cls(1), label='$\\mathrm{Theory}$', linewidth=3)
    ax.plot(x, Ma, linestyle=ft.ls(0), color=ft.cls(2), label='$\\mathrm{Present}$', linewidth=3)
    
    xyRange = [-0.5, 0.5, min(Ma), max(Ma)]
    xyLabel=['$\\mathrm{\\it{x}}$ \n $\\mathrm{(a)}$', '$\\mathrm{\\it{Ma}}$']
    ft.plot(ax, plt, xyRange, lenSize=20, xyLabel=xyLabel, axisTopRight=True, gridOff=False)
    
    
def plotAll():
    fig, ax = plt.subplots(1, figsize=(7, 5.))  
    validate(ax)
    plt.savefig('validate.png', bbox_inches='tight')    
    