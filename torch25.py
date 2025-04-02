# -*- coding: utf-8 -*-

import torch
import torchvision
import numpy as np
import torch.utils.data as Data
from torch.autograd import Variable
import torch.nn.functional as F
import random
import math as mt
import torch.optim.lr_scheduler as lr_scheduler
from torch import optim
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import StepLR
import shutil
from sklearn.preprocessing import StandardScaler

import sys, os

#Test GPU
def GPUTest():
    if torch.cuda.is_available():
        return 1
    else:
        return 0

#GPU information output
def GPUInfo():
    print("GPU 设备数量:", torch.cuda.device_count())
    for i in range(torch.cuda.device_count()):
        print(f"device {i} 名称: {torch.cuda.get_device_name(i)}")
        print(f"device {i} 计算能力: {torch.cuda.get_device_capability(i)}")
        print(f"device {i} 总内存: {torch.cuda.get_device_properties(i).total_memory / 1024**3:.2f} GB")

def get_all_directories(path='.'):
    # 获取当前目录中的所有文件和文件夹
    items = os.listdir(path)
    
    # 只保留文件夹
    directories = [item for item in items if os.path.isdir(os.path.join(path, item))]
    
    return directories

def loadDataFromFolder(folder, input_, output_, loop):
    print('handle in '+folder)
    input = np.loadtxt('../dataBase_v2_multil/'+folder+'/dataRANS/inputFeatures.txt')
    data = np.loadtxt('../dataBase_v2_multil/'+folder+'/dataRANS/ratio.txt')
    if loop == 0:
        input_ = input
        output_ = data
    else:
        input_ = arrayAppend(input_, input)
        output_ = arrayAppend(output_, data) 
    return input_, output_

def randomSaveData(input_, output_, folder, ratio=0.9):
    trainSampleRow = random.sample(range(0, input_.shape[0]-1), int(input_.shape[0]*ratio))
    trainSampleRow = sorted(trainSampleRow) 
    k = 0 
    testSample=[]
    for n in range(input_.shape[0]):
        if n!=trainSampleRow[k]:
            testSample.append(n)
        elif n== trainSampleRow[k]:
            k = k+1
            if k >= len(trainSampleRow):
                break 
                
    writeFile(folder+"/train.txt", input_, trainSampleRow)    
    writeFile(folder+"/trainRes.txt", output_, trainSampleRow)
      
    writeFile(folder+"/test.txt", input_, testSample)
    writeFile(folder+"/testRes.txt", output_, testSample) 
    
    test = np.loadtxt(folder+"/test.txt") 
    testRes = np.loadtxt(folder+"/testRes.txt")  
    train = np.loadtxt(folder+"/train.txt")   
    trainres = np.loadtxt(folder+"/trainRes.txt") 
    
    return train, trainres, test, testRes          

#load inputFeature and outputFeatures
def dataInput(newData):
    trainFolder = get_all_directories('../dataBase_v2_multil')
    input=[]
    if newData:
        trainNum = 0
        try:
            print('=============================================')
            print('try to read the existing data')
            print('this is for append data reading')
            print('if the data are new, stop this application')
            print('and delete all data file in dataRANS')
            print('=============================================')
            input_ = np.loadtxt("dataRANS/train.txt")
            data_ = np.loadtxt("dataRANS/trainRes.txt")
            test_ = np.loadtxt("dataRANS/test.txt")
            testRes_ = np.loadtxt("dataRANS/testRes.txt")
            
            shutil.copy('dataRANS/train.txt', 'dataRANS/oldData/train.txt')
            shutil.copy('dataRANS/trainRes.txt', 'dataRANS/oldData/trainRes.txt')
            shutil.copy('dataRANS/test.txt', 'dataRANS/oldData/ttest.txt')
            shutil.copy('dataRANS/testRes.txt', 'dataRANS/oldData/testRes.txt')
            trainCase = np.loadtxt('trainCases.txt')
            with open('trainCases.txt', 'a+') as f:
                for n in range(len(trainFolder)):
                    folder = trainFolder[n]
                    folderTrain = False
                    for m in range(len(trainCase)):
                        if folder == trainCase[m]:
                            folderTrain = True
                            break
                    if folderTrain:
                        continue
                    else:
                        print('handle in '+folder)
                        input = np.loadtxt('../dataBase_v2_multil/'+folder+'/dataRANS/inputFeatures.txt')
                        data = np.loadtxt('../dataBase_v2_multil/'+folder+'/dataRANS/ratio.txt')
                        train, trainRes, test, testRes = randomSaveData(input, data, 'dataRANS/dataAddition', 0.9)
                        input_ = arrayAppend(input_, train)
                        data_ = arrayAppend(data_, trainRes)
                        test_ = arrayAppend(test_, test)
                
        except:
            input_ = []
            data_ = []
            print('=============================================')
            print('try to read the new data')
            print('this is for a new model')
            print('=============================================')
            with open('trainCases.txt', 'w') as f:
                for n in range(len(trainFolder)):
                    folder = trainFolder[n]
                    f.write(folder+'\n')
                    input_, data_ = loadDataFromFolder(folder, input_, data_, n)
            f.close()
            input_, data_, test_, testRes_ = randomSaveData(input_, data_, 'dataRANS', 0.9)
    else:
        print('do not train the model')

# write file
def writeFile(fileName, input, rows):
    k=0
    with open(fileName, 'w') as f:
        for n in range(len(rows)):
            for m in range(input.shape[1]):
                f.write(repr(input[rows[n]][m])+'\t');
            f.write('\n');
    f.close()

def writeTest(fileName, input):
    with open(fileName, 'w') as f:
        for n in range(input.shape[0]):
            for m in range(input.shape[1]):
                f.write(repr(input[n][m])+'\t')
            f.write('\n')
    f.close() 

# append aaray
def arrayAppend(a, b):
    temp = np.vstack((a, b))
    return temp  

#### get data ##############################
def get_data(train_ds, valid_ds, bs):
    return(
        DataLoader(train_ds, batch_size=bs, shuffle=True),
        DataLoader(valid_ds, batch_size=bs * 2),
    )    
    

############### compute error ############################
def error(outputs, targets, error, runGPU=False, score=0):
    if runGPU:
        outputs = outputs.cpu().detach().numpy()
        targets = targets.cpu().numpy()
    else:
        outputs = outputs.detach().numpy()
        targets = targets.numpy()
    for n in range(outputs.shape[0]):
        for m in range(outputs.shape[1]):
            er = ((outputs[n][m]-targets[n][m])*(outputs[n][m]-targets[n][m]))**0.5/max(((targets[n][m])**2)**0.5, 1e-5)
            error.append(er)
            score = score + (outputs[n][m]-targets[n][m])*(outputs[n][m]-targets[n][m])
    return error, score

def accuracy(bestModel, valida_dl):
    score = 0
    out=1
    runGPU = GPUTest()
    for xb, yb in valida_dl:
        if runGPU:
            xb, yb = xb.cuda(), yb.cuda()
        pred = bestModel(xb)
        out = yb.shape[1]
        errors=[]
        errors, score =  error(pred, yb, errors, runGPU, score)
    testResponses = np.loadtxt("dataRANS/testRes.txt")        
    score = mt.sqrt(score/(testResponses.shape[0]*testResponses.shape[1]))
    writeError(errors)
    return score

############## write error ################################
def writeError(error):
    with open('error.txt', 'a+') as f:
        for n in range(len(error)):
            f.write(repr(error[n])+'\n')
    f.close() 

##################### data ####################    
def preprocess(x, y):
    #                   row cls
    return x.view(-1, 1, 1, x.shape[1]), y

################## wrapped ####################
class WrappedDataLoader:
    def __init__(self, dl, func):
        self.dl = dl
        self.func = func
        
    def __len__(self):
        return len(self.dl)
    
    def __iter__(self):
        batches = iter(self.dl)
        for b in batches:
            yield (self.func(*b))

def loadTrainingData(newData):
    if newData:
        dataInput(newData)

    trainFeatures =  np.loadtxt("dataRANS/train.txt")
    trainResponses = np.loadtxt("dataRANS/trainRes.txt") 
    
    #scaler = StandardScaler()
    #trainFeatures = scaler.fit_transform(trainFeatures)
    
    return trainFeatures, trainResponses
    
def loadTestData():
    testFeatures = np.loadtxt("dataRANS/test.txt")
    testResponses = np.loadtxt("dataRANS/testRes.txt")
    
    #scaler = StandardScaler()
    #trainFeatures = scaler.fit_transform(trainFeatures)
    
    return testFeatures, testResponses

# Pass an optimizer for training set
# https://blog.csdn.net/weixin_37993251/article/details/88916913
def loss_batch(model, loss_func, xb, yb, opt=None):
    runGPU = GPUTest()
    if runGPU:
        xb, yb = xb.cuda(), yb.cuda()
    pred = model(xb)
    loss = loss_func(pred, yb)
    if opt is not None:
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        opt.step()
        opt.zero_grad()
    """    
    else:
        errors=[]
        errors =  error(pred, yb, errors, runGPU)
        writeError(errors)
    """    
    return loss.item(), len(xb)

################## model save ################### 
def model_save(train_dl, model):
    for xb, yb in train_dl:
      xb1 = xb
      break
    runGPU = GPUTest()
    if runGPU:
        xb1 = xb.cpu().numpy()
        torch.save(model.state_dict(), 'hhk_PINNmodel.pth')
    else:
        torch.save(model.state_dict(), 'hhk_PINNmodel.pth')  

################## model load ###################    
def model_load(model): 
    runGPU = GPUTest()
    if runGPU:
        model = torch.nn.DataParallel(model)
        model.load_state_dict(torch.load('hhk_PINNmodel.pt'))
        
    else:
        model.load_state_dict(torch.load('hhk_PINNmodel.pth'))
    return model 

################## model load ###################    
def model_loadAgain(model): 
    #traced_script_module = torch.jit.load('hhk_PINNmodel.pt')
    #model.load_state_dict(traced_script_module.state_dict())
    runGPU = GPUTest()
    if runGPU:
        model.load_state_dict(torch.load('hhk_PINNmodel.pt'))
        model = torch.nn.DataParallel(model)
    else:
        model.load_state_dict(torch.load('hhk_PINNmodel.pt', map_location=torch.device('cpu')))
        model = torch.nn.DataParallel(model)
        #model.load_state_dict(torch.load('hhk_PINNmodel.pt'))
    return model   

#################### define a ResidualBlock for CNN ###################
class ResidualBlock(torch.nn.Module):
    def __init__(self, in_channels, out_channels, dropout_prob=0.2):
        super().__init__()
        self.conv1 = torch.nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1)
        self.bn1 = torch.nn.BatchNorm2d(out_channels)
        self.conv2 = torch.nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1)
        self.bn2 = torch.nn.BatchNorm2d(out_channels)
        self.dropout = torch.nn.Dropout2d(dropout_prob)  # 添加 Dropout
        self.shortcut = torch.nn.Sequential()
        if in_channels != out_channels:
            self.shortcut = torch.nn.Sequential(
                torch.nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1),
                torch.nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.dropout(out)  # 应用 Dropout
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        out = F.relu(out)
        return out

class ResidualBlockANN(torch.nn.Module):
    def __init__(self, in_features, out_features, pout):
        super(ResidualBlockANN, self).__init__()
        self.linear = torch.nn.Linear(in_features, out_features)
        self.relu = torch.nn.ReLU()
        self.dropout = torch.nn.Dropout(p=pout)
        self.shortcut = torch.nn.Sequential()
        if in_features != out_features:
            self.shortcut = torch.nn.Sequential(
                torch.nn.Linear(in_features, out_features)
            )

    def forward(self, x):
        out = self.linear(x)
        out = self.relu(out)
        out = self.dropout(out)
        out += self.shortcut(x)
        out = self.relu(out)
        return out    