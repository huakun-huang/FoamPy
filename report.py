# -*- coding: UTF-8 -*-
import platform
import os, sys
import pwd

import air as mt_air
import boundary as bd
import foam as of
import foamPost as fp
import getValueFromFile as gv

##############get user name
def getUserName():
    system_name = platform.system()
    if system_name == 'Windows':
        try:
            username = os.getlogin()
        except OSError:
            username = os.environ.get('USERNAME')
    else:
        try:
            username = pwd.getpwuid(os.getuid()).pw_name
        except:
            username = 'Unknown-user'
    return username
   
############# get casename #######
def getCasename():
    current_path = os.getcwd()
    name = os.path.basename(current_path)
    return name

############# create report/main.tex #######
def main():
  folder_path = './report'
  os.makedirs(folder_path, exist_ok=True)
  os.makedirs('./report/sections', exist_ok=True)
  os.makedirs('./report/img', exist_ok=True)
  username = getUserName()
  casename = getCasename()
  with open('report/main.tex', 'w') as f:
    f.write("\\documentclass[a4paper, 12pt]{article}\n")
    f.write("\\usepackage{geometry}\n")
    f.write("\\geometry{left=2.5cm, right=2.5cm, top=2.5cm, bottom=2.5cm}\n")
    f.write("\\usepackage{setspace}\n")
    f.write("\\setstretch{1.5}\n")
    f.write("\\usepackage{fontspec}\n")
    f.write("\\setmainfont{Times New Roman}\n")
    f.write("\n")
    f.write("%Chinese character\n")
    f.write("\\usepackage{xeCJK}\n")
    f.write('\\usepackage{indentfirst}\n')
    f.write('\\setlength{\\parindent}{2em}\n')
    f.write("\n")
    f.write("%Section\n")
    f.write("\\usepackage{titlesec}\n")
    f.write("\\titleformat{\\section}{\\fontsize{13pt}{15pt}\\selectfont\\itshape}{\\thesection}{1em}{}\n")
    f.write("\\titlespacing*{\\section}{0pt}{*0}{*0}\n")
    f.write("%Subsection\n")
    f.write("\\titleformat{\\subsection}\n")
    f.write("{\\fontsize{13pt}{15pt}\\selectfont} % \n")
    f.write("{\\thesubsection}{1em}{} % \n")
    f.write("\\titlespacing*{\\subsection}\n")
    f.write("{0pt}{2pt}{0pt} %\n")
    f.write("%\n")
    f.write("\\titleformat{\\subsubsection}\n")
    f.write("{\\fontsize{13pt}{15pt}\\selectfont} % \n")
    f.write("{\\thesubsubsection}{1em}{} % \n")
    f.write("\\titlespacing*{\\subsubsection}\n")
    f.write("{0pt}{2pt}{0pt} %\n")
    f.write("\n")
    f.write("\\usepackage{authblk}\n")
    f.write("\\usepackage{footmisc}\n")
    f.write("\\usepackage{microtype}\n")
    f.write("\\usepackage[none]{hyphenat}\n")
    f.write("\n")
    f.write("%reference\n")
    f.write("\\usepackage[numbers]{natbib}\n")
    f.write("\\usepackage[colorlinks=true, linkcolor=blue, citecolor=blue, urlcolor=blue]{hyperref}\n")
    f.write("\\bibliographystyle{unsrt} \n")
    f.write("\n")
    f.write("%table\n")
    f.write("\\usepackage{booktabs}\n")
    f.write("\\usepackage{float}\n")
    f.write("\\usepackage{tabularx}\n")
    f.write("\\usepackage{array}\n")
    f.write("\\usepackage{longtable}\n")
    f.write("% user define space for table\n")
    f.write("\\newcolumntype{Y}{>{\\raggedright\\arraybackslash}X}\n")
    f.write("\n")
    f.write("%graphy\n")
    f.write("\\usepackage{graphicx}\n")
    f.write("\\usepackage{caption}\n")
    f.write("\\usepackage{subcaption}\n")
    f.write("% space\n")
    f.write("\\captionsetup{skip=2pt, justification=justified, font={small,singlespacing}, labelfont={bf}, textfont={normalsize}}\n")
    f.write("\n")
    f.write("% caption font\n")
    f.write("\\DeclareCaptionFont{custom}{\\fontsize{10.5pt}{12pt}\\selectfont}\n")
    f.write("\\captionsetup{font=custom}\n")
    f.write("\\usepackage{bm}\n")
    f.write("\n")
    f.write("\\title{\\textbf{\\textsf{OpenFOAM \\\\ "+casename+"数值计算报告}}}\n")
    f.write("\\date{\\today}\n")
    f.write("\\author{}\n")
    f.write("\n")
    f.write("% headers\n")
    f.write("\\usepackage{fancyhdr}\n")
    f.write("\\pagestyle{fancy}\n")
    f.write("\\lhead{OpenFOAM "+casename+"数值计算报告}\n")
    f.write("\\chead{}\n")
    f.write("\\rhead{}\n")
    f.write("\n")
    f.write("\\makeatletter\n")
    f.write("\\newcommand{\\maketitlepage}{%\n")
    f.write("	\\begin{titlepage}\n")
    f.write("		\\maketitle\n")
    f.write("		\\thispagestyle{empty}\n")
    f.write("		\\vfill \n")
    f.write("		\\centering\n")
    f.write("		Version: 1.1 \\\\\n")
    f.write("		此报告仅用于前期计算分析以及同行交流使用 \\\\\n")
    f.write("		"+username+" \\\\\n")
    f.write("		广东省湍流研究重点实验室，力学与航空航天，南方科技大学\n")
    f.write("		\\vfill \n")
    f.write("	\\end{titlepage}\n")
    f.write("	\\newpage\n")
    f.write("}\n")
    f.write("\\makeatother\n")
    f.write("\n")
    f.write("\\begin{document}\n")
    f.write("	\\maketitlepage\n")
    f.write("	\\include{sections/basic}\n")
    f.write("	\\input{sections/inlet}\n")
    f.write("	\\input{sections/grid}\n")
    f.write("\\end{document}\n")
  f.close()

################ create head ##################
def writeHead(f, cla='dictionary', location='constant', object='trans'):
  
    f.write("/*--------------------------------*- C++ -*----------------------------------*\\\n")
    f.write("| =========                 |                                                 |\n")
    f.write("| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n")
    f.write("|  \\    /   O peration     | Version:  2312                                  |\n")
    f.write("|   \\  /    A nd           | Web:      www.OpenFOAM.com                      |\n")
    f.write("|    \\/     M anipulation  |                                                 |\n")
    f.write("\\*---------------------------------------------------------------------------*/\n")
    f.write("FoamFile\n")
    f.write("{\n")
    f.write("    version	   2.0;\n")
    f.write("    format	   ascii;\n")
    f.write("    class	   "+cla+";\n")
    f.write("    location  \""+location+"\";\n")
    f.write("    object	   "+object+";\n")
    f.write("}\n")
    f.write("//    author      Huakun Huang\n")
    f.write("//    Email:      huanghuakun0902@163.com\n")
    f.write("// ************************************************************************* //\n")
  
def lookKeyword(files='./constant/g', keyword='gravity', prompt='gg'):
    #file_path =
    su = 0 
    with open(files, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                name, app = parts
                if name == keyword:
                    app = app[:-1]
                    su = 1
                    return app
                    break
    file.close()
    if su == 0:
        input_ = input(prompt)
        with open(files, 'a+') as f:
            f.write(keyword+' '+input_+';\n')
        f.close()
        return input_

def lookInit(files='./constant/g', keyword='gravity'):
    #file_path =
    su = 0 
    app = '0'
    with open(files, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                name, uniform, app = parts
                if name == keyword:
                    app = app[:-1]
                    su = 1
                    break
    file.close()
    if su == 0:
        print('not found value in ', files, 'for ', keyword)
    return app

def mindContent(text):
  return '\\textcolor{red}{\\textbf{'+text+'}}'

################ create basic.tex ##################
def basicFlow():
  files = './constant/transportProperties'
  if not os.path.exists(files):
      with open(files, 'w') as f:
          writeHead(f, cla='dictionary', location='constant', object='transportProperties')
      f.close()
  #look keywords
  flow = lookKeyword(files=files, keyword='mainFlow', prompt='流动介质：') 
  Uc = lookKeyword(files=files, keyword='Uc', prompt='特征速度Uc：')
  Lc = lookKeyword(files=files, keyword='Lc', prompt='特征长度Lc：') 
  Tc = lookKeyword(files=files, keyword='Tc', prompt='特征温度Tc：')  
  rhoc = lookKeyword(files=files, keyword='rhoc', prompt='参考密度rhoc：')
  pc = lookKeyword(files=files, keyword='pc', prompt='参考压力pc：') 
  nuc = lookKeyword(files=files, keyword='nuc', prompt='动力粘性系数nu_c：')
  Pr_l = lookKeyword(files=files, keyword='Pr_lc', prompt='层流普朗特数Pr_lc：')
  Pr_t = lookKeyword(files=files, keyword='Pr_tc', prompt='湍流普朗特数Pr_tc：')
  
  # Reynolds number
  Re = round(float(Uc)*float(Lc)/float(nuc), 2)
  
  if flow == 'air' or flow=='Air' or flow == '空气':
      # 理想气体状态方程
      if(float(pc)<0.01):
          pc = repr(float(pc)+101325)
      R = 287.06
      rho_idea = round(float(pc)/(R*float(Tc)), 4)
      rho_error = round((rho_idea-float(rhoc))/rho_idea *100, 2)
      #Cp, Cv, lambda
      lambdas, Cp, Cv, mu = mt_air.conductivity(float(Tc))
      nu = mu/rho_idea
      nu_error = round((nu-float(nuc))/nu, 2)
      Prl = round(Cp*mu/(lambdas), 2)
      Prl_error = round((Prl-float(Pr_l))/Prl, 2)
      
      mt_air.LawAir(saveFile='report/img/mu.pdf', temperature = float(Tc))
      mt_air.LawAir(saveFile='report/img/mu.pdf', temperature = float(Tc))
      
  
  with open('./report/sections/basic.tex', 'w') as f:
    f.write("\\section{流动基本信息}\n")
    f.write("% Please add the following required packages to your document preamble:\n")
    f.write("% \\usepackage{booktabs}\n")
    f.write("\\begin{table}[H]\n")
    f.write("	\\caption{流动信息对比}\n")
    f.write("	\\label{tab:flowInfo}\n")
    f.write("	\\begin{tabularx}{\\textwidth}{@{}lYlllY@{}}\n")
    f.write("		\\toprule\n")
    f.write("		类别&数值  &对比类别  &数值 &单位  &误差$\\%$  \\\\ \\midrule\n")
    f.write("		流动介质&"+flow+"  &  & &  &  \\\\ \n")
    f.write("		特征速度 $U_c$&"+Uc+"  & &  &m/s  &  \\\\\n")
    f.write("		特征长度$l_c$&"+Lc+"  & & &m  &  \\\\\n")
    f.write("		参考温度$T_c$&"+Tc+"  & & &K  &"+mindContent('[170-1700]')+"  \\\\\n")
    f.write("		参考压力$p_c$&"+pc+"  & & &Pa  &  \\\\\n")
    f.write("		参考密度$\\rho_c$&"+rhoc+"  &同状态理想气体密度 &"+repr(rho_idea)+" &$\\mathrm{kg/m^3}$  &"+mindContent(repr(rho_error))+"  \\\\\n")
    nus = "{:.2e}".format(nu)
    f.write("		运动粘性系数 $\\nu$&"+nuc+"  &NIST数据库 &"+nus+" &$\\mathrm{m^2/s^2}$  & "+mindContent(repr(nu_error))+" \\\\\n")
    f.write("		层流普朗特数$Pr_l$&"+Pr_l+"  & 理论公式计算值$\\frac{C_p \mu}{\lambda}$ &"+repr(Prl)+" & & "+mindContent(repr(Prl_error))+"\\\\\n")
    f.write("		湍流普朗特数$Pr_t$&"+Pr_t+"  &常规流体默认值  &0.85-0.9 & & "+mindContent('一致')+" \\\\ \\bottomrule\n")
    f.write("	\\end{tabularx}\n")
    f.write("\\end{table}\n")
    f.write("其中，$C_p$为定压比热容，大小为"+repr(round(Cp, 2))+"，$\\mu$为动力粘性系数，大小为$\\nu \\rho$，$\\lambda$表示导热系数，大小为"+repr(round(lambdas, 5))+"。图\\ref{fig:mu}显示了当前预测值与NIST数据库之间的吻合关系。此外，特征雷诺数由公式\\ref{eq:Re}得\n")
    f.write("\\begin{equation}\n")
    f.write("	Re=\\frac{U_cL_c}{\\nu}="+repr(Re)+" \\label{eq:Re}\n")
    f.write("\\end{equation}\n")
    f.write("    \\begin{figure}[H]\n")
    f.write("        \\centering\n")
    f.write("        \\includegraphics[width=0.6\\linewidth]{img/mu.pdf}\n")
    f.write("        \\caption{动力粘性系数$\\mu$对比}\n")
    f.write("        \\label{fig:mu}\n")
    f.write("    \\end{figure}\n")    
  f.close()

################ create inlet.tex ##################
def inletFlow():
  files = './constant/transportProperties'
  Tu = lookKeyword(files=files, keyword='Tu', prompt='入口湍流强度Tu：')
  Uc = lookKeyword(files=files, keyword='Uc', prompt='特征速度Uc：')
  Lc = lookKeyword(files=files, keyword='Lc', prompt='特征长度Lc：')
  with open('./report/sections/inlet.tex', 'w') as f:
    f.write("\\section{流动入口检查}\n")
    if float(Tu)>0.025:
        f.write("初始湍流强度$Tu$设为"+Tu+"，按照文献说明，此时认为入口流动为湍流状态，")
        k_in = 1.5*(float(Tu)*float(Uc))**2
        f.write("入口湍动能$k_{in}$以及比耗散率$\\omega_{in}$可按下式进行计算：\n")
        f.write("\\begin{equation}\n")
        f.write("	k_{in}=1.5(U_{in}\\times Tu)^2 = 1.5("+Uc+"\\times "+Tu+")^2="+repr(round(k_in, 5))+"  \\label{eq:k_in}\n")
        f.write("\\end{equation}\n")
    else:
        f.write("初始湍流强度$Tu$设为"+Tu+"，按照文献说明，此时认为入口流动为层流状态，")
        k_in = (float(Tu)*float(Uc))**2
        f.write("\\begin{equation}\n")
        f.write("	k_{in}=(U_{in}\\times Tu)^2 = ("+Uc+"\\times"+Tu+")^2="+repr(round(k_in, 5))+"  \\label{eq:k_in}\n")
        f.write("\\end{equation}\n")
    
    omega_in = k_in**0.5/(0.015*float(Lc)*0.09**0.25)
    f.write("\\begin{equation}\n")
    f.write("	\\omega_{in}=\\sqrt{k_{in}}/(0.015L_c \\cdot 0.09^{0.25})="+repr(round(omega_in, 4))+" \\label{eq:omega_in}\n")
    f.write("\\end{equation}\n")
    #相对误差计算 
    kc = lookInit(files='./0/k', keyword='internalField')
    omegac = lookInit(files='./0/omega', keyword='internalField')
    try:
        er1 = (float(kc)-k_in)/k_in *100
        er2 = (float(omegac)-omega_in)/omega_in *100
    except:
        er1 = 100
        er2 = 100
    f.write("速度入口为平均速度入口，大小为"+Uc+"。检测湍动能$k$，比耗散率$\\omega$初始化值\n\n")
    f.write(mindContent("与上述估计值的相对误差分别为："+repr(round(er1, 2))+"$\\%$，"+repr(round(er2, 2))+"$\\%$ \n"))
  f.close()
 
# 读取log文件 
def read_log_file(file_path, length, targetNum, keywordNum, paras):
    with open(file_path, 'r') as file:
        for line in file:
            # 假设log文件中的数据格式为 "timestamp value"
            parts = line.strip().split()
            if len(parts) == length:
                if parts[keywordNum] == paras:
                    return parts[targetNum]
    return '0'

################### 壁面条件检查 ##########################
def wallCheck():
    bdn, type = bd.readBasic()
    wallExist = 0
    wallName=[]
    wallName1=[]
    data = []
    times = []
    for n in range(len(type)):
        if type[n] == 'wall':
            wallExist = 1
            wallName1.append(bdn[n])      
    
    app = of.getValue('system/controlDict', 'application')
    if wallExist:
        of.runFoam(app+' -postProcess -func yPlus > log.yPlus 2>&1')
        with open('log.yPlus', 'r') as file:
            for line in file:
                parts = line.strip().split()
                mini=[]
                if len(parts) ==3:
                    if parts[0] == 'Time' and parts[1]=='=':
                        times.append(parts[2])
                if(len(parts)==13):
                    if parts[2]=='y+':
                        wallName.append(parts[1])
                        mini.append(parts[6])
                        mini.append(parts[9])
                        mini.append(parts[12])
                        data.append(mini)
    file.close()
    of.runFoam('checkMesh > log.checkMesh 2>&1')
    cellNum = read_log_file('log.checkMesh', 2, 1, 0, 'cells:')
    with open('report/sections/grid.tex', 'w') as f:
        f.write('\\section{网格检查}\n')
        f.write('总网格单元数为'+cellNum+'，基本边界条件有以下类型：\n')
        f.write("\\begin{table}[H]\n")
        f.write("\\centering\n")
        f.write("\\caption{基本边界条件类型}\n")
        f.write("\\begin{tabularx}{\\textwidth}{@{}YY@{}}\n")
        f.write("\\toprule\n")
        f.write(" 边界名称&类型 \\\\ \\midrule\n")
            
        for mn in range(len(bdn)):
            f.write(bdn[mn].replace('_', '\\_')+"&"+type[mn]+" \\\\ \n")
        f.write("\\bottomrule\n")
        f.write("\\end{tabularx}\n")
        f.write("\\end{table}\n\n") 

        folder_path = './0'
        all_entries = os.listdir(folder_path)
        file_names = [f for f in all_entries if os.path.isfile(os.path.join(folder_path, f))]
        f.write('\n以下为详细边界条件设置\n')
        for mn in range(len(bdn)):
            f.write("\\begin{table}[H]\n")
            f.write("\\centering\n")
            f.write("\\caption{"+bdn[mn].replace('_', '\\_')+"边界条件设置}\n")
            f.write("\\begin{tabularx}{\\textwidth}{@{}")
            f.write("YY")
            f.write("@{}}\n")
            f.write("\\toprule\n")
            f.write(" 变量名称&边界条件类型")
            f.write("\\\\ \\midrule\n")
            typeBdr = bd.readBoundary(bdn[mn])
            for kn in range(len(typeBdr)):
                f.write(typeBdr[kn][0].replace('_', '\\_')+"&"+typeBdr[kn][1]+"\\\\ \n")
            f.write("\\bottomrule\n")
            f.write("\\end{tabularx}\n")
            f.write("\\end{table}\n\n")
                
        if wallExist:
            f.write("\\begin{table}[H]\n")
            f.write("\\centering\n")
            f.write("\\caption{不同壁面处$y^+$大小}\n")
            f.write("\\begin{tabularx}{\\textwidth}{@{}YYYYY@{}}\n")
            f.write("\\toprule\n")
            f.write(" 壁面名称&时间&最小值  & 最大值 &平均值  \\\\ \\midrule\n")
            timeSt=0
            for mn in range(len(wallName)):
                f.write(wallName[mn]+"&"+times[timeSt]+'&'+data[mn][0][:-1]+"&"+data[mn][1][:-1]+"&"+data[mn][2]+"  \\\\ \n")
                if len(wallName1)==1:
                    timeSt = timeSt+1
                elif mn==len(wallName1)-1:
                    timeSt = timeSt+1
            f.write("\\bottomrule\n")
            f.write("\\end{tabularx}\n")
            f.write("\\end{table}\n\n")                        
        else:
            f.write(mindContent('本算例中不存在壁面边界条件\n'))
            
        #flow check -- velocity field
        filesp = './constant/transportProperties'
        flow = lookKeyword(files=filesp, keyword='mainFlow', prompt='流动介质：')
        Uc = lookKeyword(files=filesp, keyword='Uc', prompt='特征速度Uc：')
        Tc = lookKeyword(files=filesp, keyword='Tc', prompt='特征温度Tc：')    
        f.write("\\section{求解器选择性检查}\n")
        f.write("本次计算的流动介质为"+flow+"，参考温度为"+Tc+" K，计算程序为"+app+"：\n")
        f.write("\\begin{equation}\n")
        markU = fp.minMax('U')
        if markU:
            timesU, maxU = gv.getValue(files='log.minMaxU', target='max(mag(U))', targetLineNum=11, targetNum=0, returnNum=2)
            f.write("U_{mag}^{max} ="+maxU[len(maxU)-1])
        markp = fp.minMax('p')
        if markp:
            timesp, maxp = gv.getValue(files='log.minMaxp', target='max(p)', targetLineNum=11, targetNum=0, returnNum=2)
            f.write(", p_{max}="+maxp[len(maxp)-1])
        markT = fp.minMax('T')
        if markT:
            timesT, maxT = gv.getValue(files='log.minMaxT', target='max(T)', targetLineNum=11, targetNum=0, returnNum=2)
            f.write(", T_{max}="+maxT[len(maxT)-1])
        f.write(' \\label{eq:maxValue}')
        f.write('\n')
        f.write("\\end{equation}\n")
        f.write("\\begin{equation}\n")
        if markU:
            timesU, minU = gv.getValue(files='log.minMaxU', target='min(mag(U))', targetLineNum=11, targetNum=0, returnNum=2)
            f.write("U_{mag}^{min} ="+minU[len(minU)-1])
        if markp:
            timesp, minp = gv.getValue(files='log.minMaxp', target='min(p)', targetLineNum=11, targetNum=0, returnNum=2)
            f.write(", p_{min}="+minp[len(minp)-1])
        if markT:
            timesT, minT = gv.getValue(files='log.minMaxT', target='min(T)', targetLineNum=11, targetNum=0, returnNum=2)
            f.write(", T_{min}="+minT[len(minT)-1])
        f.write(' \\label{eq:minValue}')
        f.write('\n')
        f.write("\\end{equation}\n")
        if markT:
            deltaT = float(maxT[len(maxT)-1]) - float(minT[len(minT)-1])  
            f.write('\n从式\\ref{eq:maxValue}和式\\ref{eq:minValue}可以发现，最大温差为'+repr(round(deltaT, 3))+'。\n')
            if deltaT>10 and app =='buoyantBoussinesqSimpleFoam' or app=='buoyantBoussinesqPimpleFoam':
                f.write(mindContent('温差过大，求解器不合适。\n'))
            tran = gv.getValue2('./constant/thermophysicalProperties', 'thermo', 2)
            if tran != '0':
                f.write('thermo模式为'+tran+'。\n')
                t2 = gv.getValue2('./constant/thermophysicalProperties', 'transport', 2)
                f.write('transport模式为'+t2+'。\n')
                t2 = gv.getValue2('./constant/thermophysicalProperties', 'equationOfState', 2)
                f.write('equationOfState模式为'+t2+'。\n')
                t2 = gv.getValue2('./constant/thermophysicalProperties', 'molWeight', 2)
                f.write('molWeight为'+t2+'。\n')
            else:
                f.write(mindContent('thermo模式为常数，计算过程采用不可压缩假设\n'))
    f.close()
    
    
        
