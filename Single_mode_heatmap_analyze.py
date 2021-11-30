# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 13:59:30 2021

@author: Chia-Wei Wang
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# import datetime as dt
# import time
# import os
#from matplotlib.colors import ListedColormap

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<輸入區>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
path = r'C:\Users\acer\Desktop\climate change'
filename = 'TN10_s'
m = 'bcc-csm1-1_cH2O'

df = pd.read_csv(r'C:\Users\acer\Desktop\climate change\bcc-csm1-1\TN10_s.csv')

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# 擷取所要的資料
df1 = df[['model','gridID','lon','lat','ID_2030','Yield_ha_2030','Yield_ha_2040','Yield_ha_2050']]
df1[['a','id','b']] = df['ID_2030'].str.split('_',expand=True)
df1 = df1.drop(['a','b'],axis=1)
# 改變資料型態
df1['id'] = df1['id'].astype(int)
# 將缺失值補上0
df1 = df1.fillna(0)
# In[]      繪製Heatmap

style = []
for j in range(0,930):
    value_model = df1.iloc[j,0]
    value_lon = df1.iloc[j,2]
    value_lat = df1.iloc[j,3]
    xy = [value_lon,value_lat]
    value_id = df1.iloc[j,8]
    value_50 = int(df1.iloc[j,7])
    value_40 = int(df1.iloc[j,6])
    value_30 = int(df1.iloc[j,5])
    style.append([value_model,value_lon,value_lat,xy,value_id,value_30,value_40,value_50])

titel = ['model','lon','lat','xy','id','yield_2030','yield_2040','yield_2050']
data = np.array(style)
report_table = pd.DataFrame(data,columns=titel)

df2 = report_table

lot_long = set(list(report_table.iloc[:, 1]))
lot_long = sorted(lot_long, reverse = False)
lat_long = set(list(report_table.iloc[:, 2]))
lat_long = sorted(lat_long, reverse = True)
table = np.zeros((68,40))
repor_table_1 = pd.DataFrame(table)
repor_table_1 = pd.DataFrame(table,index=lat_long,columns=lot_long)

Year = ['yield_2030','yield_2040','yield_2050']
for year in Year:
    for k in range(0,930):
        [x,y] = df2.loc[k,"xy"]
        repor_table_1.loc[y,x] = df2.loc[k,year]
    repor_table_1 = pd.DataFrame(repor_table_1,columns=lot_long)
    # 設定中文字型
    plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
    # 設定負號正確顯示
    plt.rcParams["axes.unicode_minus"] = False
    plt.figure(dpi=800)
    sns.heatmap(repor_table_1,vmax=6000,vmin=1000,cmap='RdYlGn',xticklabels=4,square=True,mask=(repor_table_1 < 0.5))
    # sns.heatmap(repor_table_1,vmax=18000,vmin=6000,cmap='BrBG',xticklabels=4,square=True,mask=(repor_table_1 < 0.5))
    plt.title(filename+"  "+m+"  "+year)
    file_name = path + '\\'+filename+'_'+m+'_'+year+'.png'
    plt.savefig(file_name, bbox_inches='tight',transparent=True)

# In[]      分析區域資料

# 讀取city資料
city = pd.read_csv(r'C:\Users\acer\Desktop\climate change\city.csv',encoding='big5')
# 將city資料與數據merge
df3 = pd.merge(df1,city)
report_city = df3.iloc[:,[5,6,7,9]]
report_city = report_city.groupby("city").describe()
# # 儲存檔案
# report_city.to_csv(filepath+'_city'+'.csv',encoding='big5')


# 讀取area資料
area = pd.read_csv(r'C:\Users\acer\Desktop\climate change\area.csv',encoding='big5')
# 將city資料與數據merge
df4 = pd.merge(df3,area)
report_area = df4.iloc[:,[5,6,7,10]]
report_area = report_area.groupby("area").mean()
# report_area = report_area.groupby("area").describe()
# report_area = report_area.T
# # 儲存檔案
# report_area.to_csv(filepath+'_area'+'.csv',encoding='big5')
