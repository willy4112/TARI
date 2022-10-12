# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 09:55:42 2022

@author: CWW
"""
#%% 分析各網格氣象檔，並依照風險儲存

import os
import glob
import pandas as pd

# ID對照表
df_town = pd.read_csv(r'G:\臺灣歷史氣候重建資料_5km\grid_5km_town2.csv',encoding='BIG5')
# 取得ID清單
df_ID = list(df_town[df_town['note']==1]['ID'])

day = pd.date_range('2025-01-01', '2055-12-31')
# day = pd.date_range('2020-01-01', '2020-12-31')
day = day.strftime('%m/%d')
plant = ['03/20','09/22']
# 取得日期的indsx
dayloc = day.isin(plant)
dayloc = [i for i in range(day.shape[0]) if dayloc[i]== True]



model = ['bcc-csm1-1', 'canESM2', 'CCSM4', 'MIROC-ESM', 'MRI-CGCM3', 'norESM1-M']
# model = ['his2020', ]
m = model[0]
for m in model:
    
    # file1 = r'C:\Users\TARI\Downloads\MAIZSIM WEA\wea file\grd235_rcp45_bcc-csm1-1.wea'
    path  = r'C:\Users\TARI\Downloads\MAIZSIM WEA\wea file'
    # ID = df_ID[0]
    list_all = glob.glob(path+f'\\*{m}.wea')
    
    # file = list_all[0]
    
    
    for f in list_all:
        file = f
        
        row0 = (file.split('\\')[-1]).split('.')[0]
        
        df1 = pd.read_table(file,header=None)
        df1 = pd.read_csv(file,sep=" ",skiprows=1,header=0)
        df2 = df1.copy()
        
        # df2['Date'] = pd.to_datetime(df2['Date'], format='%m/%d/%Y').dt.strftime('%Y/%m/%d')
        
        def anyalsis_wea(kind,target,threshold,bs,long):
            # 要分析的風險
            kind = kind
            # 分析的wae目標
            target = target
            # 分析的門檻值
            threshold = threshold
            # >= or <=
            bs = bs
            # 現象持續時間
            long = long
            
            # 判斷資料是否符合條件，回傳1或0
            if bs == 'B' :
                df2[kind] = (df2[target] >= threshold)*1
            elif bs == 'S' :
                df2[kind] = (df2[target] <= threshold)*1
            L = []
            for n in dayloc:
                # 計算發生次數
                times = 0
                # 單年的發生清單
                p = []
                # 分析起始點(種植日)
                start = df2.loc[n,'Date']
                # 起始點對齊
                s = n
                p.append(start)
                # 如果種植後90添加總>0才計算
                if df2.loc[n:n+90,kind].sum() > 0:
                    for i in range(0,91):
                        n1 = df2.loc[n+i,kind]
                        n2 = df2.loc[n+i+1,kind]
                        # 分析1跟0的變化
                        if n1 == 0 and n2 ==0:
                            pass
                        elif n1 == 0 and n2 ==1:
                            s = n+i
                        elif n1 == 1 and n2 == 0:
                            # 計算發生多久
                            daylong = n+i-s
                            # 判斷是否為災害
                            if daylong >= long:
                                times += 1
                                time = df2.loc[s,'Date']
                                p.append(time)
                                p.append(daylong)
                        else:
                            pass
                p.insert(1,times)
                L.append(p)
            # 將資料轉為DataFrame
            L = pd.DataFrame(L)
            # 設定columns名稱
            L.rename(columns={0: 'plantday',1: 'times'}, inplace=True)
            return L
        
        L_hot = anyalsis_wea('hot','Tmax',37.0,'B',1)
        # L_cold = anyalsis_wea('cold','Tmin',15.0,'S',1)
        # L_dry = anyalsis_wea('dry','rain',0.6,'S',20)
        # L_wet = anyalsis_wea('wet','rain',200,'B',1)
        # L_big_wind =anyalsis_wea('big_wind','Wind',8.5,'B',1)
        
        def savefile(df,row0,model,kind):
            df = df
            row0 = row0
            model = model
            kind = kind
            save_path = fr'C:\Users\TARI\Downloads\MAIZSIM WEA\wea file\analysis\{kind}'
            os.makedirs(save_path, exist_ok=True)
            df.to_csv(fr'C:\Users\TARI\Downloads\MAIZSIM WEA\wea file\analysis\{kind}\{row0}_{kind}_35.csv',header=True,index=False,encoding= 'utf-8')
        
        _ = savefile(L_hot,row0,m,'hot')
        # _ = savefile(L_cold,row0,m,'cold')
        # _ = savefile(L_dry,row0,m,'dry')
        # _ = savefile(L_wet,row0,m,'wet')
        # _ = savefile(L_big_wind,row0,m,'big_wind')
        print(row0)

#%% 整併網格風險csv

import glob
import pandas as pd

# ID對照表
df_town = pd.read_csv(r'G:\臺灣歷史氣候重建資料_5km\grid_5km_town2.csv',encoding='BIG5')
df_town = df_town[df_town['note']==1]
df_town = df_town.reset_index(drop=True)
# 取得ID清單
df_ID = list(df_town[df_town['note']==1]['ID'])

# 分險
kind = ['hot', 'cold', 'dry', 'wet', 'big_wind']
k = kind[0]
# 氣候模式
# model = ['bcc-csm1-1', 'canESM2', 'CCSM4', 'MIROC-ESM', 'MRI-CGCM3', 'norESM1-M']
model = ['his2020', ]
# m = model[0]
for m in model:
    
    
    # 路徑
    path = r'C:\Users\TARI\Downloads\MAIZSIM WEA\wea file\analysis'
    
    data = []
    for i in df_ID:
        
    # ID = df_ID[0]
    
        file = glob.glob(path+f'\\{k}\grd{i}_*{m}_{k}.csv')
        
        df = pd.read_csv(file[0])
        d = list(df.iloc[:,1])
        data.append(d)
        # 運行進度
        print(round(df_ID.index(i)/len(df_ID)*100,1),'%')
    
    titel = list(df.iloc[:,0])
    data = pd.DataFrame(data, columns = titel)
    # 將數值變為0 & 1
    data = (data > 0)*1
    report = pd.concat([df_town.iloc[:,[0,1,2,5,6]],data],axis=1)
    report.to_csv(fr'C:\Users\TARI\Downloads\MAIZSIM WEA\wea file\analysis\{k}\rcp45_{m}_{k}.csv',index=False,encoding='utf-8')

#%% 氣候模式合併
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point

df_town = pd.read_csv(r'G:\臺灣歷史氣候重建資料_5km\grid_5km_town2.csv',encoding='BIG5')
df_town = df_town[df_town['note']==1]
df_town = df_town.reset_index(drop=True)
df_town = df_town.iloc[:,[0,1,2,5,6]]

# kind = ['hot', 'cold', 'dry', 'wet', 'big_wind']
kind = ['hot',]
# k = kind[0]
for k in kind:
    
    model = ['bcc-csm1-1', 'canESM2', 'CCSM4', 'MIROC-ESM', 'MRI-CGCM3', 'norESM1-M']
    
    m1 = pd.read_csv(fr'C:\Users\TARI\Downloads\MAIZSIM WEA\wea file\analysis\{k}\rcp45_bcc-csm1-1_{k}_35.csv')
    m1 = m1.iloc[:,5:]
    m2 = pd.read_csv(fr'C:\Users\TARI\Downloads\MAIZSIM WEA\wea file\analysis\{k}\rcp45_canESM2_{k}_35.csv')
    m2 = m2.iloc[:,5:]
    m3 = pd.read_csv(fr'C:\Users\TARI\Downloads\MAIZSIM WEA\wea file\analysis\{k}\rcp45_CCSM4_{k}_35.csv')
    m3 = m3.iloc[:,5:]
    m4 = pd.read_csv(fr'C:\Users\TARI\Downloads\MAIZSIM WEA\wea file\analysis\{k}\rcp45_MIROC-ESM_{k}_35.csv')
    m4 = m4.iloc[:,5:]
    m5 = pd.read_csv(fr'C:\Users\TARI\Downloads\MAIZSIM WEA\wea file\analysis\{k}\rcp45_MRI-CGCM3_{k}_35.csv')
    m5 = m5.iloc[:,5:]
    m6 = pd.read_csv(fr'C:\Users\TARI\Downloads\MAIZSIM WEA\wea file\analysis\{k}\rcp45_norESM1-M_{k}_35.csv')
    m6 = m6.iloc[:,5:]
    
    total = round((m1 + m2 + m3 + m4 + m5 + m6)/6*100, 2)
    total = pd.concat([df_town,total], axis=1)
    
    filename = fr'C:\Users\TARI\Downloads\MAIZSIM WEA\wea file\analysis\{k}\Avg_{k}_35.csv'
    total.to_csv(filename,index = False, encoding='utf-8')
    
    
    # 輸入地圖檔
    TW_map = gpd.read_file(r'C:\Users\TARI\Downloads\mapdata202203151023\COUNTY_MOI_1090820.shp',encoding='utf-8')
    # 改變地圖編碼為 WGS84(epsg=4326)，經緯度系統
    TW_map = TW_map.to_crs(epsg=4326)
    
    # 將經緯度併入GIS編碼
    geom = [Point(xy) for xy in zip(total.LON, total.LAT)]
    # 設定地圖編碼
    crs = {'init': 'epsg:4326'}
    gdf = gpd.GeoDataFrame(total, crs=crs, geometry=geom)
    
    title = total.columns
    run = [title[l] for l in range(5,len(title)-1,2)]
    
    for i in run:
        
        year = i.split('/')[-1]
        
        # 設定中文字型
        plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
        # 設定負號正確顯示
        plt.rcParams["axes.unicode_minus"] = False
        
        # 設定畫框
        fig, ax = plt.subplots(1, figsize=(10, 10),dpi=75)
        # 劃出縣市邊界
        TW_map.boundary.plot(color = 'Black', ax=ax,alpha=0.25)
        # 畫出數據
        gdf.plot(column=i, ax=ax,cmap='RdYlGn_r',vmin = 0,vmax = 100,marker='s',markersize=50,legend=True,alpha=0.75, legend_kwds={'label':'發生機率(%)'})
        
        
        # 設定經緯度範圍
        _ = ax.set_xlim([119.8, 122.2])
        _ = ax.set_ylim([21.8, 25.4])
        
        plt.xlabel('lon')
        plt.ylabel('lat')
        plt.title(f'rcp45_{k}_0320_{year}_35')
        
        save_path = fr'C:\Users\TARI\Downloads\MAIZSIM WEA\wea file\analysis\{k}\春作'
        os.makedirs(save_path, exist_ok=True)
        file_name = fr'C:\Users\TARI\Downloads\MAIZSIM WEA\wea file\analysis\{k}\春作\rcp45_{k}_0320_{year}_35.png'
        plt.savefig(file_name, bbox_inches='tight',transparent=False)
        plt.close()
    
    
    run = [title[l] for l in range(6,len(title)-1,2)]
    
    for i in run:
        
        year = i.split('/')[-1]
        
        # 設定中文字型
        plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
        # 設定負號正確顯示
        plt.rcParams["axes.unicode_minus"] = False
        
        # 設定畫框
        fig, ax = plt.subplots(1, figsize=(10, 10),dpi=75)
        # 劃出縣市邊界
        TW_map.boundary.plot(color = 'Black', ax=ax,alpha=0.25)
        # 畫出數據
        gdf.plot(column=i, ax=ax,cmap='RdYlGn_r',vmin = 0,vmax = 100,marker='s',markersize=50,legend=True,alpha=0.75, legend_kwds={'label':'發生機率(%)'})
        
        
        # 設定經緯度範圍
        _ = ax.set_xlim([119.8, 122.2])
        _ = ax.set_ylim([21.8, 25.4])
        
        plt.xlabel('lon')
        plt.ylabel('lat')
        plt.title(f'rcp45_{k}_0922_{year}_35')
        
        save_path = fr'C:\Users\TARI\Downloads\MAIZSIM WEA\wea file\analysis\{k}\秋作'
        os.makedirs(save_path, exist_ok=True)
        file_name = fr'C:\Users\TARI\Downloads\MAIZSIM WEA\wea file\analysis\{k}\秋作\rcp45_{k}_0922_{year}_35.png'
        plt.savefig(file_name, bbox_inches='tight',transparent=False)
        plt.close()
    print(f'{k} done.')

#%% 對於連續乾旱分析

import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''
109年甜玉米_收穫面積排序
雲林 虎尾(7%)：[681, 682]
雲林 元長(7%)：[622, 650, 651]
雲林 土庫(6%)：[680]
嘉義 六腳(6%)：[563, 564, 593]
雲林 東勢(6%)：[678]
台南 安南(2%)：[279, 280, 306, 307, 308]
'''

file = r'C:\Users\TARI\Downloads\MAIZSIM WEA\wea file\analysis\dry\Avg_dry.csv'

df = pd.read_csv(file)
ID = 682

df1 = df[(df['ID']==ID)]
drow = df1.iloc[:,5:].T.astype('float')

plt.figure(figsize=(12, 5),dpi=200)
plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.rcParams["axes.unicode_minus"] = False

plt.plot(drow,marker='o')
xticks = list((drow.index))
xticks = [i.split('/')[-1] for i in xticks]
x = np.arange(0,len(xticks),10)
plt.xticks(x,xticks[::10])
plt.axhline(y=80, color='r', linestyle='-')
plt.ylabel('%',fontsize=14)
plt.xlabel('\n\n判定標準：連續20天日累積降雨量小於0.6mm\n選用氣候模式：bcc-csm1-1, canESM2, CCSM4, MIROC-ESM, MRI-CGCM3, norESM1-M',loc='left')
plt.title(f'grd_{ID} 乾旱發生百分比',fontsize=16)
plt.grid(axis='x')

#%% 分析單點

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''
109年甜玉米_收穫面積排序
雲林 虎尾(7%)：[681, 682]
雲林 元長(7%)：[622, 650, 651]
雲林 土庫(6%)：[680]
嘉義 六腳(6%)：[563, 564, 593]
雲林 東勢(6%)：[678]
台南 安南(2%)：[279, 280, 306, 307, 308]
'''

# =============================================================================
# 控制區
ID = 682
rcp = 'rcp45'
kind = '降雨量'
# =============================================================================

file_ID = r'G:\臺灣歷史氣候重建資料_5km\grid_5km_town_soilman_mount.csv'
df_ID = pd.read_csv(file_ID)

# file_his = r'C:\Users\TARI\Downloads\氣象檔\雲林分場72K220_month_200001_202210.csv'
file_his = r'C:\Users\TARI\Downloads\氣象檔\C0K330\C0K330虎尾_月_201507_202209.csv'
name = (file_his.split('\\')[-1]).split('_')[0]
df_his = pd.read_csv(file_his, encoding = 'big5')
df_his = df_his.loc[:,['觀測時間', kind]]

year = 2000
n = 1
for i in range(df_his.shape[0]):
    if n ==12:
        df_his.loc[i,'觀測時間'] = str(year) + '{0:02d}'.format(n)
        year += 1
        n = 0
    else:
        df_his.loc[i,'觀測時間'] = str(year) + '{0:02d}'.format(n)
    n +=1

df_his.index = df_his['觀測時間']
df_his = df_his.loc[:, kind]
df_his = df_his.astype('float')



df_ID = df_ID[(df_ID['ID']==ID)]
df_ID = df_ID.loc[:,['LON', 'LAT', 'SITE']]
lon, lat, site = df_ID.iloc[0,:]

model = ['bcc-csm1-1', 'canESM2', 'CCSM4', 'MIROC-ESM', 'MRI-CGCM3', 'norESM1-M']
# model = ['canESM2', ]

# plt.figure(figsize=[12,18],dpi = 200)
fig, ax = plt.subplots(6, 1, sharex=True, sharey=True, figsize=[11, 11],dpi = 200)

plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False
plt.suptitle(f'grd{ID}_{name}_{kind}', fontsize=16, y=0.92)

n = 0
for m in model:
    
    file1 = fr'G:\TCCIP統計降尺度月資料_AR5\AR5_統計降尺度_月資料_{site}_{kind}\AR5_統計降尺度_月資料_{site}_{kind}_rcp45_{m}.csv'
    df1 = pd.read_csv(file1)
    df1 = df1[(df1['LON'] == lon)]
    df1 = df1[(df1['LAT'] == lat)]
    df1 = df1.iloc[0,2:-1].T
    
    file2 = fr'G:\TCCIP統計降尺度月資料_AR5\AR5_統計降尺度_月資料_{site}_{kind}\AR5_統計降尺度_月資料_{site}_{kind}_rcp85_{m}.csv'
    df2 = pd.read_csv(file2)
    df2 = df2[(df2['LON'] == lon)]
    df2 = df2[(df2['LAT'] == lat)]
    df2 = df2.iloc[0,2:-1].T
    
    df = pd.concat([df_his, df1.loc['202210':], df2.loc['202210':]], axis = 1, keys = ['his', 'rcp45', 'rcp85'])
    df = df.loc[:'205601',:]
    df = df.astype('float')
    if kind == '降雨量':
        df['rcp45'] = df['rcp45'] * 30
        df['rcp85'] = df['rcp85'] * 30
        ymin = 0
        ymax = 1200
        linestyle = '-'
        ylable = '(mm)'
    elif kind == '最高溫':
        ymin = 17.5
        ymax = 42.5
        linestyle = '--'
        ylable = '℃'
    else:
        ymin = 0
        ymax = 100
        linestyle = '--'
        
    df.to_csv(fr'C:\Users\TARI\Downloads\MAIZSIM WEA\wea file\singlepoint_wea\grd{ID}_{m}_{name}_{kind}.csv', index = True, encoding = 'utf-8-sig')

    
    # plt.subplot(6,1,n)
    ax[n].plot(df['his'], label='history')
    ax[n].plot(df['rcp45'], label='rcp4.5',linestyle = linestyle)
    ax[n].plot(df['rcp85'], label='rcp8.5',linestyle = linestyle)
    ax[n].set_ylabel(f'{m}\n\n{ylable}')
    ax[n].set_xlim(-5, 0)
    ax[n].set_ylim(ymin, ymax)
    xticks = list(df.index)
    xticks = [x[:-2] for x in xticks]
    x = np.arange(0,len(xticks),60)
    ax[n].set_xticks(x+0.5,xticks[::60])
    ax[n].legend(bbox_to_anchor=(1.01, 0.5, 0.125, 0), loc=6, mode="expand", borderaxespad=0.1)
    # ax[n].legend(loc = 'lower left')
    n += 1
file_name = fr'C:\Users\TARI\Downloads\MAIZSIM WEA\wea file\singlepoint_wea\grd{ID}_{name}_{kind}.png'
plt.savefig(file_name, bbox_inches='tight',transparent=False)

#%% 分析單點-未來由日資料統計

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''
109年甜玉米_收穫面積排序
雲林 虎尾(7%)：[681, 682]
雲林 元長(7%)：[622, 650, 651]
雲林 土庫(6%)：[680]
嘉義 六腳(6%)：[563, 564, 593]
雲林 東勢(6%)：[678]
台南 安南(2%)：[279, 280, 306, 307, 308]
'''

# =============================================================================
# 控制區
ID = 682
rcp = 'rcp45'
kind = '最低溫'
# =============================================================================

file_ID = r'G:\臺灣歷史氣候重建資料_5km\grid_5km_town_soilman_mount.csv'
df_ID = pd.read_csv(file_ID)

file_his = r'C:\Users\TARI\Downloads\氣象檔\雲林分場72K220_month_200001_202210.csv'
# file_his = r'C:\Users\TARI\Downloads\氣象檔\C0K330\C0K330虎尾_月_201507_202209.csv'
name = (file_his.split('\\')[-1]).split('_')[0]
df_his = pd.read_csv(file_his, encoding = 'big5')
df_his = df_his.loc[:,['觀測時間', kind]]
df_his['觀測時間'] = df_his['觀測時間'].str.replace("_","")
df_his.index = df_his['觀測時間']
df_his = df_his.loc[:, kind]
df_his = df_his.astype('float',errors='ignore')



df_ID = df_ID[(df_ID['ID']==ID)]
df_ID = df_ID.loc[:,['LON', 'LAT', 'SITE']]
lon, lat, site = df_ID.iloc[0,:]

# model = ['bcc-csm1-1', 'canESM2', 'CCSM4', 'MIROC-ESM', 'MRI-CGCM3', 'norESM1-M']
model = ['canESM2', ]

# # plt.figure(figsize=[12,18],dpi = 200)
# fig, ax = plt.subplots(6, 1, sharex=True, sharey=True, figsize=[11, 11],dpi = 200)

# plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
# plt.rcParams['axes.unicode_minus'] = False
# plt.suptitle(f'grd{ID}_{name}_{kind}', fontsize=16, y=0.92)

n = 0
for m in model:
    "G:\TCCIP統計降尺度日資料_AR5\AR5_統計降尺度_日資料_中部_最高溫\AR5_統計降尺度_日資料_中部_最高溫_rcp60_MIROC5_2007.csv"
#     data = pd.DataFrame()
#     for i in range(2022,2056):
#         file1 = fr'G:\TCCIP統計降尺度日資料_AR5\AR5_統計降尺度_日資料_{site}_{kind}\AR5_統計降尺度_日資料_{site}_{kind}_rcp45_{m}_{i}.csv'
#         # index_col=False，防止資料被帶入index
#         df1 = pd.read_csv(file1, index_col=False)
#         # 處理資料中空白的問題
#         df1.columns = df1.columns.str.replace(" ","")
        
#         df1 = df1[(df1['LON'] == lon) & (df1['LAT'] == lat)]
#         df1 = df1.iloc[0,2:-1].T
#         month = [m[4:6] for m in df1.index]
#         df1.index = month
#         df1 = round(df1.groupby(df1.index).mean(), 2)
#         df1.index = [str(i)+m for m in df1.index]
#         data = pd.concat([data,df1])

file1 = fr'G:\TCCIP統計降尺度月資料_AR5\AR5_統計降尺度_月資料_{site}_{kind}\AR5_統計降尺度_月資料_{site}_{kind}_historical_{m}.csv'
df1 = pd.read_csv(file1, index_col=False)
df1.columns = df1.columns.str.replace(" ","")

df1 = df1[(df1['LON'] == lon ) & (df1['LAT'] == lat)]
df1 = df1.iloc[0,2:-1].T


file2 = fr'G:\TCCIP統計降尺度月資料_AR5\AR5_統計降尺度_月資料_{site}_{kind}\AR5_統計降尺度_月資料_{site}_{kind}_rcp45_{m}.csv'
df2 = pd.read_csv(file2, index_col=False)
df2.columns = df2.columns.str.replace(" ","")

df2 = df2[(df2['LON'] == lon ) & (df2['LAT'] == lat)]
df2 = df2.iloc[0,2:-1].T

data1 = pd.concat([df_his, df1, df2], axis = 1, keys=['obs', 'model_his','model_rcp45'])
data1 = data1.sort_index()
data1 = data1.loc['200001':'206012',:]
# 計算偏差
data1['obs-model_his'] = data1['obs'] - data1['model_his']
data1['obs-model_rcp45'] = data1['obs'] - data1['model_rcp45']
# 修正偏差
data1['cal_model_his'] = data1['model_his'] + data1['obs-model_his'].mean()
data1['cal_model_rcp45'] = data1['model_rcp45'] + data1['obs-model_rcp45'].mean()



plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False
plt.figure( figsize=[15, 5],dpi = 200)

plt.plot(data1['obs'], label='obs',linestyle = '-')
plt.plot(data1['model_his'], label='model_his',linestyle = '-')
plt.plot(data1['model_rcp45'], label='model_rcp45',linestyle = '-')
# plt.plot(data1['cal_model_his'], label='cal_model_his',linestyle = '-')
# plt.plot(data1['cal_model_rcp45'], label='cal_model_rcp45',linestyle = '-')
plt.title(f'{m}  {kind}')
xticks = list(data1.index)
xticks = [x[:-2] for x in xticks]
x = np.arange(0,len(xticks),60)
plt.xticks(x+0.5,xticks[::60])
# plt.ylim(17.5, 42.5)
plt.ylim(2.5, 42.5)
plt.legend()
