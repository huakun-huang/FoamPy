import foam as of
import preProcessing as pr
import boundary as bd
import report as rp

def runCase():
    ### 运行前处理，清楚所有数据
    of.cleanCase(meshClean=True)
    of.runLinux('rm -rf 0/yPlus')
    of.runLinux('rm -rf validation/*png')
    of.runLinux('rm -rf validation/*emf')
    of.runLinux('rm -rf constant/polyMesh')

    ### 划分网格
    of.runFoam('fluentMeshToFoam mesh/*msh')
    of.runFoam('decomposePar')

    ###
    ### 设置并行数
    pro = 6
    pr.setDecomposePar(pro = pro)

    ### 设置求解器和迭代步数
    bd.changeControlDictValue(targetWord='application', replaceString='buoyantBoussinesqSimpleFoam;')
    bd.changeControlDictValue(targetWord='endTime', replaceString='30000;')
    
    ###############################################################
    ### 设置湍流模型-kOmegaSSTCD
    pr.setRANSModel(model='kOmegaSSTCD')
    
    ### 设置beta1=0.06
    bd.changeBdrValue(bfile='./constant/turbulenceProperties',
                      targetLineNum=2,
                      targetWordNum=0,
                      targetWord='beta1',
                      targetValueNum=1,
                      replaceString='0.06;')
                      
    ### 设置beta2=0.0828
    bd.changeBdrValue(bfile='./constant/turbulenceProperties',
                      targetLineNum=2,
                      targetWordNum=0,
                      targetWord='beta2',
                      targetValueNum=1,
                      replaceString='0.0828;') 
    
    ### 设置beta0Star=0.09
    bd.changeBdrValue(bfile='./constant/turbulenceProperties',
                      targetLineNum=2,
                      targetWordNum=0,
                      targetWord='beta0Star',
                      targetValueNum=1,
                      replaceString='0.09;')

    ### 打开KatoLaunder
    bd.changeBdrValue(bfile='./constant/turbulenceProperties',
                      targetLineNum=2,
                      targetWordNum=0,
                      targetWord='KatoLaunder',
                      targetValueNum=1,
                      replaceString='yes;')
    
    ### 关闭VortexCorrect
    bd.changeBdrValue(bfile='./constant/turbulenceProperties',
                      targetLineNum=2,
                      targetWordNum=0,
                      targetWord='VortexCorrect',
                      targetValueNum=1,
                      replaceString='no;')    
    ###############################################################
    
    ### 并行运行
    of.runParallel()

def post():
    of.runApplication('reconstructPar -latestTime')
    of.runLinux('(cd validation && python plot.py)')
    of.checkYplus(log=False)
    
    ### 计算报告显示
    ### 生成主格式
    rp.main()
    
    ### 检查流动基本信息的正确性
    rp.basicFlow()
    
    ### 检查流动入口的正确性
    rp.inletFlow()
    
    ### 检查壁面及其他边界条件的设置正确性
    rp.wallCheck()

runCase()
post()