# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 15:50:23 2021

@author: Chai-Wei Waang
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import time


# <<<資料輸入區>>>
Input_Date = '20220523'                                                #<<<<<<<<<<<<<<<<請輸入資料起始時間>>>>>>>>>>>>>>


Year = int(Input_Date[0:4])
Montth = int(Input_Date[4:6])
Day = int(Input_Date[6:])



start_day = pd.to_datetime(Input_Date)
day = pd.date_range(start_day,periods=15,freq='D')
day = day.strftime('%Y/%m/%d')
# L = day.strftime('%Y/%m/%d %H:%M:%S')

Tmax = r'C:\Users\user_11\Downloads\soy_Tmax_35upFcst_1-15d_'+Input_Date+'.csv'    #<<<<<<<<<<<<<<<<請輸入資料>>>>>>>>>>>>>>>>>>>>>
Tmin = r'C:\Users\user_11\Downloads\soy_Tmin_17lowFcst_1-15d_'+Input_Date+'.csv'    #<<<<<<<<<<<<<<<<請輸入資料>>>>>>>>>>>>>>>>>>>>>
file_name = Input_Date                                                                  #<<<<<<<<<<<<<<<<請輸入圖片名稱>>>>>>>>>>>>>>>>>>


# start_day = str(dt.datetime(Year, Montth, Day))

# # <<<修改colums日期用>>>
# # 轉成時間元組
# struct_time = time.strptime(start_day, '%Y-%m-%d %H:%M:%S')


# # 轉成時間截
# time_stamp = int(time.mktime(struct_time))
# # 建立空list，將轉換成時間元組，轉換成字串，存入list
# day = []
# for i in range(0,15):
#     sec = i*86400+time_stamp
#     struct_time = time.localtime(sec)
#     date = time.strftime('%Y/%m/%d', struct_time)
#     day.append(date)
# # day.insert(0, 'day')



# <<<處理Tmax資料>>>
# 讀取資料，音資料長度不一致，因此分區塊讀取
df1_1 = pd.read_csv(Tmax,nrows=6)
df1_2 = pd.read_csv(Tmax,skiprows=7,nrows=6)
# 去除不要的欄位
df1_1 = df1_1.drop(['day'],axis=1)
df1_2 = df1_2.drop(['day'],axis=1)
# 利用merge來左右合併
df1 = pd.merge(df1_1,df1_2)
# 修改區域名稱
df1.iloc[0,0] = '屏東縣新園鄉'
df1.iloc[1,0] = '高雄市旗山區'
df1.iloc[2,0] = '嘉義縣鹿草鄉'
df1.iloc[3,0] = '嘉義縣六腳鄉'
df1.iloc[4,0] = '雲林縣水林鄉'
df1.iloc[5,0] = '台中市大肚區'
df1.set_index("Stn" , inplace=True)
# 改columns名稱
df1.columns=day



# <<<處理Tmin資料>>>
# 讀取資料，音資料長度不一致，因此分區塊讀取
df2_1 = pd.read_csv(Tmin,nrows=6)
df2_2 = pd.read_csv(Tmin,skiprows=7,nrows=6)
# 去除不要的欄位
df2_1 = df2_1.drop(['day'],axis=1)
df2_2 = df2_2.drop(['day'],axis=1)
# 利用merge來左右合併
df2 = pd.merge(df2_1,df2_2)
# 修改區域名稱
df2.iloc[0,0] = '屏東縣新園鄉'
df2.iloc[1,0] = '高雄市旗山區'
df2.iloc[2,0] = '嘉義縣鹿草鄉'
df2.iloc[3,0] = '嘉義縣六腳鄉'
df2.iloc[4,0] = '雲林縣水林鄉'
df2.iloc[5,0] = '台中市大肚區'
df2.set_index("Stn" , inplace=True)
# 改columns名稱
df2.columns=day



# <<<資料圖像化>>>
# 設定中文字型
plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
# 設定負號正確顯示
plt.rcParams["axes.unicode_minus"] = False
plt.figure(dpi=200)
plt.subplot(211)
cbar_kws = {"ticks":[0,1,2]}
sns.heatmap(df1,vmax=2, vmin=0,cmap='OrRd', cbar_kws=cbar_kws, linewidths=1,xticklabels = False,annot=True)
plt.ylabel('')
plt.title('<高於35度警告>')
plt.subplot(212)
sns.heatmap(df2,vmax=2, vmin=0,cmap='Blues',cbar_kws=cbar_kws,linewidths=1,annot=True)
plt.ylabel('')
plt.title('<低於17度警告>')
note = ' \n 0：發生機率低\n 1：當日或前後1日有機會發生 \n 2：當日發生可能性大'
#plt.xlabel(note,loc='left')
file_name = r'C:\Users\user_11\Downloads\\'+file_name+'.png'
plt.savefig(file_name, bbox_inches='tight',transparent=False)
