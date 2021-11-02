# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 08:04:29 2021

@author: Chia-Wei Wang
"""

import pandas as pd
# import numpy as np
# import seaborn as sns
# import datetime as dt
# import time



# 將不同區域的日射量資料合併
# for n in range(1980,2021):
#     files = [r"L:\臺灣歷史氣候重建資料_5公里\TReAD_日資料_北部_日射量\TReAD_日資料_北部_日射量_"+str(n)+".csv",
#               r"L:\臺灣歷史氣候重建資料_5公里\TReAD_日資料_中部_日射量\TReAD_日資料_中部_日射量_"+str(n)+".csv",
#               r"L:\臺灣歷史氣候重建資料_5公里\TReAD_日資料_南部_日射量\TReAD_日資料_南部_日射量_"+str(n)+".csv",
#               r"L:\臺灣歷史氣候重建資料_5公里\TReAD_日資料_東部_日射量\TReAD_日資料_東部_日射量_"+str(n)+".csv"]
#     df = pd.concat([pd.read_csv(f) for f in files])
#     df = df.T
#     df.reset_index(inplace=True)
#     df.to_csv(r"L:\臺灣歷史氣候重建資料_5公里\TReAD_日射量_"+str(n)+".csv",header=False,index=False,encoding='utf-8-sig')



# 合併不同地區資料並將日期分離
for n in range(1980,2021):
    # files = [r"L:\臺灣歷史氣候重建資料_5公里\TReAD_日資料_北部_平均風速\TReAD_日資料_北部_平均風速_"+str(n)+".csv",
    #           r"L:\臺灣歷史氣候重建資料_5公里\TReAD_日資料_中部_平均風速\TReAD_日資料_中部_平均風速_"+str(n)+".csv",
    #           r"L:\臺灣歷史氣候重建資料_5公里\TReAD_日資料_南部_平均風速\TReAD_日資料_南部_平均風速_"+str(n)+".csv",
    #           r"L:\臺灣歷史氣候重建資料_5公里\TReAD_日資料_東部_平均風速\TReAD_日資料_東部_平均風速_"+str(n)+".csv"]
    files = [r"L:\臺灣歷史氣候重建資料_5公里\TReAD_日資料_北部_日射量\TReAD_日資料_北部_日射量_"+str(n)+".csv",
             r"L:\臺灣歷史氣候重建資料_5公里\TReAD_日資料_中部_日射量\TReAD_日資料_中部_日射量_"+str(n)+".csv",
             r"L:\臺灣歷史氣候重建資料_5公里\TReAD_日資料_南部_日射量\TReAD_日資料_南部_日射量_"+str(n)+".csv",
             r"L:\臺灣歷史氣候重建資料_5公里\TReAD_日資料_東部_日射量\TReAD_日資料_東部_日射量_"+str(n)+".csv"]
    df = pd.concat([pd.read_csv(f) for f in files])
    # 轉置
    df = df.T
    df.reset_index(inplace=True)
    # 取出index來處理日期
    L = list(df['index'])
    # 建立list
    L1=[]
    # 計算list長度
    num = len(L)
    # 將日期轉換成mm/dd
    for i in range(0,num):
        a = L[i]
        mm = a[4:6]
        dd = a[6:8]
        L1.append(mm+'/'+dd)
    # 將list存成DataFrame
    df_2= pd.DataFrame(L1,columns=['date'])
    # 將數值改成所需的值
    df_2.iloc[0,0] = 'LON'
    df_2.iloc[1,0] = 'LAT'
    # 合併資料
    df_3 = pd.concat([df_2,df],axis=1)
    # 移除多於資料
    df_3 = df_3.drop([i],axis=0)
    df_3 = df_3.drop(['index'],axis=1)
    # 儲存資料
    # df_3.to_csv(r"L:\臺灣歷史氣候重建資料_5公里\TReAD_平均風速_"+str(n)+".csv",header=True,index=False,encoding='utf-8-sig')
    df_3.to_csv(r"L:\臺灣歷史氣候重建資料_5公里\TReAD_日射量_"+str(n)+".csv",header=True,index=False,encoding='utf-8-sig')





# 將不同年份平均化
files1 = []
for m in range(1980,2021):
    # site = r"L:\臺灣歷史氣候重建資料_5公里\TReAD_平均風速_"+str(m)+".csv"
    site = r"L:\臺灣歷史氣候重建資料_5公里\TReAD_日射量_"+str(m)+".csv"
    files1.append(site)
    df_4 = pd.concat([pd.read_csv(f1) for f1 in files1],ignore_index=True)
    df_5 = df_4.groupby('date').mean()
    df_5 = df_5.reset_index()
    df_6 = df_5.drop(df_5.index[0:366],axis=0)
    df_6 = df_6.sort_values(by='date',ascending=False)
    df_7 = df_5.drop(df_5.index[366:368],axis=0)
    df_8 = pd.concat([df_6,df_7],ignore_index=True)
    df_8 = df_8.T
    df_8.reset_index(inplace=True)
    df_8 = df_8.drop(['index'],axis=1)
# df_8.to_csv(r"L:\臺灣歷史氣候重建資料_5公里\TReAD_平均風速_all.csv",header=True,index=False,encoding='utf-8-sig')
df_8.to_csv(r"L:\臺灣歷史氣候重建資料_5公里\TReAD_日射量_all.csv",header=True,index=False,encoding='utf-8-sig')
# df_123 = pd.read_csv(r"L:\臺灣歷史氣候重建資料_5公里\TReAD_平均風速\TReAD_平均風速_all.csv")





# df_4.reset_index(inplace=True)
# df_4 = df_4.groupby('date').mean()
# df_4 = df_4.drop(df_4.columns[1],axis=1)
# df_4 = df_4.T
# df_4.reset_index(inplace=True)
# df_4.to_csv(r"L:\臺灣歷史氣候重建資料_5公里\TReAD_平均風速__1980-1990.csv",header=True,index=False,encoding='utf-8-sig')




# r"L:\臺灣歷史氣候重建資料_5公里\TReAD_日射量\TReAD_日射量_all_1980-1990_r.csv.csv"
# r"L:\臺灣歷史氣候重建資料_5公里\TReAD_日射量\TReAD_日射量_all_1991-2000_r.csv"
# r"L:\臺灣歷史氣候重建資料_5公里\TReAD_日射量\TReAD_日射量_all_2001-2010_r.csv"
# r"L:\臺灣歷史氣候重建資料_5公里\TReAD_日射量\TReAD_日射量_all_2011-2020_r.csv"
# r"L:\臺灣歷史氣候重建資料_5公里\TReAD_日射量\TReAD_日射量_all_r.csv"


# df_1 = pd.read_csv(r"L:\臺灣歷史氣候重建資料_5公里\TReAD_平均風速\R_TReAD_平均風速_all.csv",encoding='utf-8')
# df_1 = df_1.drop(df_1.columns[1],axis=1)
# df_1 = df_1.T
# df_1.reset_index(inplace=True)
# df_1.to_csv(r"L:\臺灣歷史氣候重建資料_5公里\TReAD_平均風速\TReAD_平均風速_all.csv",header=False,index=False,encoding='utf-8-sig')


