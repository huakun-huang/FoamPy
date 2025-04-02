import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import sys, os
import matplotlib.pyplot as plt
import figurePlot as ft
import foam as of

def inquiry(T0, data, T):
    y=0
    for n in range(1, len(T)):
        if T0>=T[n-1] and T0<T[n]:
            grad =(data[n]-data[n-1])/ (T[n]-T[n-1])
            y = grad*(T0-T[n-1])+data[n-1]
            break
    return y
    
def fit(degree, x, y, ax, enlarge=1):
    coefficients = np.polyfit(x, y, degree)
    polynomial = np.poly1d(coefficients)
    x_fit = np.linspace(min(x), max(x), 100)
    y_fit = polynomial(x_fit)
    ax.plot(x_fit, y_fit, linewidth=3, color=ft.cls(2), label='$\\mathrm{polynomial}$')
    ax.plot(x, y, 's', markersize=3, markeredgecolor=ft.cls(1), markerfacecolor='none', label='$\\mathrm{NIST}$')
    print("Polynomial Formula:") 
    #print(polynomial)
    coefficients_sorted = polynomial.coef[::-1]
    format = [f"{coef:.5e}" for coef in coefficients_sorted*enlarge]
    string='('
    for m in range(len(format)):
        string = string+format[m]+' '
    string = string+')'
    print(string)
    return x_fit, y_fit, coefficients
    
    
def polynomial():
    dataO2 = np.loadtxt('O2.txt')
    dataN2 = np.loadtxt('N2.txt')
    #O2:0.21, N2-0.79
    T = dataO2[:,0]
    Cp = (dataO2[:,8]*0.21+dataN2[:,8]*0.79)/28.9
    lambdas = dataO2[:,12]*0.21+dataN2[:,12]*0.79
    mu = dataO2[:,11]*0.21+dataN2[:,11]*0.79
    rho = dataO2[:,2]*0.21+dataN2[:,2]*0.79
    
    fig, axs = plt.subplots(2,2, figsize=(8, 6), dpi=600)
    ax1 = axs[0][0]
    ax2 = axs[0][1]
    ax3 = axs[1][0]
    ax4 = axs[1][1]
    lenSize = 12
    #fit
    ############## Cp #################
    x_fit, y_fit, coefficients = fit(7, T, Cp, ax1, enlarge=1e3)
    xyRange = [100, 1000, min(Cp), max(Cp)]
    xyLabel = ['$\\mathrm{Temperature \\ [K]}$', '$\\mathrm{{\\it C_p} \\ (J/(gK)) }$'] 
    ft.plot(ax1, plt, xyRange, xyLabel=xyLabel, lenSize=lenSize, axisTopRight=True, gridOff=False)
    
    ############### mu ####################
    x_fit, y_fit, coefficients = fit(7, T, mu, ax2, enlarge=1e-6)
    xyRange = [100, 1000, min(mu), max(mu)]
    xyLabel = ['$\\mathrm{Temperature \\ [K]}$', '$\\mathrm{{\\it \\mu} \\ (uPa/s) }$'] 
    ft.plot(ax2, plt, xyRange, xyLabel=xyLabel, lenSize=lenSize, axisTopRight=True, gridOff=False)
    
    ############### lambda ####################
    x_fit, y_fit, coefficients = fit(7, T, lambdas, ax3)
    xyRange = [100, 1000, min(lambdas), max(lambdas)]
    xyLabel = ['$\\mathrm{Temperature \\ [K]}$', '$\\mathrm{{\\it \\lambda} \\ (W/(mK)) }$'] 
    ft.plot(ax3, plt, xyRange, xyLabel=xyLabel, lenSize=lenSize, axisTopRight=True, gridOff=False)
    
    ############### rho ####################
    x_fit, y_fit, coefficients = fit(7, T, rho, ax4)
    xyRange = [100, 1000, min(rho), max(rho)]
    xyLabel = ['$\\mathrm{Temperature \\ [K]}$', '$\\mathrm{{\\it \\rho} \\ (kg/(m^3)) }$'] 
    ft.plot(ax4, plt, xyRange, xyLabel=xyLabel, lenSize=lenSize, axisTopRight=True, gridOff=False)
    
    plt.savefig('air.pdf', bbox_inches='tight')
    plt.close()
    
    #空气摩尔质量 28.9 g/mol
    mu0 = inquiry(298, mu, T)
    rho0 = inquiry(298, rho, T)
    Cp0 = inquiry(298.00001, Cp, T)
    print(mu0, rho0, Cp0)

polynomial()
    
    