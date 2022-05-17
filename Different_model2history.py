# -*- coding: utf-8 -*-
"""
Created on Tue May 17 08:30:15 2022

@author: user_11
"""
import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# =============================================================================
# 輸入區

# 輸入要比對的經緯度，最小單位為0.05
(lon,lat) = (120.25,23.45)
Type = '最高溫'
rcp = ['rcp26','rcp45','rcp60','rcp85']
rcp = rcp[0]
# =============================================================================


#%% 歷史資料

# 氣象資料所在地
path = r'F:\臺灣歷史氣候重建資料_5公里'
# 讀取地區csv
site = pd.read_csv(r'F:\臺灣歷史氣候重建資料_5公里\grid_5km.csv',encoding='big5')
for i in range(site.shape[0]):
    LON = site.iloc[i,1]
    LAT = site.iloc[i,2]
    if (LON, LAT) == (lon, lat):
        file_site = site.iloc[i,3]
        break

# 選擇數據類別與.csv檔
file_his = r'F:\臺灣歷史氣候重建資料_5公里\*'+file_site+'_'+Type+'\*.csv'
# 取得絕對路經
file_list_his = glob.glob(file_his)
# 資料須為2006至2015年的資料
file_list_his = [f for f in file_list_his if int(f[-8:-4]) >=2006 and int(f[-8:-4]) <=2015]

# 建立JDAY為了排序用
df_his = [i for i in range(1,367)]
df_his = pd.DataFrame(df_his, columns=['JDAY'])
for f in file_list_his:
    df= pd.read_csv(f)
    for i in range(site.shape[0]):
        LON = df.iloc[i,0]
        LAT = df.iloc[i,1]
        if (LON, LAT) == (lon, lat):
            # 取出年度資料
            data = df.iloc[i,2:]
            # 重設index,覆蓋回去，並刪除原先的
            data.reset_index(inplace=True, drop=True)
            # 取得cloumns,並重新命名
            columns = list(df_his.columns)
            columns.append(f[-8:-4])
            df_his = pd.concat([df_his,data],axis=1)
            df_his.columns = columns
            break
# 算出平均
df_his['his_mean'] = round(df_his.iloc[:,1:].mean(axis=1),2)
calculate = df_his.iloc[:,[0,-1]]

#%% 模型資料

# 選擇數據類別與.csv檔
file_model = r'F:\TCCIP統計降尺度日資料_AR5\*'+file_site+'_'+Type+'\*.csv'
# 取得絕對路經
file_list = glob.glob(file_model)
# 篩選氣候情境
file_list = [f for f in file_list if rcp in f]
# 資料須為2026至2035年的資料
file_list = [f for f in file_list if int(f[-8:-4]) >=2026 and int(f[-8:-4]) <=2035]

# 取得有使用的model
path_model = r'F:\Maize stage future'
# 取得資料夾下，之子資料夾(檔名不含'.')
model_list = [f for f in os.listdir(path_model) if '.' not in f]
model_list.remove('__pycache__')
model_list.remove('2 km')
model_list.remove('5 km')
model_list.remove('_Draw')
model_list.remove('_Draw_2D')
model_list.remove('_Draw_3D')
model_list.remove('舊程式碼')

# 列出在情境下有使用到的model
use_model = []
for m in model_list:
    for f in file_list:
        if  m in f:
            use_model.append(m)
use_model = set(use_model)

# 跑不同模式，並分別產出DataFrame
for m in use_model:
    file_list_1 = [f for f in file_list if m in f]
    # 建立JDAY為了排序用
    df_model = [i for i in range(1,367)]
    df_model = pd.DataFrame(df_model, columns=['JDAY'])
    for f in file_list_1:
        df= pd.read_csv(f,index_col=False)
        for i in range(site.shape[0]):
            LON = df.iloc[i,0]
            LAT = df.iloc[i,1]
            if (LON, LAT) == (lon, lat):
                # 取出年度資料
                data = df.iloc[i,2:]
                # 重設index,覆蓋回去，並刪除原先的
                data.reset_index(inplace=True, drop=True)
                columns = list(df_model.columns)
                # 取得cloumns,並重新命名
                columns.append(f[-8:-4])
                df_model = pd.concat([df_model,data],axis=1)
                df_model.columns = columns
                break
    # 算出平均
    df_model[str(m+'_mean')] = round(df_model.iloc[:,1:].mean(axis=1),2)
    calculate = pd.concat([calculate,df_model.iloc[:,-1]],axis=1)
    calculate[str(m+'_dif')] = calculate[m+'_mean'] - calculate['his_mean']
    globals()[f'df_{m}'] = df_model
    num = list(use_model).index(m)+1
    num_all = len(use_model)
    print(f'{num}/{num_all}',m)

#%% 劃出差異圖

# 畫出觀測值減平均值的圖
report = []
for i in range(3,len(calculate.columns),2):
    
    plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=[6,4],dpi=200)
    
    colors = np.where(np.array(calculate.iloc[:,i]) > 0,'red','blue')
    plt.bar(calculate.iloc[:,0],calculate.iloc[:,i],color=colors)
    title_name = '未來值減歷史平均__'+calculate.columns[i][:-4]
    plt.title(title_name)
    plt.ylabel('溫度差 (℃)')
    num_dif = round(np.sum(calculate.iloc[:,i]),2)
    if num_dif > 0:
        icon_temp = '多'
    else:
        icon_temp = '少'
    num_dif = abs(num_dif)
    plt.xlabel('\n累積差異： '+icon_temp+str(num_dif)+'℃',loc='left',size = 12)
    plt.tight_layout()
    report.append([calculate.columns[i][:-4],str(icon_temp+str(num_dif)+'℃')])
    print(calculate.columns[i][:-4])

report = np.array(report)
