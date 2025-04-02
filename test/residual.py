import sys, os
sys.path.append('/mnt/d/Codes/others/FoamPy')
import matplotlib.pyplot as plt
import figurePlot as ft
import foam as of
import foamPost as fp

def residual():
    file_path = 'log.rhoSimpleFoam'
    sampleParas =['Ux', 'Uy', 'k', 'omega']
    fp.Residual(sampleParas, file_path)

residual()