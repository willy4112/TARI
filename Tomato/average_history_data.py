# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 16:04:54 2021

@author: Chia-Wei Wang
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

raw = pd.read_csv(r'C:\Users\acer\Desktop\Tomato\weather_history\2001-2020.csv')
name = r'C:\Users\acer\Desktop\Tomato\weather_history\Hiswea_20012020.csv'
name1 = r'C:\Users\acer\Desktop\Tomato\weather_history\Hiswea_20012020_count.csv'


data = raw

# 將Time分割成date與hour，其格式為文字
data[['date','hour']] = data['Time'].str.split(' ',expand=True)
data = data.drop(['Time'],axis=1)
# 將date分割成Year,Month,Day，其格式為文字
data[['Year','Month','Day']] = data['date'].str.split('/',expand=True)
# 將Mounth變更格式為數字
data['Month'] = data['Month'].astype('int32')
# 將Month設為兩位數整數，缺值補0
data['Month'] = data['Month'].apply(lambda x : '{:0>2d}'.format(x))
# 將Day變更格式為數字
data['Day'] = data['Day'].astype('int32')
# 將Day設為兩位數整數，缺值補0
data['Day'] = data['Day'].apply(lambda x : '{:0>2d}'.format(x))
data['Date'] = data['Month']+'/'+data['Day']
data = data.drop(['date','Year','Month','Day'],axis=1)
# 將hour分割成Hour,Minute,Second，其格式為文字
data[['Hour','Minute']] = data['hour'].str.split(':',expand=True)

# 將格式改為數字，以利下面判斷用
data['Hour'] = data['Hour'].astype('int32')
data['Minute'] = data['Minute'].astype('int32')


# 處理hour，將起始設為0點，結束為23點
(data_row,data_columns) = data.shape
for i in range(0,data_row):
    if data.loc[i,'Minute'] == 0:
        data.loc[i,'Hour'] = data.loc[i,'Hour']-1
    else:
        pass

data = data.drop(['hour','Minute'],axis=1)

# 單位轉換
# 為轉換UV的
# in units of µmol m-2 s-1, by 0.327 J µmol-1.
# https://www.apogeeinstruments.com/conversion-ppfd-to-watts/
# data['PPFD'] = data['(MJ/m2)']*0.327*1000

# 修正2022.03.22 CCW
# Agrometeoros, Passo Fundo, v.27, n.2, p.227-258, dez 2019
# (MJ/m2) = 10^6 J/m2
# 1 hour(3600s), 10^6 J/m2 = 10^6/3600 W/m2
# MH/m2 = 277.78 W/m2
# W/m2 = 2.02 umol/m2/s
data['PPFD'] = data['(MJ/m2)']*227.78*2.02
data = data.drop(['(MJ/m2)'],axis=1)

#重排順序
data = data[['Date','Hour','Temperature','RH','PPFD']]

# 取得平均值
data1 = data.groupby(['Date','Hour'],as_index = False).mean()
data1.to_csv(name, index=False,encoding='utf-8-sig')

# 檢視資料缺失程度
# 取得數量
data2 = data.groupby(['Date'],as_index = False).count()
plt.figure(figsize=[16,9],dpi=200)
plt.plot(data2.Date,data2.Temperature,label='Temperature')
plt.plot(data2.Date,data2.RH,label='RH')
plt.plot(data2.Date,data2.PPFD,label='PPFD')
plt.legend()
# 描述原始data的資料量
data3 = data.agg('count')
data3.to_csv(name1)

# In[]
# 比較歷史差異
a = np.genfromtxt(r'C:\Users\acer\Desktop\Tomato\weather_history\Hiswea_20112020.csv',delimiter = ',',skip_header = 1)
b = np.genfromtxt(r'C:\Users\acer\Desktop\Tomato\weather_history\Hiswea_20012020.csv',delimiter = ',',skip_header = 1)
c = a-b
c_1 = np.max(c, axis=0)
c_2 = np.min(c, axis=0)
c_3 = np.mean(c, axis=0)
data4 = pd.DataFrame([c_1,c_2,c_3],index=['max','min','mean'],columns=['Date','Hour','Temperature','RH','PPFD'])
