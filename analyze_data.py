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
from matplotlib.colors import ListedColormap

path = r'C:\Users\acer\Desktop\climate change'

# 'KH9_s' , 'KH9_f' , 'TN10_s' , 'TN10_f'       # <<<<<<<<<<<<<<<<<<<<<<選擇要整理的檔名
filename = 'TN10_f'      # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<輸入要整理的檔名
filepath = path + '\\' +filename

# In[1]     取得位於那些資料夾
# files = ['bcc-csm1-1','MIROC-ESM','NorESM1-M']
# files = ['bcc-csm1-1','camESM2']
files = ['bcc-csm1-1','camESM2','CCSM4','MIROC-ESM','MRI-CGCM3','NorESM1-M']
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


# df3 = city_data.groupby("city").describe()
# In[2]     <<<取25%,50%,75% 分布數值>>>

# 擷取所要的資料
df1 = df[['model','gridID','lon','lat','ID_2030','Yield_ha_2030','Yield_ha_2040','Yield_ha_2050']]
df1[['a','id','b']] = df['ID_2030'].str.split('_',expand=True)
df1 = df1.drop(['a','b'],axis=1)
# 改變資料型態
df1['id'] = df1['id'].astype(int)
# 將缺失值補上0
df1 = df1.fillna(0)
# 以ID為基準的解析數據
df2 = df1.groupby("id").describe()
# 取出所需的資料
report_dif_model = df2.iloc[:,[1,9,16,17,20,21,22,24,25,28,29,30,32,33,36,37,38]]    # <<<<<<<<<<<<<<<<<<<<<<<<查看df2來選所需的columns
# 儲存檔案
# report_dif_model.to_csv(filepath+'_dif_model'+'.csv')
# df2.to_csv(filepath+'_dif_model'+'.csv')

# In[3]      <<<以city/area群組分析各年度產量變化,分析Max.Min.25%.50%.75%.Mean>>>

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
report_area = report_area.groupby("area").describe()
report_area = report_area.T
# # 儲存檔案
# report_area.to_csv(filepath+'_area'+'.csv',encoding='big5')

# In[4]     <<<以city群組分析各年度產量變化>>>

# 讀取city資料
city = pd.read_csv(r'C:\Users\acer\Desktop\climate change\city.csv',encoding='big5')
# 將city資料與數據merge
city_data = pd.merge(df1,city)

file_name = filepath

p1 = sns.boxplot(x="Yield_ha_2030", y="city", data=city_data)
p1.set_xlim(-1000, 10000)
plt.savefig(file_name+"_Yield_2030.png", bbox_inches='tight',transparent=True,dpi=200)
plt.show()
plt.close()
p2 = sns.boxplot(x="Yield_ha_2040", y="city", data=city_data)
p2 = p2.set_xlim(-1000, 10000)
plt.savefig(file_name+"_Yield_2040.png", bbox_inches='tight',transparent=True,dpi=200)
plt.show()
plt.close()
p3 = sns.boxplot(x="Yield_ha_2050", y="city", data=city_data)
p3 = p3.set_xlim(-1000, 10000)
plt.savefig(file_name+"_Yield_2050.png", bbox_inches='tight',transparent=True,dpi=200)
plt.show()
plt.close()
# 取出所需的資料
report_city_yield = city_data.iloc[:,[0,17,19,20,21,22,23,25,27,28,29,30,31,33,35,36,37,38,39]]

# In[5]      <<<比較各年度產量變化>>>
'''
# style = 1, 2030>2040>2050
# style = 2, 2030>2050>2040
# style = 3, 2040>2030>2050
# style = 4, 2040>2050>2030
# style = 5, 2050>2040>2030
# style = 6, 2050>2030>2040
'''
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
# # 儲存檔案
# report_style.to_csv(filepath+'_style'+'.csv')



# In[6]     <<<繪製heatmap在不同氣候模式下>>>

# 取得lot與lat的資料長度
lot_long = set(list(report_style.iloc[:, 1]))
lot_long = sorted(lot_long, reverse = False)
lat_long = set(list(report_style.iloc[:, 2]))
lat_long = sorted(lat_long, reverse = True)
table = np.zeros((68,40))
repor_table = pd.DataFrame(table)
repor_table = pd.DataFrame(table,index=lat_long,columns=lot_long)
# 將list填入表格
# 'bcc-csm1-1' , 'camESM2' , 'CCSM4' , 'MIROC-ESM' , 'MRI-CGCM3' , 'NorESM1-M'
m = 'bcc-csm1-1'
df3 = report_style[(report_style['model']==m)]
df3.reset_index(inplace=True)
df3 = df3.drop(['index'],axis=1)
for k in range(0,930):
    [x,y] = df3.loc[k,"xy"]
    repor_table.loc[y,x] = df3.loc[k,"style"]
repor_table = pd.DataFrame(repor_table,columns=lot_long)
# 設定中文字型
plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
# 設定負號正確顯示
plt.rcParams["axes.unicode_minus"] = False
plt.figure(dpi=800)
sns.heatmap(repor_table,vmax=6, vmin=1,cmap=ListedColormap(['#ff9999','#FF0000','#00FF00','#006000', '#84C1FF', '#0000FF']),square=True,mask=(repor_table < 0.5))
plt.title(filename+"  "+m)
note = ' \n 1：2030>2040>2050     2：2030>2050>2040\n 3：2040>2030>2050     4：2040>2050>2030\n 5：2050>2040>2030     6：2050>2030>2040\n'
plt.xlabel(note,loc='left')
file_name = path + '\\'+filename+'_'+m+'.png'
# plt.savefig(file_name, bbox_inches='tight',transparent=True)



# In[7]     <<<繪製不同氣候模型下的產量變化>>>

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
plt.figure(dpi=10000)
drow_style.plot(kind='bar')
note = ' \n 1：2030>2040>2050     2：2030>2050>2040\n 3：2040>2030>2050     4：2040>2050>2030\n 5：2050>2040>2030     6：2050>2030>2040\n'
plt.xlabel(note,loc='left')


# In[8]     <<<繪製不同氣候模型下的產量Heatmap>>>

df5 = report_style

lot_long = set(list(report_style.iloc[:, 1]))
lot_long = sorted(lot_long, reverse = False)
lat_long = set(list(report_style.iloc[:, 2]))
lat_long = sorted(lat_long, reverse = True)
table = np.zeros((68,40))
repor_table_1 = pd.DataFrame(table)
repor_table_1 = pd.DataFrame(table,index=lat_long,columns=lot_long)


for m in files:
    df5 = report_style[(report_style['model']==m)]
    df5.reset_index(inplace=True)
    df5 = df5.drop(['index'],axis=1)
    Year = ['yield_2030','yield_2040','yield_2050']
    for year in Year:
        for k in range(0,930):
            [x,y] = df5.loc[k,"xy"]
            repor_table_1.loc[y,x] = df5.loc[k,year]
        repor_table_1 = pd.DataFrame(repor_table_1,columns=lot_long)
        # 設定中文字型
        plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
        # 設定負號正確顯示
        plt.rcParams["axes.unicode_minus"] = False
        plt.figure(dpi=800)
        sns.heatmap(repor_table_1,vmax=6000,vmin=1000,cmap='BrBG',xticklabels=4,square=True,mask=(repor_table_1 < 0.5))
        # sns.heatmap(repor_table_1,vmax=18000,vmin=6000,cmap='BrBG',xticklabels=4,square=True,mask=(repor_table_1 < 0.5))
        plt.title(filename+"  "+m+"  "+year)
        file_name = path + '\\'+filename+'_'+m+'_'+year+'.png'
        plt.savefig(file_name, bbox_inches='tight',transparent=True)
