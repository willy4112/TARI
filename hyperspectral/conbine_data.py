# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 11:55:19 2022

@author: CWW
"""

import glob
import numpy as np
import pandas as pd
import random

# 要處理的資料夾，包含析出後的兩台高光譜檔案
path = r'C:\Users\Thermo-IRMS\Desktop\hyperfine'

# 搜尋目標檔案，附檔名為csv
fileList = glob.glob(str(path+'\*\*.csv'))
nameList = []
# 取出檔案名
for i in fileList:
    Lis = i.split("\\")
    name = Lis[-1]
    nameList.append(name)

data = [nameList,fileList]
data = np.array(data)

had_read = []

for i in range(len(nameList)):
    for j in range(1,len(nameList)):
        if i+j > (len(nameList)-1):
            break
        # print(i,j,i+j)
        for a in had_read:
            if i+j == a :
                break
        if nameList[i] == nameList[i+j]:
            print([i,i+j],nameList[i],nameList[i+j])
            had_read.append(int(i+j))


            data1 = fileList[0]
            data2 = fileList[2]
            df1 = pd.read_csv(data1)
            df2 = pd.read_csv(data2)
            size1,a = df1.shape
            size2,a = df2.shape
            if size1 > size2:
                L = [i for i in range(size1)]
                L = random.sample(L,size2)
                df1 = df1.iloc[L,:]
                df1.reset_index(inplace = True)
                df1 = df1.drop('index',axis = 1)
                report = pd.merge(df1,df2)
                report.to_csv(nameList[i]+'.csv',header=True,index=False,encoding='utf-8-sig')
            else:
                L = [i for i in range(size2)]
                L = random.sample(L,size1)
                df2 = df2.iloc[L,:]
                df2.reset_index(inplace = True)
                df2 = df2.drop('index',axis = 1)
                report = pd.concat([df1,df2],axis = 1)
                report.to_csv(nameList[i]+'.csv',header=True,index=False,encoding='utf-8-sig')

