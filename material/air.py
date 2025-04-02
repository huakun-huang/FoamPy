import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import sys, os
import matplotlib.pyplot as plt
import figurePlot as ft
import foam as of

def sutherland(T, As, Ts):
    return As*T**(3/2)/(Ts+T)

def conductivity(T):
    As = 1.458329648648463e-06
    Ts = 110.42339
    
    #dynamic viscosity
    mu = As*T**0.5/(1+Ts/T)
    
    #Cp
    coe = [3.4002706656000004, 
                   0.00048319574240000016, 
                   -1.0630119579e-06, 
                   2.4237248811000003e-09, 
                   -1.2502517023e-12, 
                   -1029.9390686000002, 
                   3.8889057833000003];
    #conductivity
    R = 287.06
    Cp = R*(coe[0]+coe[1]*T+coe[2]*T**2+coe[3]*T**3+coe[4]*T**4)
    Cv = Cp-R

    lambdas = mu*Cv*(1.32+1.77*R/Cv)
    return lambdas, Cp, Cv, mu

def LawAir(saveFile='SutherlandFit.pdf', temperature=298):
    #air in 101325Pa
    T=[175, 
    200, 
    240,
    300,
    350,
    400,
    450,
    500,
    550,
    600,
    700,
    800,
    900,
    1000,
    1200,
    1400,
    1700]

    mu=[11.84e-6,
    13.28e-6,
    15.46e-6,
    18.45e-6,
    20.74e-6,
    22.87e-6,
    24.85e-6,
    26.72e-6,
    28.49e-6,
    30.17e-6,
    33.32e-6,
    36.24e-6,
    38.96e-6,
    41.53e-6,
    46.26e-6,
    50.57e-6,
    56.47e-6]
    
    fig, ax = plt.subplots(1,figsize=(8,6.2), dpi=600)
    popt, pcov = curve_fit(sutherland, T, mu)
    As=popt[0]
    Ts=popt[1]
    #print('As = '+str(popt[0])+'\n')
    #print('Ts = '+str(popt[1])+'\n')

    xplot=np.linspace(200,2000,100)
    yplot=sutherland(xplot,As,Ts)
    
    y = sutherland(temperature, As, Ts)

    ax.plot(T, mu, 'o', markersize=9, markeredgecolor=ft.cls(1), markerfacecolor='none', label='$\\mathrm{NIST}$')
    ax.plot(xplot, yplot, '-', color=ft.cls(1), linewidth=3, label='$\\mathrm{Sutherland}$')
    ax.plot(temperature, y, 's', markerfacecolor='r', markeredgecolor='r', markersize=9, label='$\\mathrm{Estimation}$')
    
    xyRange = [160, 2000, 1e-5, 6e-5]
    xyLabel = ['$\\mathrm{Temperature \\ [K]}$', '$\\mathrm{Dynamic \\ Viscosity \\times 10^{-5} \\ (Pa.s) }$'] 
    legenPos = [0.03, 0]
    lenSize = 18
    ft.plot(ax, plt, xyRange, xyLabel, legenPos, lenSize)       
    ft.savefig(saveFile, fig, ax)
        
    