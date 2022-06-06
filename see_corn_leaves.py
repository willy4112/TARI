# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 16:27:28 2022

@author: CCW
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

file = r'C:\Users\user_11\Downloads\玉米葉片生長紀錄.xlsx'
df = pd.read_excel(file)
df['NO'] = df['NO'].astype(str)

# 
no = set(df['NO'])
no = sorted(no, reverse = False)

# 測試用控制迴圈
# no = no[0]

for i in no:
        
    num_no = i
    
    df_1 = df[(df['NO']==num_no)]
    # 缺值補滿
    df_1 = df_1.fillna(-1)
    x,y = df_1.shape
    # 將文字替換成數字，以利分析計算
    for i in range(x):
        for j in range(y):
            if df_1.iloc[i,j]=='X':
                df_1.iloc[i,j]=2
            elif df_1.iloc[i,j]=='O':
                df_1.iloc[i,j]=1
            elif df_1.iloc[i,j]=='V':
                df_1.iloc[i,j]=0
            else:
                pass
    df_1.iloc[:,2:] = df_1.iloc[:,2:].astype(int)
    df_1.index = df_1['紀錄日期'].dt.date
    # 刪除不需要的欄位
    df_1 = df_1.drop(['紀錄日期'],axis=1)
    df_1 = df_1.drop(['NO'],axis=1)
    # L = [i for i in range(30,0,-1)]
    # df_1 = df_1[L]
    df_1 = df_1.T
    
    # 設定color bar 格式
    cbar_kws = {"ticks":[0,1,2]}
    # 設定x-axis格式
    # 取得x標記
    xticks = list(df_1.columns)
    # 判定間格
    if len(xticks)>20:
        gap_x = 3
    elif len(xticks)>5:
        gap_x = 2
    else:
        gap_x = 1
    # 取得x位置
    x = np.arange(0,len(xticks),gap_x)
    
    
    # 畫圖
    plt.figure(dpi = 200)
    plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
    plt.rcParams['axes.unicode_minus'] = False
    
    sns.heatmap(df_1,vmin=0,vmax=2,cmap='RdYlGn_r',cbar_kws=cbar_kws,linewidths = 0.1,square=True,mask=(df_1 < 0 ))
    plt.xticks(x+0.5,xticks[::gap_x])
    plt.ylim(0,30)
    plt.ylabel('葉序')
    plt.title(f'NO. {num_no}')

