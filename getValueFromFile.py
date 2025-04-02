import os

# read log file for residual
def read_log_file(file_path, parasList):
    datas=[]
    for m in range(len(parasList)):
        datazt=[]
        datas.append(datazt)
    with open(file_path, 'r') as file:
        for line in file:
            # timestamp value
            parts = line.strip().split()
            if len(parts) == 3:
                timeName, eq, timestamp = parts
            if len(parts) > 4:
                for mn in range(len(parasList)):
                    if parts[3] == parasList[mn]+',':
                        value = parts[7]
                        value = value[:-1]
                        datas[mn].append((float(timestamp), float(value)))
    return datas
    
# limite data leng
def limit_data_length(data, max_length=40000): 
    if len(data) > max_length: 
        data = random.sample(data, max_length) 
    return data
    
################## get specific lines ##################
def getValue(files='.', target='0', targetLineNum=11, targetNum=0, returnNum=1):
    #file_path = 
    targetLine = 0
    targetString=[]
    times=[]
    with open(files, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) ==3:
                if parts[0] == 'Time' and parts[1]=='=':
                    times.append(parts[2])
            if len(parts)==targetLineNum:
                if parts[targetNum]==target:
                    targetString.append(parts[returnNum])
    file.close()
    return times, targetString

################## get specific value ##################
def getValueFloat(files='.', target='0', targetLineNum=11, targetNum=0, returnNum=1):
    #file_path = 
    targetLine = 0
    targetString=[]
    times=[]
    with open(files, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) ==3:
                if parts[0] == 'Time' and parts[1]=='=':
                    times.append(float(parts[2]))
            if len(parts)==targetLineNum:
                if parts[targetNum]==target:
                    targetString.append(float(parts[returnNum]))
    file.close()
    return times, targetString

################## get specific lines ##################    
def getValue2(file_path, target, num):
    #file_path = 
    app = '0'
    if not os.path.exists(file_path):
        return app
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == num:
                name, app = parts
                if name == target:
                    app = app[:-1]
                    break
    file.close()
    return app