# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 11:03:04 2021

@author: WIN10
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import re

# In[]      將4區合併成通一個檔案

## 找到所有的檔名 ###
# 取得名稱
L = os.listdir(r'K:\TCCIP統計降尺度月資料_AR5\AR5_統計降尺度_月資料_北部_平均溫')
L1 = []
L2 = []
L3 = []
L4 = []
L5 = []
L6 = []
L7 = []

for i in range(0,136):
    [n1,n2,n3,n4,n5,n6,n7] = L[i].split('_')
    L1.append(n1)
    L2.append(n2)
    L3.append(n3)
    L4.append(n4)
    L5.append(n5)
    L6.append(n6)
    [n7,n8] = n7.split('.')
    L7.append(n7)

# name = ['type','model']
# data = np.array([L6,L7])
# data = data.T
# df1 = pd.DataFrame(data,columns=name)
# df1.to_csv(r'K:\TCCIP統計降尺度月資料_AR5\分析.csv')


key_1 = '最高溫'
for i in range(0,136):
    key_2 = L6[i]
    key_3 = L7[i]
    s = pd.read_csv(r'K:\TCCIP統計降尺度月資料_AR5\AR5_統計降尺度_月資料_北部_'+key_1+'\\'+'AR5_統計降尺度_月資料_北部_'+key_1+'_'+key_2+'_'+key_3+'.csv')
    n = pd.read_csv(r'K:\TCCIP統計降尺度月資料_AR5\AR5_統計降尺度_月資料_中部_'+key_1+'\\'+'AR5_統計降尺度_月資料_中部_'+key_1+'_'+key_2+'_'+key_3+'.csv')
    e = pd.read_csv(r'K:\TCCIP統計降尺度月資料_AR5\AR5_統計降尺度_月資料_南部_'+key_1+'\\'+'AR5_統計降尺度_月資料_南部_'+key_1+'_'+key_2+'_'+key_3+'.csv')
    c = pd.read_csv(r'K:\TCCIP統計降尺度月資料_AR5\AR5_統計降尺度_月資料_東部_'+key_1+'\\'+'AR5_統計降尺度_月資料_東部_'+key_1+'_'+key_2+'_'+key_3+'.csv')
    df = pd.concat([s,n,e,c])
    df.to_csv(r'K:\TCCIP統計降尺度月資料_AR5\AR5_統計降尺度_月資料_'+key_1+'\\'+'AR5_月資料_'+key_1+'_'+key_2+'_'+key_3+'.csv',header=True,index=False,encoding='utf-8-sig')


# In[]      繪製特定單點的摺線圖

## 找到所有的檔名 ###
# 取得名稱
# L = os.listdir(r'C:\Users\acer\Desktop\TCCIP統計降尺度月資料_AR5\AR5_統計降尺度_月資料_平均溫')
# L = os.listdir(r'C:\Users\acer\Desktop\TCCIP統計降尺度月資料_AR5\AR5_統計降尺度_月資料_降雨量')
# L = os.listdir(r'C:\Users\acer\Desktop\TCCIP統計降尺度月資料_AR5\AR5_統計降尺度_月資料_最低溫')
# L = os.listdir(r'C:\Users\acer\Desktop\TCCIP統計降尺度月資料_AR5\AR5_統計降尺度_月資料_最高溫')

# 匯入經特別篩選過經緯度的數據

df1 = pd.read_csv(r'C:\Users\acer\Desktop\TCCIP統計降尺度月資料_AR5\降雨量_rcp26_bcc-csm1-1.csv')
df2 = df1.T

# 選擇繪製的區域點
# 0 = Xinyuan, 1 = Chishan
area = 0
# 讀取資料
month = []
for i in range(3,1143,12):
    [v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12] = [df2.iloc[i,area],df2.iloc[i+1,area],df2.iloc[i+2,area],df2.iloc[i+3,area],df2.iloc[i+4,area],df2.iloc[i+5,area],df2.iloc[i+6,area],df2.iloc[i+7,area],df2.iloc[i+8,area],df2.iloc[i+9,area],df2.iloc[i+10,area],df2.iloc[i+11,area]]
    month.append([v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12])

data = np.array(month)
# data = data.T

year = []
for j in range(2006,2101):
    year.append(j)
report = pd.DataFrame(data,index = year)
report = report.round(2)

# 選擇要繪製的年份，注意單位
plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.figure(dpi=800)
# g1 = report.loc[2010].plot(kind='line',legend = True, xticks = range(0,12))
# g1 = report.loc[2020].plot(kind='line',legend = True, xticks = range(0,12))
g1 = report.loc[2030].plot(kind='line',legend = True, xticks = range(0,12))
g1 = report.loc[2040].plot(kind='line',legend = True, xticks = range(0,12))
g1 = report.loc[2050].plot(kind='line',legend = True, xticks = range(0,12))
plt.title('rcp26_bcc-csm1-1  Chishan')
plt.ylabel('平均日降雨量 (mm/day)')
plt.xlabel('月份')
