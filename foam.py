################################### in linux or windows ###################
import platform
import numpy as np

import time as t
import subprocess, os
import re
import shutil, glob
import threading


#######################system##############
def winOrLinux():
    plat = platform.system().lower()
    if plat == 'windows':
        return 1
    else:
        return 0
###########################################
def runFoam(cmd):
    source = 'source /home/hhk/OpenFOAM/OpenFOAM-v2312/etc/bashrc'
    run='0'
    win = winOrLinux()
    if win == 1:
        run = 'bash -c \"'+source+' && '+cmd+'\"'
    else:
        run = cmd
    os.system(run)

###########################################
def runLinux(cmd):
    run='0'
    win = winOrLinux()
    if win == 1:
        run = 'bash -c \"'+cmd+'\"'
    else:
        run = cmd
    os.system(run)

def inser(x0, y0, x1, y1, x):
    grad = (y0-y1)/(x0-x1)
    return (x-x0)*grad+y0

###########################################
def clean(folder):
    try:
       os.system('bash -c \"rm -r '+folder+' \" >log.clean 2>&1')
    except:
       print('delete '+folder)
       
#clean the case
def cleanCase(meshClean=True):
    clean('postProcessing')
    clean('proc*')
    for m in range(9):
        string = repr(m+1)+'*'
        clean(string)
    clean('log*')
    if meshClean:
        clean('constant/polyMesh')
    clean('dynamicCode')
    clean('0/Cx')
    clean('0/Cy')
    clean('0/Cz')
    clean('0/grad*')
    clean('0/yPlux')
    print('Clean the case')
    
###################getValue##############
#get application name
def getValue(file_path, target):
    #file_path = 
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                name, app = parts
                if name == target:
                    app = app[:-1]
                    break
    file.close()
    return app
    
###################run##############
def runParallel(log=True):
    print('Run decomposePar')
    runFoam('decomposePar >log.decomposePar 2>&1')
    app = getValue('system/controlDict', 'application')
    core = getValue('system/decomposeParDict', 'numberOfSubdomains')
    if log:
        cmd = 'mpirun -np '+core+' '+app+' -parallel >log.'+app+' 2>&1'
        print('Run '+cmd)
    else:
        cmd = 'mpirun -np '+core+' '+app+' -parallel'
    runFoam(cmd)

###################run single##############
def runSingleCore(log=True):
    app = getValue('system/controlDict', 'application')
    if log:
        cmd = app+' >log.'+app+' 2>&1'
        print('Run '+cmd)
    else:
        cmd = app
    runFoam(cmd)

###################run foam application##############
def runApplication(app, log=True):
    name = app.strip().split()
    if log:
        cmd = app+' >log.'+name[0]+' 2>&1'
        print('Run '+cmd)
    else:
        cmd = app
    runFoam(cmd)

#########################
def restore0():
    os.system('bash -c \"cp -rf 0.orig 0\"')

def runParallelCase(args, func):
    for case in range(len(args)):
       sub_thread = threading.Thread(target = func,
                                  args = (args[case],))     
       sub_thread.start()
                      
###########################################
      
def getLatestTime(path='.'):
    all_items = os.listdir(path)
    timesString=[]
    for strI in range(len(all_items)):
        try:
            value = float(all_items[strI])
        except:
            continue
        timesString.append(all_items[strI])
    numeric_folders = timesString
    
    latest=0
    index=0
    for nn in range(len(numeric_folders)):
        if float(numeric_folders[nn])>latest:
            latest = float(numeric_folders[nn])
            index = nn

    return numeric_folders[index]

def getTime(path='.'):
    all_items = os.listdir(path)
    timesString=[]
    for strI in range(len(all_items)):
        try:
            value = float(all_items[strI])
        except:
            continue
        timesString.append(all_items[strI])
    numeric_folders = timesString
    return numeric_folders

def checkYplus(log=True):
    app = getValue('./system/controlDict', 'application')
    if log:
        cmd = app+' -postProcess -func yPlus >log.yPlus 2>&1'
    else:
        cmd = app+' -postProcess -func yPlus'
    runFoam(cmd)







