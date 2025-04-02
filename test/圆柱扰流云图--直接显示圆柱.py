"""
采用python输出动画
（1）输出切面数据，格式为raw
（2）在ani中指定输出帧数间隔
（3）在140行中指定数据
"""

import numpy as np
#import vtk
#from vtk.util.numpy_support import vtk_to_numpy
#from vtk.util import numpy_support as npvtk
import matplotlib
import matplotlib.pyplot as plt
from numpy import mgrid
#import pyvista as pv
import math as mt
from skimage.measure import marching_cubes

import time as t
import os
import re

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import numpy as np

from scipy.interpolate import griddata 

import foam as of
import figurePlot as ft

     
def colorBarWrite():
    with open('colorBar.txt', 'w') as f:
        f.write('1 2\n2 3')
    f.close()
def colorBarRead():
    data = np.loadtxt('colorBar.txt')
    if(data[0][1]<1):
        colorBarWrite()
        return 0
    else:
        return 1

timeData = of.getTime('./postProcessing/cuttingPlate') 

with open('colorBar.txt', 'w') as f:
    f.write('1 0\n2 3')
f.close()

FFwriter = animation.FFMpegWriter(fps=5)

fig = plt.figure(figsize=(12,8), dpi=300)
gs = gridspec.GridSpec(1, 2, width_ratios=[20, 1], wspace=0.05)
ax = fig.add_subplot(gs[0])
def animate(i):
    ax.clear()
    
    fileName = 'postProcessing/cuttingPlate/'+timeData[i]+'/U_plane.raw'
    data = np.loadtxt(fileName)
    Uref = 0.3939
    Lref = 0.01
    x = data[:,0]/Lref
    y = data[:,1]/Lref
    k = data[:,3]
    
    for ii in range(len(k)):
        k[ii] = mt.sqrt(data[:,3][ii]**2+
                   data[:,4][ii]**2+
                   data[:,5][ii]**2)/Uref
    xi = np.linspace(-4, 8, 400)
    yi = np.linspace(-4, 4, 400)
    [X, Y] = np.meshgrid(xi, yi)
    V = griddata((x,y), k, (X, Y), method='linear')
    
    #create the cylinder
    x0, y0 = 0, 0
    r = 0.005/Lref
    distance = np.sqrt( (X-x0)**2 + (Y-y0)**2)
    mask = (distance <= r)
    V_masked = np.where(mask, np.nan, V)

    levels = np.arange(0, 2.1, 0.1)
    im=ax.contourf(X,Y,V_masked,levels=levels,cmap=matplotlib.cm.jet)
    isoline=ax.contour(X,Y,V,15, linewidths=0.1)
    
    
    xyLabel = ['$\\mathrm{\\it{x/D}}$', '$\\mathrm{\\it{y/D}}$']
    Range = [-4, 8, -4, 4]
    ax.set_aspect('equal')
    k1 = colorBarRead()
    if(k1==0):
        cax = fig.add_subplot(gs[1])
        cBar = fig.colorbar(im, cax=cax) 
        cBar.set_label('$\\mathrm{\\it U_{mag}/U_0}$ $\\mathrm{[m/s]}$ ')
        
    ft.plot(ax, plt, Range, xyLabel=xyLabel, legendOff=True, lenSize=20) 
    ax.set_title('$\\mathrm{t='+timeData[i]+'}$')    
        

print(len(timeData))
ani = animation.FuncAnimation(fig=fig,
    func=animate,
    frames=len(timeData),
    interval=10,
    blit=False)
    
ani.save('velocity.gif', writer = FFwriter)
#plt.show()

"""
for i in range(len(timeData)):      
   fileName = 'postProcessing/cuttingPlate/'+repr(timeData[i])+'/p_planeWater.raw'
   readRaw(fileName, repr(timeData[i]))
"""   
   
#plotContour(fileName)
#x, y, z, k = loadVTPFile(fileName)





