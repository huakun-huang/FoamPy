################################### for preProcessing ###################
import foam as of
import boundary as bd

################################### collapseDict ###################
def makeCollapseDict(mini=1e-7, maxMer=179):
  with open('./system/collapseDict', 'w') as f:
    f.write("/*--------------------------------*- C++ -*----------------------------------*\\\n")
    f.write("  =========                 |\n")
    f.write("  \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox\n")
    f.write("   \\\\    /   O peration     | Website:  https://openfoam.org\n")
    f.write("    \\\\  /    A nd           | Version:  7\n")
    f.write("     \\\\/     M anipulation  |\n")
    f.write("\\*---------------------------------------------------------------------------*/\n")
    f.write("FoamFile\n")
    f.write("{\n")
    f.write("    version         2;\n")
    f.write("    format          ascii;\n")
    f.write("    class           dictionary;\n")
    f.write("    location        \"system\";\n")
    f.write("    object          collapseDict;\n")
    f.write("}\n")
    f.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n")
    f.write("\n")
    f.write("// If on, after collapsing check the quality of the mesh. If bad faces are\n")
    f.write("// generated then redo the collapsing with stricter filtering.\n")
    f.write("\n")
    f.write("\n")
    f.write("collapseEdgesCoeffs\n")
    f.write("{\n")
    f.write("    // Edges shorter than this absolute value will be merged\n")
    f.write("    minimumEdgeLength   "+repr(mini)+";\n")
    f.write("\n")
    f.write("    // The maximum angle between two edges that share a point attached to\n")
    f.write("    // no other edges\n")
    f.write("    maximumMergeAngle   "+repr(maxMer)+";\n")
    f.write("}\n")
    f.write("\n")
    f.write("\n")
    f.write("// ************************************************************************* //\n")
  f.close()

################################### rotationDict ###################
def makeRotationDict(axis='(1 0 0)', originVector='(0 0 0)'):
  with open('./system/rotationDict', 'w') as f:
    f.write("/*--------------------------------*- C++ -*----------------------------------*\\\n")
    f.write("  =========                 |\n")
    f.write("  \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox\n")
    f.write("   \\\\    /   O peration     | Website:  https://openfoam.org\n")
    f.write("    \\\\  /    A nd           | Version:  7\n")
    f.write("     \\\\/     M anipulation  |\n")
    f.write("\\*---------------------------------------------------------------------------*/\n")
    f.write("FoamFile\n")
    f.write("{\n")
    f.write("    version         2;\n")
    f.write("    format          ascii;\n")
    f.write("    class           dictionary;\n")
    f.write("    location        \"system\";\n")
    f.write("    object          rotationDict;\n")
    f.write("}\n")
    f.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n")
    f.write("\n")
    f.write("makeAxialAxisPatch AXIS;\n")
    f.write("makeAxialWedgePatch frontAndBackPlanes;\n")
    f.write("\n")
    f.write("rotationVector "+axis+";\n")
    f.write("//originVector (0 0.15 0); //offset\n")
    f.write("originVector "+originVector+"; // origin\n")
    f.write("\n")
    f.write("// revolve option\n")
    f.write("// 0 = old and default mode, points are projected on wedges\n")
    f.write("// 1 = points are revolved\n")
    f.write("revolve 0;\n")
    f.write("\n")
    f.write("\n")
    f.write("// ************************************************************************* //\n")
  f.close()

def makeAxisMesh(mshPath='./fluent.msh', axis='(1 0 0)', originVector='(0 0 0)', scale=1.0, mini=1e-7, maxMer=179):
    if scale >1 or scale <1:
        of.runApplication('fluentMeshToFoam '+mshPath+' -scale '+ repr(scale))
    else:
        of.runApplication('fluentMeshToFoam '+mshPath)
    makeCollapseDict(mini=mini, maxMer=maxMer)
    makeRotationDict(axis=axis, originVector = originVector)
    of.runApplication('makeAxialMesh -overwrite')
    of.runApplication('collapseEdges -overwrite')
    print('Please check your mesh in constant/polyMesh/boundary')
        
####### set the decomposeParDict ###############
def setDecomposePar(pro=6):
  with open('./system/decomposeParDict', 'w') as f:
    f.write("/*--------------------------------*- C++ -*----------------------------------*\\\n")
    f.write("  =========                 |\n")
    f.write("  \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox\n")
    f.write("   \\\\    /   O peration     | Website:  https://openfoam.org\n")
    f.write("    \\\\  /    A nd           | Version:  7\n")
    f.write("     \\\\/     M anipulation  |\n")
    f.write("\\*---------------------------------------------------------------------------*/\n")
    f.write("FoamFile\n")
    f.write("{\n")
    f.write("    version         2;\n")
    f.write("    format          ascii;\n")
    f.write("    class           dictionary;\n")
    f.write("    location        \"system\";\n")
    f.write("    object          decomposePar;\n")
    f.write("}\n")
    f.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n")
    f.write("\n")
    f.write("// author      Huakun Huang\n")
    f.write("// Email:      huanghuakun0902@163.com.\n")
    f.write("\n")
    f.write("\n")
    f.write("// ************************************************************************* //\n")
    f.write("    numberOfSubdomains   "+repr(pro)+";\n")
    f.write("    method       scotch;\n")
    f.write("\n")
    f.write("// ************************************************************************* //\n")
  f.close()

def setRANSModel(model='kOmegaSST', printCoef=False):
  with open('./constant/turbulenceProperties', 'w') as f:
    f.write("/*--------------------------------*- C++ -*----------------------------------*\\\n")
    f.write("| =========                 |                                                 |\n")
    f.write("| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n")
    f.write("|  \\\\    /   O peration     | Version:  6                                     |\n")
    f.write("|   \\\\  /    A nd           | Web:      www.OpenFOAM.org                      |\n")
    f.write("|    \\\\/     M anipulation  |                                                 |\n")
    f.write("\\*---------------------------------------------------------------------------*/\n")
    f.write("FoamFile\n")
    f.write("{\n")
    f.write("    version     2.0;\n")
    f.write("    format      ascii;\n")
    f.write("    class       dictionary;\n")
    f.write("    location    \"constant\";\n")
    f.write("    object      turbulenceProperties;\n")
    f.write("}\n")
    f.write("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n")
    f.write("simulationType	RAS;\n")
    f.write("RAS\n")
    f.write("{\n")
    f.write("    RASModel        "+model+";\n")
    f.write("\n")
    f.write("    turbulence      on;\n")
    f.write("\n")
    f.write("    printCoeffs     on;\n")
    f.write("\n")
    if printCoef:
      f.write("     "+model+"Coeffs\n")
      f.write("     {\n")
      if model=='kOmegaSSTCD' or model=='kOmegaSSTCDLM' or model=='kOmegaSST' or model=='kOmegaSSTLM':
        f.write("             beta1             0.075;\n")
        f.write("             beta2             0.0828;\n")
        f.write("             betaStar          0.09;\n")
        f.write("             alphaOmega2       0.856;\n")
        f.write("             alphaOmega1       0.5;\n")
        f.write("             alphaK1           0.85;\n")
        f.write("             alphaK2           1;\n")
        f.write("             a1                0.31;\n")
        f.write("             b1                1;\n")
        f.write("             c1                10;\n")
        f.write("             F3                no;\n")
        if model == 'kOmegaSSTCD' or model=='kOmegaSSTCDLM':
            f.write("             f1                680;\n")
            f.write("             f2                80;\n")
            f.write("             beta0Star         0.09;\n")
            f.write("             KatoLaunder       yes;\n")
            f.write("             VortexCorrect     no;\n")            
        f.write("     }\n")
    f.write("}\n")
  f.close()
  
    
##### change turbulence constants    
def changeTurConstants(model='kOmegaSST', paraName='beta1', paraValue='0.075'):
    bd.changeBdrValue(bfile='./constant/turbulenceProperties',
                      targetBdr=model+'Coeffs',
                      targetLineNum=2,
                      targetWordNum=0,
                      targetWord=paraName,
                      targetValueNum=1,
                      replaceString=paraValue+';')
                      
def changeDivSchemes(div='U', scheme='upwind', bounded=False): 
    divName='0'
    divName='div(phi,'+div+')'
        
    with open('./system/fvSchemes', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    find = 0
    for m in range(len(lines)):
        line = lines[m]
        parts = line.strip().split()
        try:
          if parts[0]==divName and len(parts)>0:
            if bounded:
                lines[m] = '     '+divName+'    bounded Gauss '+ scheme+';\n'
            else:
                lines[m] = '     '+divName+'    Gauss '+ scheme+';\n'
            find = 1
            break
        except:
            print('check fvSchemes')
    
    if find == 0:
        target = 0
        for m in range(len(lines)):
           line = lines[m]
           parts = line.strip().split()
           if parts[0]=='divSchemes':
             target = m+2
             break
        if bounded:
            lines[target]='\n     '+divName+'  bounded  Guass '+scheme+';\n'
        else:
            lines[target]='\n     '+divName+'    Guass '+scheme+';\n'
    file.close() 
    with open('./system/fvSchemes', 'w', encoding='utf-8') as file:
            file.writelines(lines)
    file.close()         