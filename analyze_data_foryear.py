# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 11:21:02 2021

@author: Chia-Wei Wang
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# import datetime as dt
# import time
# import os


path = r'C:\Users\acer\Desktop\climate change'

# 'KH9_s' , 'KH9_f' , 'TN10_s' , 'TN10_f'       # <<<<<<<<<<<<<<<<<<<<<<選擇要整理的檔名
filename = 'KH9_s'      # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<輸入要整理的檔名
filepath = path + '\\' +filename


files = ['2020']
n = len(files)

# 選擇所需要的資料夾
folder = []
for i in range(0,n):
    f = files[i]
    folder.append(path+'\\'+f+'\\'+filename+'.csv')

# 將不同模式的資料串連
df = pd.concat([pd.read_csv(f1) for f1 in folder])
df.reset_index(inplace=True)
df = df.drop(['index'],axis=1)



# 擷取所要的資料
df1 = df[['model','gridID','lon','lat','ID','Yield_ha']]
df1[['a','id','b']] = df['ID'].str.split('_',expand=True)
df1 = df1.drop(['a','b'],axis=1)
# 改變資料型態
df1['id'] = df1['id'].astype(int)
# 將缺失值補上0
df1 = df1.fillna(0)
df2 = df1.iloc[:,[0,2,3,5]]



# In[8]     <<<將產量資料讀入table>>>



lot_long = set(list(df2.iloc[:, 1]))
lot_long = sorted(lot_long, reverse = False)
lat_long = set(list(df2.iloc[:, 2]))
lat_long = sorted(lat_long, reverse = True)
num_lot = len(lot_long)
num_lat = len(lat_long)
table = np.zeros((num_lat,num_lot))
repor_table = pd.DataFrame(table)
repor_table = pd.DataFrame(table,index=lat_long,columns=lot_long)



for k in range(0,6543):
    x = df2.iloc[k,1]
    y = df2.iloc[k,2]
    repor_table.loc[y,x] = int(df2.iloc[k,3])
    print(k,x,y,df2.iloc[k,3],repor_table.loc[y,x])

# In[]    <<<繪製產量Heatmap>>>
repor_table = pd.DataFrame(repor_table,columns=lot_long)
# 設定中文字型
plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
# 設定負號正確顯示
plt.rcParams["axes.unicode_minus"] = False
# plt.figure(dpi=800)
sns.heatmap(repor_table,cmap='BrBG',square=True,mask=(repor_table < 0.5))
# sns.heatmap(repor_table,vmax=6000,vmin=1000,cmap='BrBG',xticklabels=4,square=True,mask=(repor_table < 0.5))
# plt.title(filename+"  "+files)
# file_name = path + '\\'+files+'.png'
# plt.savefig(file_name, bbox_inches='tight',transparent=True)
