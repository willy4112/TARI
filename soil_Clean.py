# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 14:40:42 2021

@author: Chia-Wei Wang
"""

import pandas as pd
# import numpy as np
# import seaborn as sns
# import datetime as dt
# import time

# 讀取檔案
df = pd.read_excel(r'C:\Users\acer\Desktop\土壤物理化學分析數據.xlsx', sheet_name="soil")
# 設定篩選
df1 = df[df['match']=='y']
df2 = df1.fillna(0)
for i in range(0,547):
    # 處理BD_20 預設為1.2
    a = df2.values[i,7]
    if a == 0:
        df2.iloc[i,7] = 1.2
    # 處理OM_20 預設為1.0
    b = df2.values[i,8]
    if b == 0:
        df2.iloc[i,8] = 1.0
    # 處理砂粒_40 缺失取上一層
    c = df2.values[i,9]
    if c == 0:
        df2.iloc[i,9] = df2.iloc[i,4]
        df2.iloc[i,10] = df2.iloc[i,5]
        df2.iloc[i,11] = df2.iloc[i,6]
    # 處理BD_40 預設為1.4
    d = df2.values[i,12]
    if d == 0:
        df2.iloc[i,12] = 1.4
    # 處理OM_40 預設為1.0
    e = df2.values[i,13]
    if e == 0:
        df2.iloc[i,13] = 1.0
    # 處理處理砂粒_60 缺失取上一層
    f = df2.values[i,14]
    if f == 0:
        df2.iloc[i,14] = df2.iloc[i,9]
        df2.iloc[i,15] = df2.iloc[i,10]
        df2.iloc[i,16] = df2.iloc[i,11]
    # 處理BD_60 預設為1.6
    g = df2.values[i,17]
    if g == 0:
        df2.iloc[i,17] = 1.6
    # 處理OM_60 預設為0.5
    h = df2.values[i,18]
    if h == 0:
        df2.iloc[i,18] = 0.5
df2.to_csv('土壤物理化學分析數據.csv')
