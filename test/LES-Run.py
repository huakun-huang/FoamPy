import foam as of
import preProcessing as pr
import boundary as bd
import report as rp
import turbulenceEva as trE

def cleanCase():
    of.cleanCase(meshClean=True)
    of.runLinux('rm -rf 0/yPlus')
    of.runLinux('rm -rf 0/C*')
    of.runLinux('rm -rf constant/polyMesh')

def runCase():
    
    ### 运行前处理，清楚所有数据
    #cleanCase()
    
    ###############################################################
    ### 入口湍流条件定义 ####
    ######
    Lt = 0.04
    Ubar = 8.9
    TKE, omega, Re = trE.inlet(velocity=Ubar, Tu=4.5, Lc=Lt)
    
    ###############################################################
    ### 设置边界条件 ####
    ######
    bd.changeBdrValue(bfile='0/U', targetBdr='IN', targetLineNum=2, 
                      targetWordNum=0, targetWord='TKE', 
                      targetValueNum=1, replaceString=repr(TKE)+';')
    bd.changeBdrValue(bfile='0/U', targetBdr='IN', targetLineNum=2, 
                      targetWordNum=0, targetWord='Lt', 
                      targetValueNum=1, replaceString=repr(Lt)+';')
    bd.changeBdrValue(bfile='0/U', targetBdr='IN', targetLineNum=2, 
                      targetWordNum=0, targetWord='Ubar', 
                      targetValueNum=1, replaceString=repr(Ubar)+';')
    bd.changeBdrValue(bfile='0/U', targetBdr='IN', targetLineNum=2, 
                      targetWordNum=0, targetWord='delta', 
                      targetValueNum=1, replaceString=repr(1e-7)+';')
    
    """
    ### 设置边界k ####
    bd.changeBdrValue(bfile='0/k', targetBdr='IN', targetLineNum=3, 
                      targetWordNum=0, targetWord='value', 
                      targetValueNum=2, replaceString=repr(TKE)+';')
    """

    ### 划分网格
    #of.runFoam('blockMesh')
    of.runFoam('decomposePar -force')

    ### 设置求解器和迭代步数
    bd.changeControlDictValue(targetWord='application', replaceString='buoyantBoussinesqPimpleFoam;')
    bd.changeControlDictValue(targetWord='startFrom', replaceString='latestTime;')
    bd.changeControlDictValue(targetWord='endTime', replaceString='0.01;')
    bd.changeControlDictValue(targetWord='purgeWrite', replaceString='2;')
    bd.changeControlDictValue(targetWord='adjustTimeStep', replaceString='no;')
    bd.changeControlDictValue(targetWord='writeInterval', replaceString='5e-5;')
    bd.changeControlDictValue(targetWord='deltaT', replaceString='1e-7;')
    bd.changeControlDictValue(targetWord='maxCo', replaceString='0.5;') 
    
    
    
    
    
    ###############################################################
    #### 设置离散格式
    #### 一阶迎风：upwind； 二阶迎风：linearUpwind grad; 
    #### 中心格式：linear;  二阶混合: LUST grad;
    ###############################################################
    pr.changeDivSchemes(div='U', scheme='upwind', bounded=True)
    
    ###############################################################
    ### 并行运行                                                   
    ### 设置并行数                                                 
    ###############################################################
    pro = 90
    pr.setDecomposePar(pro = pro)
    of.runParallel(log=False)
    
    bd.changeControlDictValue(targetWord='endTime', replaceString='0.08;')
    pr.changeDivSchemes(div='U', scheme='linear', bounded=True)
    of.runParallel(log=False)
    of.runApplication('reconstructPar -latestTime')
    
    ###############################################################

def post():
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
    
    #of.runLinux('(cd validation && python plot.py)')

runCase()
#post()
