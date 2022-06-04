# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 16:07:26 2021

@author: Chia-Wei Wang
"""

# import matplotlib.pyplot as plt
import pandas as pd
# import numpy as np
# import seaborn as sns
import datetime as dt
import time



# 取得日期時間，並轉換成文字
start_day = str(dt.datetime(2021, 10, 30))    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<請輸入資料起始時間>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 取出檔案名
name = start_day[0:4]+start_day[5:7]+start_day[8:10]+'00'
# 建立要轉換的地區
area = ['liujiao', 'qinan', 'shuilin', 'xinyuan']    #<<<<<<<<<<<<<<<<<<<<<<<<<<<<請輸入要轉換的地區>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 編寫絕對路徑
f1 = 'C:\\Users\\acer\\Desktop\\Tomato\\weather_FTP\\'
f1 = f1+name+"\\"+name
for a in area:
    f2 = f1+'_'+a+'.csv'
    # 讀取檔案
    data1 = pd.read_csv(f2,encoding='utf-8')
    # 轉成時間元組
    struct_time = time.strptime(start_day, '%Y-%m-%d %H:%M:%S')
    # 轉成時間截
    time_stamp = int(time.mktime(struct_time))
    # 將時間轉換成秒，以利計算
    data2 = data1['fd ']*86400+time_stamp
    # 建立空list，將轉換成時間元組，轉換成字串，存入list
    data3 = []
    for i in range(0,45):
        struct_time = time.localtime(data2[i])
        date = time.strftime('%Y/%m/%d %H:%M:%S', struct_time)
        data3.append(date)
    # 轉成DataFrame，分離資料，移除不需要的資料
    data3 = pd.DataFrame(data3,columns=['datetime'])
    data3[['date','hour']] = data3['datetime'].str.split(' ',expand=True)
    data3 = pd.concat([data3,data1],axis=1)
    data3 = data3.drop(['datetime','hour','fd '],axis=1)
    # 將所需資料讀成list
    data4 = data3['date']
    data4_1 = []
    data4_2 = []
    data4_3 = []
    for i in range(0, 45):
        for j in range(0, 24):
            day = data4[i]
            Temp = data3.values[i,j+1]
            data4_1.append(day)
            data4_2.append(j)
            data4_3.append(Temp)
    # 將list改變為DataFrame
    data4_1 = pd.DataFrame(data4_1,columns=['date'])
    data4_2 = pd.DataFrame(data4_2,columns=['Hour'])
    data4_3 = pd.DataFrame(data4_3,columns=['Temperature'])
    # 合併全部資料
    data5 = pd.concat([data4_1,data4_2,data4_3],axis=1)
    # 分析資料
    data6 = data5.groupby('date')['Temperature'].agg(['max','min','mean'])
    # 匯出成cxv檔
    data6.to_csv(r'C:\Users\acer\Desktop\Tomato\weather_FTP\45D_'+a+'.csv',encoding='utf-8-sig')
