# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 08:03:35 2021
@author: Chai-Wei Waang
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import time


# In[]      <<<將.tab轉換與整理成csv>>>

# 採用讀取文字位置的方式
file = 'bcc-csm1-1_changeH2Otime'
point = '1032'
year = '2050'
read_site = r'L:\\climate change model\\to_run\\'+file+'\\'+'TN10-spring\\spring_'+point+'_chishan_'+year+'\\'+'spring_'+point+'_chishan.tab'
save_site = r'D:\我的雲端硬碟\work\3.TARI\climate change\\TN10_spring_'+point+'_'+year+'_'+file+'.csv'

df = pd.read_table(read_site,header=None)

Date=[]
Jday=[]
R_Stage=[]
W=[]
C=[]
N=[]

# 取得字串中所需要的資料，並存成list
(length,width) = df.shape
for i in range(length):
    data = df.iloc[i,0]
    date = data[0:5]
    Date.append(date)
    jday = data[6:9]
    Jday.append(jday)
    try:
        R_stage = float(data[9:15])
    except ValueError:
        pass
    R_Stage.append(R_stage)
    grow = data[17:23]+data[24:36]+data[37:43]
    num_W = grow.count('W')
    W.append(num_W)
    num_C = grow.count('C')
    C.append(num_C)
    num_N = grow.count('N')
    N.append(num_N)

# 將list合併成DataFrame
name = ['Date','Jday','R_Stage','W','C','N']
df1 = np.array([Date,Jday,R_Stage,W,C,N])
df1 = df1.T
df2 = pd.DataFrame(df1,columns=name)
df2['Jday'] = df2['Jday'].astype('int32')
df2['R_Stage'] = df2['R_Stage'].astype('float32')
df2['W'] = df2['W'].astype('int32')
# 儲存檔案
df2.to_csv(save_site)



# In[]      <<<讀取與合併.tab檔案>>>
folder_name = os.listdir(r'C:\Users\acer\Desktop\GLYCIM\Run\20211115-1')
# folder_name = ['Chishan_0928','Chishan_1001']

# 建立mm/dd的時間與Jday
L = []
start_day = str(dt.datetime(2021, 1, 1))
L1 = []
for i in range(1,366):
    jday = i
    L.append(jday)
    struct_time = time.strptime(start_day, '%Y-%m-%d %H:%M:%S')
    time_stamp = int(time.mktime(struct_time))
    date = (i-1)*86400+time_stamp
    struct_time = time.localtime(date)
    date = time.strftime('%m/%d', struct_time)
    L1.append(date)
# 將mm/dd與Jday的list存成DataFrame
df_1 = np.array([L1,L])
df_1 = pd.DataFrame(df_1,index=['Date','Jday'])
# 轉置
df_1 = df_1.T
report = df_1
report_w = df_1
# 讀取檔案中的.tab
for f in folder_name:
    file_name = f
    file_name_tolist = f
    path = 'C:\\Users\\acer\\Desktop\\GLYCIM\\Run\\20211115-1\\'+file_name+'\\'+file_name+'.tab'
    df = pd.read_table(path,header=None)
    
    Date=[]
    Jday=[]
    R_Stage=[]
    file_name_tolist=[]
    
    # 
    (length,width) = df.shape
    for i in range(length):
        data = df.iloc[i,0]
        date = data[0:5]
        Date.append(date)
        try:
            R_stage = float(data[9:15])
        except ValueError:
            pass
        # R_stage = float(data[9:15])
        R_Stage.append(R_stage)
        grow = data[17:23]+data[24:36]+data[37:43]
        num_W = grow.count('W')
        file_name_tolist.append(num_W)
        
        name = ['Date','R_'+file_name,file_name]
        name1 = ['Date',file_name]
        df1 = np.array([Date,R_Stage,file_name_tolist])
        df1_1 = np.array([Date,file_name_tolist])
        df2 = pd.DataFrame(df1,index=name)
        df2_1 = pd.DataFrame(df1_1,index=name1)
        df2 = df2.T
        df2_1 = df2_1.T
        # df2['Jday'] = df2['Jday'].astype('int32')
        df2['R_'+file_name] = df2['R_'+file_name].astype('float32')
        df2[file_name] = df2[file_name].astype('int32')
    print(f)
    report = pd.merge(report,df2,how="left")
    report_w = pd.merge(report_w, df2_1,how='right')



# In[]      <<<繪製heatmap>>>

report_w.set_index("Date" , inplace=True)
report_w = report_w.drop(['Jday'],axis=1)
report_w = report_w.T
report_w = report_w.fillna(-1)
report_w = report_w.astype('int32')


# 設定中文字型
plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
# 設定負號正確顯示
plt.rcParams["axes.unicode_minus"] = False
sns.heatmap(report_w ,yticklabels=1, vmin=3,cmap='Accent', mask=(report_w < 3))
# sns.heatmap(report_w ,vmax=10, vmin=1,cmap='Set1',xticklabels=30, mask=(report_w < 0))
