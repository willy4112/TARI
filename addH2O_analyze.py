# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 09:39:19 2022

@author: CWW
"""
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

# ID對照表
df_town = pd.read_csv(r'E:\臺灣歷史氣候重建資料_5km\grid_5km_town2.csv',encoding='BIG5')
# 取得ID清單
df_ID = list(df_town[df_town['note']==1]['ID'])

# 所有的model
model = ['bcc-csm1-1', 'canESM2', 'CCSM4', 'MIROC-ESM', 'MRI-CGCM3', 'norESM1-M']
# 選擇model
m = model[5]
# 資料路徑
path = fr'E:\下載\MAIZSIM WEA\wea file\addH2O\grd*_{m}_sumrain.csv'
# 取得累積雨量資料，為種植後+90天
files = glob.glob(path)

# 建立title
df = pd.read_csv(files[0])
title = list(df.iloc[:,0])
title.insert(0,'ID')
# 取出個別網格資料合併
data = []
for i in df_ID:
    file = [f for f in files if int(((f.split('\\')[-1]).split('_')[0])[3:])== i][0]
    df = pd.read_csv(file)
    d = list(df.iloc[:,1])
    d.insert(0,i)
    data.append(d)
# 轉換為DataFrame
data = pd.DataFrame(data,columns = title)
# 加入經緯度鄉鎮資料
df = df_town[df_town['note']==1]
df = df.reset_index(drop=True)
data = pd.concat([df,data.iloc[:,1:]],axis=1)

# <<<<<<<<<<<<<<<<<<<這邊要修改>>>>>>>>>>>>>>>>>>>>>>>>>>


data.to_csv(fr'E:\下載\MAIZSIM WEA\wea file\addH2O\rcp45_{m}_sumrain.csv')
# 畫圖區1
run = [title[l] for l in range(1,len(title),2)]

for i in run:
    year = i.split('/')[-1]
    lis_lon = set(list(data['LON']))
    lis_lon = sorted(lis_lon, reverse = False)
    lis_lat = set(list(data['LAT']))
    lis_lat = sorted(lis_lat, reverse = True)
    
    plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
    plt.rcParams["axes.unicode_minus"] = False
    plt.figure(figsize=[7,8],dpi = 100)
    plt.scatter(data['LON'],data['LAT'],marker='s',s=40, c=data[i],vmin=0,vmax=1000,cmap='RdYlGn')
    
    
    plt.xlim(119.5, 122.5)
    plt.ylim(21.5, 25.5)
    plt.axis('equal')
    plt.colorbar()
    plt.xlabel('lon')
    plt.ylabel('lat')
    plt.title(f'rcp45_{m}_sumrain0322_{year}')
    plt.tight_layout()
    save_path = fr'E:\下載\MAIZSIM WEA\wea file\addH2O\rcp45_{m}\春作'
    os.makedirs(save_path, exist_ok=True)
    file_name = fr'E:\下載\MAIZSIM WEA\wea file\addH2O\rcp45_{m}\春作\rcp45_{m}_sumrain0322_{year}.png'
    plt.savefig(file_name, bbox_inches='tight',transparent=False)
    
# 畫圖區2
run = [title[l] for l in range(2,len(title),2)]

for i in run:
    year = i.split('/')[-1]
    lis_lon = set(list(data['LON']))
    lis_lon = sorted(lis_lon, reverse = False)
    lis_lat = set(list(data['LAT']))
    lis_lat = sorted(lis_lat, reverse = True)
    
    plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
    plt.rcParams["axes.unicode_minus"] = False
    plt.figure(figsize=[7,8],dpi = 100)
    plt.scatter(data['LON'],data['LAT'],marker='s',s=40, c=data[i],vmin=0,vmax=1000,cmap='RdYlGn')
    
    
    plt.xlim(119.5, 122.5)
    plt.ylim(21.5, 25.5)
    plt.axis('equal')
    plt.colorbar()
    plt.xlabel('lon')
    plt.ylabel('lat')
    plt.title(f'rcp45_{m}_sumrain0922_{year}')
    plt.tight_layout()
    save_path = fr'E:\下載\MAIZSIM WEA\wea file\addH2O\rcp45_{m}\秋作'
    os.makedirs(save_path, exist_ok=True)
    file_name = fr'E:\下載\MAIZSIM WEA\wea file\addH2O\rcp45_{m}\秋作\rcp45_{m}_sumrain0922_{year}.png'
    plt.savefig(file_name, bbox_inches='tight',transparent=False)
