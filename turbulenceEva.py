# -*- coding: UTF-8 -*-
import math as mt

################## 评估入口湍流特性 ##################
"""
### k, omega数值大小： k-w系列
##  Numerical Study of Plane and Round Impinging 
    Jets using RANS Models, 2008
### Retheta数值大小：SSTLM系列
##  Correlation-Based Transition Modeling for 
    Unstructured Parallelized Computational 
    Fluid Dynamics Codes, 2009
"""
###################################################
def inlet(velocity=7.9, Tu=2.5, Lc=0.04):
    #calculate turbulence kinetic energy k
    if Tu<3:
       k = (velocity*Tu*0.01)**2
    else:
       k = 1.5*(velocity*Tu*0.01)**2 

    #calculate the specific dissipation rate
    omega = mt.sqrt(k)/(0.015*Lc*0.09**0.25)

    #calculate the ReThetat
    Re=0
    if Tu>1.3:
        Re = 331.50*(Tu-0.5658)**(-0.571)*1

    else:
        Re = (1173.51-589.428*Tu+0.2196/(Tu**2))

    f = open('0/settings.H', 'w')

    #TKE
    f.write('//turbulence kinetic energy\n')
    str = 'TKE ' + repr(k) +';\n\n'
    f.write(str)

    #omega
    f.write('//the specific dissipation rate\n')
    str = 'w ' +repr(omega)+';\n\n'
    f.write(str)

    #Re
    f.write('//ReThetat\n')
    str = 'Re ' + repr(Re)+';\n\n'
    f.write(str)

    f.write('velocity '+repr(velocity)+';\n')
    f.close()
    return k, omega, Re