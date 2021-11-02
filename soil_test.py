# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 09:47:43 2021

@author: Chia-Wei Wang
"""

import os
import numpy as np
import pandas as pd

## 找到所有的檔名 ###
# 取得名稱
L = os.listdir(r'C:\Users\acer\Desktop\soil test\Soil')
# 建立要複製的檔名
L1 = []
filepath = []
for i in range(0,547):
    a = L[i]+'.soi'
    L1.append(a)
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
        b = 'Error'
    elif b < 18:
        b = 'Lack'
    else:
        b = 'OK'
    stay.append(b)


### 將資料串聯 ###
name = ['filename','data length','stay']
data = np.array([L1,length,stay])
data = data.T
df = pd.DataFrame(data,columns=name)
df.to_csv(r'C:\Users\acer\Desktop\soil test\土壤物理化學分析數據_測試結果.csv')

