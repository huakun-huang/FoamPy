import foam as of
import os
import sys
sys.path.append('.')
import results as rt
import boundary as bd

os.system('rm -rf *png')
os.system('rm -rf log.*')
of.runLinux('cp -rf 0.orig 0')
Pstep = ['4000;', '6000;', '8000;', '101325;']
Tstep = ['0.1;', '0.2;', '0.3;', '0.4;']

for mn in range(len(Pstep)):
    ### pressure step by step
    times = of.getLatestTime()
    bd.changeBdrValue(times+'/p', targetBdr='INLET', targetLineNum=3, targetWordNum=0, targetWord='p0', targetValueNum=2, replaceString=Pstep[mn])
    bd.changeControlDictValue(replaceString=Tstep[mn])
    of.runSingleCore()

of.runFoam('postProcess -func \"grad(U)\"')
of.runFoam('rhoCentralFoam -postProcess -func MachNo')
of.runFoam('postProcess -func center')
of.runFoam('postProcess -func surfaces')
rt.plotAll()
rt.plotAll()
#of.runParallel()