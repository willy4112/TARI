# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 15:44:45 2022

@author: acer
"""


import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import time


data_Hour = r'C:\Users\acer\Desktop\HourWea\G2F820_item_hour_2000to2021.csv'
df_hour = pd.read_csv(data_Hour)


plt.figure(figsize=[16,9],dpi=200)
for i in range(1,13):
    month = i
    for j in range(1,29,3):
        day = j
        
        start_day = str(dt.datetime(2010, month, day))        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<輸入日期
    
        struct_time = time.strptime(start_day, '%Y-%m-%d %H:%M:%S')
        time_stamp = int(time.mktime(struct_time))
        sec = time_stamp
        struct_time = time.localtime(sec)
        start_day = time.strftime('%Y/%m/%d', struct_time)
        df_1_4 =df_hour[df_hour.Date == start_day]
        
        
        tempH_obs = list(df_1_4['Temp'])
    
    
        # --------- make plot
        Hour = []
        tempH_lst = []
        for h in range(1,25):
            Hour.append(h)
        plt.subplot(4,3,i)
        plt.plot(Hour,tempH_obs,alpha = 0.3)
        plt.title(start_day)
        plt.tight_layout()
plt.show()
