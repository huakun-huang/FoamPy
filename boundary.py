import shutil, glob
import os
import foam as of

######################## change a boundary value ################
def changeBdrValue(bfile='0/p', targetBdr='INLET', targetLineNum=3, targetWordNum=0, targetWord='p0', targetValueNum=2, replaceString='2'):
    with open(bfile, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    find = 0
    for m in range(len(lines)):
        line = lines[m]
        parts = line.strip().split()
        if len(parts)==1:
            if parts[0] == targetBdr:
                find = 1
        if len(parts)== targetLineNum and find==1:
            if parts[targetWordNum]==targetWord:
                lines[m] = lines[m].replace(parts[targetValueNum], replaceString)
                break
    file.close()
    with open(bfile, 'w', encoding='utf-8') as file:
        file.writelines(lines)
    file.close()
                
######################## change a boundary value ################
def changeControlDictValue(bfile='./system/controlDict', targetWord='endTime', targetLineNum=2, targetWordNum=0, targetValueNum=1, replaceString='2'):
    with open(bfile, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    for m in range(len(lines)):
        line = lines[m]
        parts = line.strip().split()
        if len(parts)== targetLineNum:
            if parts[targetWordNum]==targetWord:
                lines[m] = lines[m].replace(parts[targetValueNum], replaceString)
                break
    file.close()
    with open(bfile, 'w', encoding='utf-8') as file:
        file.writelines(lines)
    file.close()

######################## change a boundary value ################
def changeInternalValue(bfile='./0/U', targetWord='endTime', targetLineNum=2, targetWordNum=0, targetValueNum=1, replaceString='2'):
    with open(bfile, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    for m in range(len(lines)):
        line = lines[m]
        parts = line.strip().split()
        if len(parts)== targetLineNum:
            if parts[targetWordNum]==targetWord:
                lines[m] = lines[m].replace(parts[targetValueNum], replaceString)
                break
    file.close()
    with open(bfile, 'w', encoding='utf-8') as file:
        file.writelines(lines)
    file.close()    

######################## read basic boundary type ################
def readBasic():
    path = 'constant/polyMesh/boundary'
    bdn=[]
    type=[]
    with open(path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 1:
                if  parts[0] =='FoamFile':
                    continue
                else:
                    try:
                        if float(parts[0])>0:
                            continue
                    except:
                        bdn.append(parts[0])
            elif len(parts)==2:
                types, name = parts
                if types == 'type':
                    name = name[:-1]
                    type.append(name)
                
    file.close()
    bdn = [s for s in bdn if 1 < len(s) <=40]
    return bdn, type
    
##################### read setting boundary ###################
def boundaryType(files, bdr_):
    k = 0
    bdrName='0'
    with open(files, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts)==1:
                if parts[0]==bdr_:
                    k = 1
                #print(parts[0], bdr_, k, files)
            if len(parts)==2 and k==1:
                type, name = parts
                if parts[0] == 'type' or parts[0]=='#include':
                    if parts[0]=='#include':
                        bdrName = name
                    else:
                        bdrName = name[:-1]
                    break
    file.close()
    num = k
    return num, bdrName
                    
def readBoundary(bdn):
    folder_path = './0'

    all_entries = os.listdir(folder_path)
    
    file_names = [f for f in all_entries if os.path.isfile(os.path.join(folder_path, f))]
    
    type=[]
    
    #current application
    app = of.getValue('system/controlDict', 'application')
    
    for file_name in file_names:
        bdr=[]
        name = bdn
        k, types = boundaryType('0/'+file_name, name)
        appropriate = '1'
        if k==0:
            continue
        else:
            if app == 'rhoCentralFoam':
                if types == 'fixedFluxPressure':
                    appropriate == '0'
            bdr.append(file_name)
            bdr.append(types)
            bdr.append(appropriate)
            type.append(bdr)
    return type
    