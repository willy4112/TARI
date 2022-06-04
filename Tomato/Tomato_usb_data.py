# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 09:09:40 2021
@author: Chia-Wei Wang
"""

# import matplotlib.pyplot as plt
import pandas as pd
# import numpy as np
# import seaborn as sns
from os import walk


name = r'C:\Users\acer\Desktop\Tomato\19D-GHwea_20211228.csv'

# 讀取檔案
# 使用絕對路徑
L = []
path = r'C:\Users\acer\Desktop\Tomato\USB' #資料夾目錄
for root, dirs, files in walk(path):
  for f in files:
    fullpath = root +'\\' + f
    L.append(fullpath)


row = pd.concat([pd.read_csv(f) for f in L])
row.reset_index(inplace=True)
data = row


# 移除columns[62]
data = data.drop(data.columns[62],axis=1)
# 將Time分割成date與hour，其格式為文字
data[['date','hour']] = data['Time'].str.split(' ',expand=True)
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
data['Date'] = data['Year']+'/'+data['Month']+'/'+data['Day']
# 將hour分割成Hour,Minute,Second，其格式為文字
data[['Hour','Minute','Second']] = data['hour'].str.split(':',expand=True)
#將date與Hour群組
data['D+T'] = data['Date']+' '+data['Hour']
# 移除不需要的資料columns
data = data.drop(['hour','Minute','Second'],axis=1)
# 將Hour資料從str改為int
data['Hour'] = data['Hour'].astype('int32')

data_a = data.groupby('D+T')['Hour','19D-室內溫度','19D-室內濕度','19D-室內光度'].mean()
data_a.rename(columns={'Hour':'Hour','19D-室內溫度':'Temperature','19D-室內濕度':'RH','19D-室內光度':'PPFD'}, inplace=True)
data_a = data_a.reset_index()
data_a[['Date','hour']] = data_a['D+T'].str.split(' ',expand=True)
data_a = data_a.drop(['D+T','hour'],axis=1)
data_a = data_a[['Date','Hour','Temperature','RH','PPFD']]

data_a['Hour'] = data_a['Hour'].astype('int64')

# 匯出成cxv檔
# data_a.to_excel('19D-Greenhouse_20211228.xlsx',encoding='utf-8-sig')
data_a.to_csv(name,index=False,encoding='utf-8-sig')
