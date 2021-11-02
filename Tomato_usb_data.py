# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 09:09:40 2021

@author: Chia-Wei Wang
"""

# import matplotlib.pyplot as plt
import pandas as pd
# import numpy as np
# import seaborn as sns

# 讀取檔案
# 使用絕對路徑
data1=pd.read_csv(r"C:\Users\acer\Desktop\Tomato\USB\202109\MAC256840_20210929_01.csv",encoding='utf-8')
data2=pd.read_csv(r"C:\Users\acer\Desktop\Tomato\USB\202109\MAC256840_20210929_02.csv",encoding='utf-8')
data3=pd.read_csv(r"C:\Users\acer\Desktop\Tomato\USB\202109\MAC256840_20210929_00.csv",encoding='utf-8')
data4=pd.read_csv(r"C:\Users\acer\Desktop\Tomato\USB\202109\MAC256840_20210930_00.csv",encoding='utf-8')

# 上下合併
data = pd.concat([data1,data2,data3,data4],axis=0)
# 移除columns[62]
data = data.drop(data.columns[62],axis=1)
# 將Time分割成date與hour，其格式為文字
data[['date','hour']] = data['Time'].str.split(' ',expand=True)
# 將hour分割成Hour,Minute,Second，其格式為文字
data[['Hour','Minute','Second']] = data['hour'].str.split(':',expand=True)
#將date與Hour群組
data['D+T'] = data['date']+' '+data['Hour']
# 移除不需要的資料columns
data = data.drop(['hour','Minute','Second'],axis=1)
# 將Hour資料從str改為int
data['Hour'] = data['Hour'].astype('int32')


# 另指定DataFrame為data_a,將data資料以Hour移除重複
data_a = data.drop_duplicates(subset='D+T', keep='first', inplace=False)
# 移除0:62 columns
data_a = data_a.drop(data_a.columns[0:62],axis=1)
# 重設index
data_a = data_a.reset_index()
# 移除index columns
data_a = data_a.drop(['index'],axis=1)
# 調整columns順序
data_a =data_a[['D+T','date','Hour']]
# 移除Hour columns
data_a = data_a.drop(['Hour'],axis=1)


# 用groupby計算
data_b = data.groupby('D+T')['Hour','19D-室內溫度','19D-室內濕度','19D-室內光度'].mean()
#重新命名columns
data_b.rename(columns={'Hour':'Hour','19D-室內溫度':'Temperature','19D-室內濕度':'RH','19D-室內光度':'PPFD'}, inplace=True)
# 轉換成DataFeame形式
data_b = pd.DataFrame(data_b)
# 重設index
data_b = data_b.reset_index()
# 移除Hour columns
data_b = data_b.drop(['D+T'],axis=1)
# data_a,data_b左右合併
data_c = pd.concat([data_a,data_b],axis=1)


# 匯出成cxv檔
# data_c.to_excel('19D-Greenhouse_20210929.xlsx',encoding='utf-8-sig')
data_c.to_csv('19D-GHwea.csv',encoding='utf-8-sig')

