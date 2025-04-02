# -*- coding: UTF-8 -*-
#import vtk
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties
import matplotlib
import matplotlib.pyplot as plt
from numpy import mgrid
import numpy as np
#import pyvista as pv
import math as mt

try:
    from skimage.measure import marching_cubes
except:
    from skimage.measure import marching_cubes_lewiner as marching_cubes

import matplotlib.animation as animation

from scipy.interpolate import griddata 
import matplotlib.cm as cm
from scipy.interpolate import splrep, splev
import matplotlib.ticker as ticker

#### svg to emf
#import cairosvg
from PIL import Image
#import pyemf3


import subprocess, os
import foam as of

def smoothLine(x, y):
    # 
    f = splrep(x, y)
    xnew = np.linspace(x.min(), x.max(), num=len(x), endpoint=True)
    ynew = splev(xnew, f)
    return xnew, ynew

###### trans figure from svg to emf #######
def svg_to_emf(svg_figpath):
    svg_figpaths = svg_figpath+'.svg'
    emf_figpath = svg_figpath  + '.emf'
    
    inkscapePath = 'inkscape'
    win = of.winOrLinux()
    if(win == 1):
        inkscapePath = '\"C:\\Program Files\\Inkscape\\bin\\inkscape.exe\"'
    subprocess.call("{} {} -T -o {}".format(
            inkscapePath, svg_figpaths, emf_figpath), shell=True)
    
    os.remove(svg_figpaths)
###########################################

###########################################
def cls(n=0):
    color_hex = [
     "#a88462",   # 驼色 7
     "#3b2e7e",  # 藏蓝 6
     "#896c39",  # 秋色 5
     "#0c8918",  # 绿沈 4
     "r",        # 红 3
     "#395260",  # 苍黑 2
     "b",        # 蓝色 1
     "#ffffff"  # 精白 背景 0
    ]
    return color_hex[7-n]

##########################################
def ls(n=0):
    linestyle=[
    'solid',
    'dashed',
    'dotted',
    'dashdot'
    ]
    line2=[
    (0, (3,1,1,1,1,1)),
    (0, (1,1)),
    (0, (5,1)),
    (0, (3,1,1,1)),
    (0, (5, 10)),
    (0, (3, 10,1,10))
    ]
    if n<4:
        return linestyle[n]
    else:
        if n<10:
            return line2[n-4]
        else:
            return linestyle[0]

def arrowDouble(x0, y0, x1, y1, plt):
    headLen = 0.3
    headWid = headLen*0.2
    L = (x0-x1)**2+(y0-y1)**2
    L = L**0.5
    sinTheta = abs(y1-y0)/L
    cosTheta = abs(x1-x0)/L    
    x_center = (x0+x1)/2
    y_center = (y0+y1)/2
    dx = abs(x1-x0)/2-headLen*cosTheta
    dy = abs(y1-y0)/2-headLen*sinTheta
    plt.arrow(x_center, y_center, -dx, -dy, linewidth=0.5, head_width=headWid, head_length=headLen, fc='r', ec='r')
    plt.arrow(x_center, y_center, dx, dy, linewidth=0.5, head_width=headWid, head_length=headLen, fc='r', ec='r')

def arrowSingle(x0, y0, x1, y1, plt):
    headLen = 0.3
    headWid = headLen*0.2
    L = (x0-x1)**2+(y0-y1)**2
    L = L**0.5
    sinTheta = abs(y1-y0)/L
    cosTheta = abs(x1-x0)/L    
    x_center = (x0+x1)/2
    y_center = (y0+y1)/2
    dx = abs(x1-x0)/2*cosTheta-headLen*cosTheta
    dy = abs(y1-y0)/2*sinTheta-headLen*sinTheta
    plt.plot([x0, x_center], [y0, y_center], linewidth=0.5, color='b')
    plt.arrow(x_center, y_center, dx, dy, linewidth=0.5, head_width=headWid, head_length=headLen, fc='b', ec='b') 

################# figure properties #########################
"""
lenSize: font size
ticksStep: x, y ticks
roundNum: ticks round number
"""    
def figureProperty(lenSize, ticksStep, moveCoeff, tightCoeff, xyLabel, ax, plt, roundNum=2):

  Fonts = 'DejaVu Sans'
  #- set font style
  config={
     "font.family":'serif',
     "font.size":lenSize,
     "mathtext.fontset":'stix',
     "font.serif":[Fonts],
  }
  rcParams.update(config)
  plt.subplots_adjust(top =tightCoeff[0], 
          bottom =tightCoeff[1], right = tightCoeff[2], left = tightCoeff[3],
          hspace = 0, wspace = 0);  
  #- set the axis
  # x, y axis move
  axisM=[-ticksStep[1]*moveCoeff[0], -ticksStep[3]*moveCoeff[1]]
  
  
  xtickLabel = [] 
  ytickLabel = [] 

  xticks = [] 
  yticks = [] 
  for mn in range(1000):
      value = round(ticksStep[4]+mn*ticksStep[0], roundNum)
      if value > ticksStep[5]:
          break
      else:
          xticks.append(value)
          labels = '$\\mathrm{'+repr(value)+'}$'
          xtickLabel.append(labels)
  for mn in range(1000):
      value = round(ticksStep[6]+mn*ticksStep[2], roundNum)
      if value > ticksStep[7]:
          break
      else:
          yticks.append(value)
          labels = '$\\mathrm{'+repr(value)+'}$'
          ytickLabel.append(labels)
  ax.tick_params(axis='both', which='major', labelsize=lenSize,
           direction='in', length=4, width=2)
  ax.tick_params(axis='both', which='minor', labelsize=lenSize-4,
           direction='in', length=3, width=1)
  font2 = {'family' : Fonts, 'weight' : 'normal', 'size': lenSize}
  ax.set_ylabel(xyLabel[1], fontsize=lenSize, fontproperties=font2)
  ax.set_xlabel(xyLabel[0], fontsize=lenSize, fontproperties=font2)
  ax.set_xlim(ticksStep[4], ticksStep[5])
  ax.set_ylim(ticksStep[6], ticksStep[7])
  fm = FontProperties(family=Fonts)
  ax.set_xticks(xticks)
  ax.set_yticks(yticks)
  ax.set_xticklabels(xtickLabel, fontproperties=fm, fontsize=lenSize-2)
  ax.set_yticklabels(ytickLabel, fontproperties=fm, fontsize=lenSize-2)
  xm = axisM[0]
  ym = axisM[1]
  for n in range(len(ax.yaxis.get_majorticklabels())):
    ax.yaxis.get_majorticklabels()[n].set_x(xm)
  for n in range(len(ax.xaxis.get_majorticklabels())):
    ax.xaxis.get_majorticklabels()[n].set_y(ym)
  ax.tick_params(right=True)
  ax.tick_params(top=True)

  #- show legend and grid
  legend = ax.legend(fontsize=lenSize-4, frameon=False)
  frame = legend.get_frame()
  frame.set_alpha(1)
  frame.set_facecolor('none') 
  labels = legend.get_texts()
  for mn in range(len(labels)):
      labels[mn].set_fontproperties(Fonts)
    
  ax.grid(False)

##########################################################################
def plot(ax, plt, xyRange, xyLabel=['x', 'y'], legenPos=[0,0], lenSize=24, legendOff=False, axisTopRight=False, gridOff=True):    
    Fonts = 'DejaVu Sans'
    #- set font style
    config={
       "font.family":'serif',
       "font.size":lenSize,
       "mathtext.fontset":'stix',
       "font.serif":[Fonts],
    }
    rcParams.update(config) 
      
    # 设置坐标轴范围
    ax.set_xlim(xyRange[0], xyRange[1])
    ax.set_ylim(xyRange[2], xyRange[3])
    
    # 获取现有的 tick 标签
    xticks = ax.get_xticklabels()
    yticks = ax.get_yticklabels()
    xtickLabel=xticks
    ytickLabel=yticks
    
    # 设置主要和次要刻度
    ax.xaxis.set_major_locator(ticker.FixedLocator(ax.get_xticks()))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator((ax.get_xticks()[1] - ax.get_xticks()[0]) / 2))
    ax.yaxis.set_major_locator(ticker.FixedLocator(ax.get_yticks()))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator((ax.get_yticks()[1] - ax.get_yticks()[0]) / 2))
    
    #字体替换
    for m in range(len(xticks)):
        tick = xticks[m]
        text = tick.get_text()
        xtickLabel[m] = '$\\mathrm{'+text+'}$'
        
    for m in range(len(yticks)):
        tick = yticks[m]
        text = tick.get_text()
        try:        
            ytickLabel[m] = '$\\mathrm{'+text+'}$'
        except:
            ytickLabel[m] = text

    #更改坐标轴的tick标签
    ax.xaxis.set_major_locator(ticker.FixedLocator(ax.get_xticks()))
    ax.yaxis.set_major_locator(ticker.FixedLocator(ax.get_yticks()))

    ax.set_xticklabels(xtickLabel, fontsize = lenSize-2)
    ax.set_yticklabels(ytickLabel, fontsize = lenSize-2)
    
    ax.tick_params(axis='both', which='major', labelsize=lenSize,
           direction='in', length=4, width=2, pad=8)
    ax.tick_params(axis='both', which='minor', labelsize=lenSize-4,
           direction='in', length=3, width=1, pad=8)
     
    # 顶部和右侧轴标签     
    if axisTopRight:
        ax.tick_params(right=True)
        ax.tick_params(top=True)
    
    # 去掉顶部和右侧轴
    if axisTopRight==False:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
    if gridOff==False:
        ax.grid(which='major', linestyle=':', linewidth='0.5', color='gray') 
        ax.grid(which='minor', linestyle=':', linewidth='0.5', color='gray') 
        #ax.minorticks_on()
        
    if legendOff==False:
        #显示legend
        legend = ax.legend()

        #显示图例，并使用 bbox_to_anchor 根据坐标设置图例位置
        #legend = ax.legend(loc='upper left', bbox_to_anchor=(legenPos[0], legenPos[1]))
        
        if gridOff:
            legend.get_frame().set_facecolor('none')
            legend.get_frame().set_edgecolor('none')
    
    #添加轴标题
    ax.set_xlabel(xyLabel[0], fontsize = lenSize-2)
    ax.set_ylabel(xyLabel[1], fontsize = lenSize-2)
    #plt.tight_layout()
        
#########################################
## save figure, tight layout, 
## set background color
#########################################
def savefig(name, fig, ax):
    fig.patch.set_facecolor(cls(0))
    ax.set_facecolor(cls(0))
    plt.savefig(name, bbox_inches='tight')
    plt.close()    

#########################################
## 2D stream plot
#########################################  
def streamPlot(ax, x, y, ux, uz, Range):
    x2, y2, ux1 = dataReflect(x, y, ux)
    x3, y3, uz1 = dataReflect(x, y, uz)
    xi = np.linspace(Range[0], Range[1], 400)
    yi = np.linspace(Range[2], Range[3], 400)
    [X, Y] = np.meshgrid(xi, yi)
    U = griddata((x2,y2), ux1, (X, Y), method='linear')
    W = griddata((x3,y3), uz1, (X, Y), method='linear')
    ax.quiver(X, Y, U, W)

#########################################
## 2D contour plot
#########################################
def contourPlot(fig, ax, x1, y1, Range, data, level=15, direction='vertical', 
                skip=1, lenSize=12, legendLabels='value', 
                emphaseizeLine=False, 
                lineValue=0,
                linecolor='white',
                linewidth=3,
                method='linear'
    ):
    xi = np.linspace(Range[0], Range[1], 400)
    yi = np.linspace(Range[2], Range[3], 400)
    [X, Y] = np.meshgrid(xi, yi)
    V = griddata((x1,y1), data, (X, Y), method=method)
    #levels = range(0,15,1) 
    im=ax.contourf(X,Y,V,level,cmap=matplotlib.cm.jet)
    isoline=ax.contour(X,Y,V,level, linewidths=0.1)
    cBar = fig.colorbar(im, orientation=direction) 
    
    # if you want to emphasize a specific contour line
    if emphaseizeLine:
        highlighted_contour = ax.contour(X, Y, V, levels=[lineValue], colors=linecolor, linewidths=linewidth, linestyles=ls(1))
    
    legendLabel=[]
    kk=0
    le=[]
    for n in range(len(level)):
        if kk==0 or kk==skip:
            formatted_number = "{:.2f}".format(level[n])
            legendLabel.append('$\\mathrm{'+formatted_number+'}$')
            le.append(level[n])
            if kk==skip:
                kk=1
            else:
                kk=kk+1
        elif kk<skip and kk>0:
            kk=kk+1
            continue           
    cBar.set_ticks(ticks=le, labels=legendLabel)
    cBar.set_label(label=legendLabels, size=lenSize-2)
    cBar.ax.tick_params(labelsize=lenSize-2)
    #cBar.ax.set_yticklabels(legendLabel)    
    return im  
    
#########################################
## 2D isoline plot
#########################################
def isolinePlot(fig, ax, x1, y1, Range, data, level, 
                color, fontSize, lineStyle, barOn, labels):
    xi = np.linspace(Range[0], Range[1], 400)
    yi = np.linspace(Range[2], Range[3], 400)
    [X, Y] = np.meshgrid(xi, yi)
    V = griddata((x1,y1), data, (X, Y), method='linear')
    CS = ax.contour(X,Y,V,level,linewidths=1.75, linestyles=lineStyle,
        colors=color,
        )
    
    if barOn==True:
        CB = fig.colorbar(CS, shrink=0.8, label=labels)
        l, b, w, h = ax.get_position().bounds
        ll, bb, ww, hh = CB.ax.get_position().bounds
        CB.ax.set_position([ll, b + 0.1*h, ww, h*0.8])
        
        legendLabel=[]
        for n in range(len(level)):
            legendLabel.append('$\\mathrm{'+repr(level[n])+'}$')
        CB.set_ticks(ticks=level, labels=legendLabel)
        CB.set_label(label=labels,size=fontSize-4)
        CB.ax.tick_params(labelsize=fontSize-4)
        CB.ax.set_yticklabels(legendLabel)

        Fonts = 'DejaVu Sans'
        config={
           "font.family":'serif',
           "font.size":fontSize-4,
           "text.usetex": True,
           "mathtext.fontset":'stix',
           "font.serif":[Fonts],
        }
        rcParams.update(config)        
        #im=ax.contourf(X,Y,V,19,cmap=reverse_map)
        #cBar = fig.colorbar(im, orientation='horizontal') 
        #cBar.set_label(legendLabel)   

def save(figureName, plt):
  plt.tight_layout()
  plt.savefig(figureName+'.png')
  plt.savefig(figureName+'.svg')
  svg_to_emf(figureName)
  plt.close()
