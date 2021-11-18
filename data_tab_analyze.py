# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 14:04:51 2021

@author: Chai-Wei Waang
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import time
import glob
# In[]      <<<讀取與合併.tab檔案>>>

# bcc-csm1-1    canESM2     CCSM4    MIROC-ESM    MRI-CGCM3    NorESM1-M
# KH9-spring    KH9-fall    TN10-spring    TN10-fall
# 2030    2040    2050


folder_path = glob.glob(r'L:\climate change model\to_run\bcc-csm1-1\KH9-spring\*2050\*.tab')# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<要改
folder_name = os.listdir(r'L:\climate change model\to_run\bcc-csm1-1\KH9-spring')
folder_name_1 = []
year = str(2050) # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<要改
times_1 = len(folder_name)
for i in range(times_1):
    name = folder_name[i]
    if year in name:
        folder_name_1.append(name)
    else:
        pass
times = len(folder_path)



start_day = str(dt.datetime(2040, 1, 1)) # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<要改
L1 = []
for i in range(1,366):

    struct_time = time.strptime(start_day, '%Y-%m-%d %H:%M:%S')
    time_stamp = int(time.mktime(struct_time))
    date = (i-1)*86400+time_stamp
    struct_time = time.localtime(date)
    date = time.strftime('%m/%d', struct_time)
    L1.append(date)
df_1 = np.array([L1])
df_1 = pd.DataFrame(df_1,index=['Date'])
df_1 = df_1.T
report = df_1

for n in range(times):
    path = folder_path[n]
    data_name = folder_name_1[n]
    df = pd.read_table(path,header=None)
    
    Date=[]
    Jday=[]
    R_Stage=[]
    file_name_tolist=[]
    
    (length,width) = df.shape
    for i in range(length):
        data = df.iloc[i,0]
        date = data[0:5]
        Date.append(date)
        try:
            R_stage = float(data[9:15])
        except ValueError:
            pass
        R_Stage.append(R_stage)
        grow = data[17:23]+data[24:36]+data[37:43]
        num_W = grow.count('W')
        file_name_tolist.append(num_W)
        
        name = ['Date',data_name]
        df1 = np.array([Date,file_name_tolist])
        df2 = pd.DataFrame(df1,index=name)
        df2 = df2.T
        df2[data_name] = df2[data_name].astype('int32')
    print(f'{n+1}/{times}')
    report = pd.merge(report,df2,how="right")


report.set_index("Date" , inplace=True)
# report = report.drop(['Jday'],axis=1)
report = report.T
report = report.fillna(-1)
report = report.astype('int32')


# 設定中文字型
plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
# 設定負號正確顯示
plt.rcParams["axes.unicode_minus"] = False
plt.figure(dpi=400)
sns.heatmap(report , vmin=4,cmap='Accent', mask=(report < 4))
# sns.heatmap(report , vmin=8,cmap='Accent',center=12, mask=(report < 8))
plt.title('<bcc-csm1-1_KH9-spring_2050>')   # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<要改

