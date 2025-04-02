import foam as of
import os
import figurePlot as ft
import getValueFromFile as gv
import matplotlib.pyplot as plt

################### define a line ########################
def sampleLine(file='line', start='(0 0 0)', end='(0 0 0)', field='U'):
  with open('./system/line','w') as f:
    f.write("/*--------------------------------*- C++ -*----------------------------------*\\\n")
    f.write("  =========                 |\n")
    f.write("  \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox\n")
    f.write("   \\\\    /   O peration     |\n")
    f.write("    \\\\  /    A nd           | Web:      www.OpenFOAM.org\n")
    f.write("     \\\\/     M anipulation  |\n")
    f.write("-------------------------------------------------------------------------------\n")
    f.write("Description\n")
    f.write("    Writes graph data for specified fields along a line, specified by start\n")
    f.write("    and end points.\n")
    f.write("\n")
    f.write("\\*---------------------------------------------------------------------------*/\n")
    f.write("\n")
    f.write("start   "+start+";\n")
    f.write("end     "+end+";\n")
    f.write("fields  ("+field+");\n")
    f.write("\n")
    f.write("// Sampling and I/O settings\n")
    f.write("#includeEtc \"caseDicts/postProcessing/graphs/sampleDict.cfg\"\n")
    f.write("\n")
    f.write("// Override settings here, e.g.\n")
    f.write("// setConfig { type midPoint; }\n")
    f.write("\n")
    f.write("// Must be last entry\n")
    f.write("#includeEtc \"caseDicts/postProcessing/graphs/graph.cfg\"\n")
  f.close()

def grad(file='line', field='T'):
  with open('./system/'+file, 'w') as f:
    f.write("/*--------------------------------*- C++ -*----------------------------------*\\\n")
    f.write("| =========                 |                                                 |\n")
    f.write("| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n")
    f.write("|  \\    /   O peration     | Version:  10                                  |\n")
    f.write("|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |\n")
    f.write("|    \\/     M anipulation  |                                                 |\n")
    f.write("\\*---------------------------------------------------------------------------*/\n")
    f.write("FoamFile\n")
    f.write("{\n")
    f.write("    version	   2.0;\n")
    f.write("    format	   ascii;\n")
    f.write("    class	   dictionary;\n")
    f.write("    location	  \"system/\";\n")
    f.write("    object	   gradT;\n")
    f.write("}\n")
    f.write("//    author      Huakun Huang\n")
    f.write("//    Email:      huanghuakun0902@163.com\n")
    f.write("// ************************************************************************* //\n")
    f.write("type            grad;\n")
    f.write("libs            (\"libfieldFunctionObjects.so\");\n")
    f.write("\n")
    f.write("field           "+field+";\n")
    f.write("\n")
    f.write("executeControl  writeTime;\n")
    f.write("writeControl    writeTime;\n")
    f.write("\n")
    f.write("// ************************************************************************* //\n")
  f.close()

############################ get filed minMax ###############################
def minMax(field):
  # check the field
  latestTime = of.getLatestTime()
  fields = './'+latestTime+'/'+field
  if not os.path.exists(fields):
      return 0
  with open('system/minMax'+field, 'w') as f:
    f.write("/*--------------------------------*- C++ -*----------------------------------*\\\n")
    f.write("  =========                 |\n")
    f.write("  \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox\n")
    f.write("   \\\\    /   O peration     | Version:  v2312\n")
    f.write("    \\\\  /    A nd           | Website:  www.openfoam.com\n")
    f.write("     \\\\/     M anipulation  |\n")
    f.write("-------------------------------------------------------------------------------\n")
    f.write("Description\n")
    f.write("    Writes out the minimum and maximum values, by magnitude for non-scalar\n")
    f.write("    fields, and the locations where they occur.\n")
    f.write("\n")
    f.write("\\*---------------------------------------------------------------------------*/\n")
    f.write("\n")
    f.write("#includeEtc \"caseDicts/postProcessing/minMax/fieldMinMax.cfg\"\n")
    f.write("\n")
    f.write("fields ("+field+");\n")
    f.write("\n")
    f.write("// ************************************************************************* //\n")
  f.close()
  cmd = 'postProcess -func minMax'+field+' >log.'+'minMax'+field+' 2>&1'
  of.runFoam(cmd)
  return 1

def CoNum(path='log.txt'):
    app = of.getValue('./system/controlDict', 'application')
    if app=='rhoCentralFoam':
        times, value = gv.getValueFloat(path, target='Courant', targetLineNum=8, targetNum=3, returnNum=7)
    else:
        return '0'
    fig, ax = plt.subplots(1, figsize=(8, 5), dpi=600)
    xyRange = [min(times), max(times), min(value), max(value)]
    xyLabel = ['$\\mathrm{Time \\ [s]}$', '$\\mathrm{\\it C_u }$'] 
    ax.plot(times, value, linewidth=3, color=ft.cls(2), label='$\\mathrm{\\it C_u }$')
    ft.plot(ax, plt, xyRange, xyLabel=xyLabel, lenSize=20, axisTopRight=True, gridOff=False) 
    ft.savefig('Cu.png', ax, fig)
    plt.close()

def Residual(valueList, file_path):
    datas = gv.read_log_file(file_path, valueList)
    fig, ax = plt.subplots(1, figsize=(8, 5), dpi=600)
    minValue=23
    maxValue=0
    valuesL=[]
    for n in range(len(valueList)):
        #data = gv.limit_data_length(data)
        timestamps, values = zip(*datas[n])
        valuesL.append(values)
        minV = min(values)
        maxV = max(values)
        if minValue > minV:
            minValue = minV
        if maxValue < maxV:
            maxValue = maxV
        labels = '$\\mathrm{ \\it '+valueList[n]+' }$'
        ax.plot(timestamps, values, color=ft.cls(n+1), linewidth=1.75, label=labels)
    
    xyRange = [min(timestamps)-0.00001, max(timestamps), minValue, maxValue]
    xyLabel = ['$\\mathrm{Time}$', '$\\mathrm{Residual}$'] 
    plt.yscale('log')
    plt.legend()
    ax.set_xlabel('Iteration')  
    ax.set_ylabel('Residual')     
    #ft.plot(ax, plt, xyRange, xyLabel=xyLabel, lenSize=16, axisTopRight=True, gridOff=True, yLog=True) 
    plt.savefig('resdiual.png', bbox_inches='tight')
    with open('residual.txt', 'w') as f:
        for kn in range(len(timestamps)):
            f.write(repr(timestamps[kn])+'\t')
            for mn in range(len(valueList)):
                f.write(repr(valuesL[mn][kn])+'\t')
            f.write('\n')
    f.close()
    plt.close()    

