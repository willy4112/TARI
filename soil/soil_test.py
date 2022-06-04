# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 09:47:43 2021

@author: Chia-Wei Wang
"""

import os
import numpy as np
import pandas as pd
import re


## 找到所有的檔名 ###
# 取得名稱
L = os.listdir(r'C:\Users\acer\Desktop\soil test\Soil')
# 建立要複製的檔名
L1 = []
L2 = []
filepath = []
for i in range(0,547):
    a = L[i]+'.soi'
    c = L[i]
    # 取得編號
    d = re.findall(r'-?\d+\.?\d*', c)
    d = d[0]
    L1.append(a)
    L2.append(d)
    f1 = 'C:\\Users\\acer\\Desktop\\soil test\\Soil\\'
    f1 = f1+L[i]+'\\'+a
    filepath.append(f1)




### 計算文件長度 ###
length = []
stay = []
for j in range(0,547):
    filename = filepath[j]
    try:
        myfile = open(filename)
    except FileNotFoundError:
        pass
    lines = len(myfile.readlines())
    length.append(lines)
    b = length[j]
    if b <=0:
        b = 'Not done'
    elif b < 18:
        b = 'Data missing'
    else:
        b = 'OK'
    stay.append(b)


### 將資料串聯 ###
name = ['No','filename','data length','stay']
data = np.array([L2,L1,length,stay])
data = data.T
df = pd.DataFrame(data,columns=name)
# 檢查資料型態
# df.dtypes
# 轉換資料型態
df['No'] = df['No'].astype('int')
df['data length'] = df['data length'].astype('int')
df = df.sort_values(by='No',ascending=True)
df.reset_index(inplace=True)
df = df.drop(['index'],axis=1)
df.to_csv(r'C:\Users\acer\Desktop\soil test\土壤物理化學分析數據_測試結果.csv')

