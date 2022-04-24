# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 10:32:06 2022

@author: Chia-Wei Wang
"""

import numpy as np
import pandas as pd

#%% 將資料整理成GLYCIM格式

# GLYCIM 格式 = [Year,Month,Day,Tmax,Tmin,WS,SolRad,Precp]
# =============================================================================
# <<<填入資料位置>>>
# 
# files1：上周整理完的資料
# files2：CODiS 地區氣象站
# files3：農業氣象觀測網，農改場，補齊資料，日射量來源
# files4：中央氣象局未來氣象7日
# files5：歷史平均資料
# =============================================================================

files1 = r'C:\Users\willy\Desktop\test\高雄旗山C0V740.csv'
files2 = r'C:\Users\willy\Desktop\test\高雄旗山C0V740-2022-04.csv'
files3 = r'C:\Users\willy\Desktop\test\高雄旗山-高雄旗南72V140_item_day_20220419085539.csv'
files4 = r'C:\Users\willy\Desktop\test\未來氣象_高雄旗山.csv'
files5 = r'C:\Users\willy\Desktop\test\average\365_Chishan_20152019.csv'


# =============================================================================
# 匯入先前資料
# =============================================================================
df1 = pd.read_csv(files1)
df1.columns=['Year','Month','Day','Tmax','Tmin','WS','Precp','SolRad']
# df1[['Year','Month','Day']] = df1['Time'].str.split('/',expand=True)
# df1 = df1.drop(['Time'],axis=1)
# df1 = df1[['Year','Month','Day','Tmax','Tmin','WS','Precp','SolRad']].astype('float64')
# df1 = pd.read_csv(files1,skiprows=0,header=1,encoding='big5')
# df1.columns=['Time','Tmax','Tmin','WS','Precp','SolRad']
# df1[['Year','Month','Day']] = df1['Time'].str.split('/',expand=True)
# df1 = df1.drop(['Time'],axis=1)
# df1 = df1[['Year','Month','Day','Tmax','Tmin','WS','Precp','SolRad']].astype('float64')

# =============================================================================
# 整理網路資料，農改場有含日射量的
# =============================================================================
df3 = pd.read_csv(files3,skiprows=0,header=1,usecols=[1,2,3,4,5,6],encoding='big5')
x,y = df3.shape
# 將缺直('...')改為-999,才能將格式改為float
for i in range(x):
    for j in range(y):
        if df3.iloc[i,j] == '...':
            df3.iloc[i,j] = -999
df3.columns=['Time','Tmax','Tmin','WS','Precp','SolRad']
df3[['Year','Month','Day']] = df3['Time'].str.split('-',expand=True)
df3 = df3.drop(['Time'],axis=1)
df3 = df3[['Year','Month','Day','Tmax','Tmin','WS','Precp','SolRad']].astype('float64')

# =============================================================================
# 整理網路資料，區域資料
# =============================================================================
num_len = x
df2 = pd.read_csv(files2,skiprows=0,header=1,usecols=[0,8,10,16,21])
x,y = df2.shape
# 將缺直('...')改為-999,才能將格式改為float
for i in range(x):
    for j in range(y):
        if df2.iloc[i,j] == '...':
            df2.iloc[i,j] = -999
df2 = df2.astype('float64')
df2 = df2.iloc[0:num_len,:]
df2.columns=['Day','Tmax','Tmin','WS','Precp']

# =============================================================================
# 與先前的觀測資料合併
# =============================================================================
report_check = df3
for i in range(1,5):
    for j in range(len(df2.axes[0])):
        if df2.iloc[j,i] != -999:
            report_check.iat[j,i+2] = df2.iloc[j,i]
        else:
            # 印出有缺值(-999)的位置
            print(int(df2.iloc[j,0]),df2.columns[i])

for i in range(len(report_check.axes[0])):
    [a,b,c] = df1.iloc[-1,0:3] == report_check.iloc[i,0:3]
    if [a,b,c] == [True,True,True]:
        num_cut = i

report_cut = report_check.iloc[num_cut+1:,:]
report_now = pd.concat([df1,report_cut],axis=0)

# =============================================================================
# 整理未來氣象
# =============================================================================
df4 = pd.read_csv(files4,encoding='big5')
df4 = df4.iloc[3:5,1:].astype('float64')
Time = df4.columns.tolist()
Time = [Time[0],Time[2],Time[4],Time[6],Time[8],Time[10],Time[12]]
Tmax = []
Tmin = []

for i in range(0,14,2):
    tmax = (df4.iloc[0,i]+df4.iloc[0,i+1])/2
    Tmax.append(tmax)
    tmin = (df4.iloc[1,i]+df4.iloc[1,i+1])/2
    Tmin.append(tmin)
future = [Time,Tmax,Tmin]
df4 = pd.DataFrame(future, index = ['Time','Tmax','Tmin']).T
df4[['Month','Day']] = df4['Time'].str.split('/',expand=True)
df4 = df4.drop(['Time'],axis=1)
df4 = df4[['Month','Day','Tmax','Tmin']].astype('float64')

# =============================================================================
# 整理未來7天數據
# =============================================================================
df5 = pd.read_csv(files5)
df5 = df5[['Year','Month','Day','Tmax','Tmin','WS','Precp','SolRad']]
for i in range(len(df5.axes[0])):
    if df5.iloc[i,1] == df4.iloc[0,0] and df5.iloc[i,2] == df4.iloc[0,1]:
        start = i
    elif df5.iloc[i,1] == df4.iloc[-1,0] and df5.iloc[i,2] == df4.iloc[-1,1]:
        end = i
df5_cut = df5.iloc[start:end+1,:]
df5_cut.reset_index(inplace = True)
df5_cut = df5_cut.drop(['index'],axis=1)
for i in range(len(df4.axes[0])):
    df5_cut.at[i,'Tmax'] = df4.loc[i,'Tmax']
    df5_cut.at[i,'Tmin'] = df4.loc[i,'Tmin']

report_future = df5_cut
report_future['Year'] = report_now.iloc[-1,0]

# =============================================================================
# 合併觀測資料與未來氣象，匯出存檔
# =============================================================================
report = pd.concat([report_now,report_future],axis=0)
# 匯出檔案
# report.to_csv(files1,header=True,index=False,encoding='utf-8-sig')

# # 檢查是否相同,要放最後面才執行
# from pandas.testing import assert_frame_equal
# check = report_check.iloc[:,2:7]
# assert_frame_equal(df2,check)


#%% 觀測資料與歷史比較

import matplotlib.pyplot as plt

Time_start = '20220314'
Time_end = '20220518'
title = "高雄旗山"

Year_start = int(Time_start[0:4])
Month_start = int(Time_start[4:6])
Day_strat = int(Time_start[6:])
Year_end = int(Time_end[0:4])
Month_end = int(Time_end[4:6])
Day_end = int(Time_end[6:])

# 全部的歷史平均資料
report_history = df5.iloc[:,1:]
Temperature_his = report_history.loc[:,['Month','Day','Tmax','Tmin']]
Temperature_his['Temp'] = (Temperature_his['Tmax']+Temperature_his['Tmin'])/2
Temperature_his['Time'] = Temperature_his['Month'].astype('str')+'/'+Temperature_his['Day'].astype('str')
Temperature_his = Temperature_his.loc[:,['Time','Temp']]
Temperature_his.columns=['Time','Temp_his']

# 全部的觀測資料
Temperature_now = report_now.loc[:,['Month','Day','Tmax','Tmin']]
Temperature_now['Temp'] = (Temperature_now['Tmax']+Temperature_now['Tmin'])/2
Temperature_now['Month'] = Temperature_now['Month'].astype('int')
Temperature_now['Day'] = Temperature_now['Day'].astype('int')
Temperature_now['Time'] = Temperature_now['Month'].astype('str')+'/'+Temperature_now['Day'].astype('str')
Temperature_now = Temperature_now.loc[:,['Time','Temp']]
Temperature_now.columns=['Time','Temp_now']

# 全部的未來資料
Temperature_fut = report_future.loc[:,['Month','Day','Tmax','Tmin']]
Temperature_fut['Temp'] = (Temperature_fut['Tmax']+Temperature_fut['Tmin'])/2
Temperature_fut['Time'] = Temperature_fut['Month'].astype('str')+'/'+Temperature_fut['Day'].astype('str')
Temperature_fut = Temperature_fut.loc[:,['Time','Temp']]
Temperature_fut.columns=['Time','Temp_fut']

# 將歷史平均、現在觀測、未來氣象合併在一起
Temperature = pd.merge(Temperature_his,Temperature_now,how = 'outer')
Temperature = pd.merge(Temperature,Temperature_fut,how = 'outer')
Temperature['now-his'] = Temperature['Temp_now']-Temperature['Temp_his']


for i in range(len(Temperature.axes[0])):
    if Temperature.loc[i,'Time'] == str(str(Month_start)+'/'+str(Day_strat)):
        start = i
    elif Temperature.loc[i,'Time'] == Temperature_now.iloc[-1,0]:
        now = i
    elif Temperature.loc[i,'Time'] == Temperature_fut.iloc[-1,0]:
        fut = i
    elif Temperature.loc[i,'Time'] == str(str(Month_end)+'/'+str(Day_end)):
        end = i

Temperature['now-his_cut'] = Temperature.loc[start:now,'now-his']
Temperature['add_his'] = np.add.accumulate(Temperature.loc[start:end,'Temp_his'])
Temperature['add_now'] = np.add.accumulate(Temperature.loc[start:now,'Temp_now'])
Temperature['add_fut'] = Temperature.loc[now,'add_now'] + np.add.accumulate(Temperature.loc[now+1:end,'Temp_fut'])


# 畫出觀測值減平均值的圖
plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=[6,4],dpi=200)
colors = np.where(np.array(Temperature['now-his_cut']) > 0,'red','blue')
plt.bar(Temperature['Time'],Temperature['now-his_cut'],color=colors)
xaxis = [Temperature.loc[i,'Time'] for i in range(start,now,7)]
plt.xticks(xaxis)
title_name = '觀測值減歷史平均__'+title
plt.title(title_name)
plt.ylabel('溫度差 (℃)')
num_dif = round(abs(np.sum(Temperature['now-his_cut'])),2)
if num_dif > 0:
    icon_temp = '多'
else:
    icon_temp = '少'
plt.xlabel('\n觀測期間：'+str(Temperature.loc[start,'Time'])+'-'+str(Temperature.loc[now,'Time'])+'                累積差異： '+icon_temp+str(num_dif)+'℃',loc='left',size = 12)
plt.tight_layout()

# 畫出累積溫度圖
plt.figure(figsize=[6,4],dpi=200)
y = np.zeros(Temperature['Time'].size)
plt.plot(Temperature['Time'],Temperature['add_now'], label='現在觀測',linewidth=0,marker='o')
plt.plot(Temperature['Time'],Temperature['add_fut'], label='未來預測',linewidth=0,marker='*')
plt.fill_between(Temperature['Time'], y1 = Temperature['add_his'],y2 = y,color = '#844200',alpha = 0.5, label='歷史累積',)
xaxis = [Temperature.loc[i,'Time'] for i in range(start,end,7)]
plt.xticks(xaxis)
title_name = '累積溫度__'+title
plt.title(title_name)
plt.ylabel('累積溫度 (℃)')
num_add_his = round(Temperature.loc[fut,'add_his'],2)
num_add_fut = round(Temperature.loc[fut,'add_fut'],2)
num_add_dif = round(abs(num_add_fut-num_add_his),2)
if num_add_dif > 0:
    icon_temp_add = '多'
else:
    icon_temp_add = '少'
plt.xlabel('\n觀測期間：'+str(Temperature.loc[start,'Time'])+'-'+str(Temperature.loc[now,'Time'])+'                觀測期間：'+str(Temperature.loc[now+1,'Time'])+'-'+str(Temperature.loc[fut,'Time'])+'\n歷史累積： '+str(num_add_his)+'℃'+'            預測累積： '+str(num_add_fut)+'℃'+'            累積差異： '+icon_temp_add+str(num_add_fut)+'℃',loc='left')
plt.legend(loc = 'upper left')
plt.tight_layout()
