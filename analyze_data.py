# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 11:21:02 2021

@author: Chia-Wei Wang
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
# import datetime as dt
# import time
import os

path = os.getcwd()

# KH9_s , KH9_f , TN10_s , TN10_f       # <<<<<<<<<<<<<<<<<<<<<<選擇要整理的檔名
filename = 'TN10_f'      # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<輸入要整理的檔名
filepath = path + '\\' +filename


# 取得位於那些資料夾
# files = ['bcc-csm1-1','MIROC-ESM','NorESM1-M']
files = ['bcc-csm1-1','camESM2','CCSM4','MIROC-ESM','MRI-CGCM3','NorESM1-M']


# 選擇所需要的資料夾
folder = []
for i in range(0,6):
    f = files[i]
    folder.append(path+'\\'+f+'\\'+filename+'.csv')

# 將不同模式的資料串連
df = pd.concat([pd.read_csv(f1) for f1 in folder])
df.reset_index(inplace=True)
df = df.drop(['index'],axis=1)
df.rename(columns={"Yield_ha":"Yield_ha_2030",
                    "Yield_ha.1":"Yield_ha_2040",
                    "Yield_ha.2":"Yield_ha_2050",},inplace=True)



# <<<取25%,50%,75% 分布數值>>>

# 擷取所要的資料
df1 = df[['model','gridID','lon','lat','ID','Yield_ha_2030','Yield_ha_2040','Yield_ha_2050']]
df1[['a','id','b']] = df['ID'].str.split('_',expand=True)
df1 = df1.drop(['a','b'],axis=1)
# 改變資料型態
df1['id'] = df1['id'].astype(int)
# 將缺失值補上0
df1 = df1.fillna(0)
# 以ID為基準的解析數據
df2 = df1.groupby("id").describe()
# 取出所需的資料
report_dif_model = df2.iloc[:,[1,9,16,17,20,21,22,24,25,28,29,30,32,33,36,37,38]]    # <<<<<<<<<<<<<<<<<<<<<<<<查看df2來選所需的columns
# # 儲存檔案
report_dif_model.to_csv(filepath+'_dif_model'+'.csv')



# <<<比較各年度產量變化>>>

# style = 1, 2030>2040>2050
# style = 2, 2030>2050>2040
# style = 3, 2040>2030>2050
# style = 4, 2040>2050>2030
# style = 5, 2050>2040>2030
# style = 6, 2050>2030>2040

style = []
for j in range(0,5580):
    value_model = df1.iloc[j,0]
    value_lon = df1.iloc[j,2]
    value_lat = df1.iloc[j,3]
    xy = [value_lon,value_lat]
    value_id = df1.iloc[j,8]
    value_50 = int(df1.iloc[j,7])
    value_40 = int(df1.iloc[j,6])
    value_30 = int(df1.iloc[j,5])

    if value_50 > value_30 and value_50 > value_40:
        if value_40 > value_30:
            s = 6
        else:
            s = 5
    elif value_40 > value_30 and value_40 > value_50:
        if value_50 > value_30:
            s = 4
        else:
            s = 3
    else:
        if value_50 > value_40:
            s = 2
        else:
            s = 1
    style.append([value_model,value_lon,value_lat,xy,value_id,value_30,value_40,value_50,s])

titel = ['model','lon','lat','xy','id','yield_2030','yield_2040','yield_2050','style']
data = np.array(style)
report_style = pd.DataFrame(data,columns=titel)
# 儲存檔案
report_style.to_csv(filepath+'_style'+'.csv')



# <<<繪製heatmap在不同氣候模式下>>>
# # 取得lot與lat的資料長度
# lot_long = set(list(report_style.iloc[:, 1]))
# lat_long = set(list(report_style.iloc[:, 2]))
# table = np.zeros((40,68))
# repor_table = pd.DataFrame(table,index=lot_long,columns=lat_long)
# # 將list填入表格
# # bcc-csm1-1 , camESM2 , CCSM4 , MIROC-ESM , MRI-CGCM3 , NorESM1-M
# m = 'bcc-csm1-1'
# df3 = report_style[(report_style['model']==m)]
# for k in range(0,930):
#     [x,y] = df3.loc[k,"xy"]
#     repor_table.loc[x,y] = df3.loc[k,"style"]
# # 設定中文字型
# plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
# # 設定負號正確顯示
# plt.rcParams["axes.unicode_minus"] = False
# plt.figure(dpi=800)
# sns.heatmap(repor_table,vmax=6, vmin=1,cmap='Set1',square=True,mask=(repor_table < 1))
# plt.title(m)


# <<<繪製不同氣候模型下的產量變化>>>
drow_table = report_style.iloc[:,[0,8]]
L1 = report_style[(report_style['model']=='bcc-csm1-1')].groupby('style')['model'].count()
L2 = report_style[(report_style['model']=='canESM2')].groupby('style')['model'].count()
L3 = report_style[(report_style['model']=='CCSM4')].groupby('style')['model'].count()
L4 = report_style[(report_style['model']=='MIROC-ESM')].groupby('style')['model'].count()
L5 = report_style[(report_style['model']=='MRI-CGCM3')].groupby('style')['model'].count()
L6 = report_style[(report_style['model']=='NorESM1-M')].groupby('style')['model'].count()
drow_style = pd.concat([L1,L2,L3,L4,L5,L6], axis=1)
drow_style.columns=files
drow_style = drow_style.fillna(0)
plt.figure(dpi=800)
drow_style.plot(kind='bar')
note = ' \n 1：2030>2040>2050     2：2030>2050>2040\n 3：2040>2030>2050     4：2040>2050>2030\n 5：2050>2040>2030     6：2050>2030>2040\n'
plt.xlabel(note,loc='left')