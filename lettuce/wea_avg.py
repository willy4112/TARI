# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 15:14:57 2022

@author: CWW
"""
import pandas as pd

file = r"C:\Users\TARI\Downloads\A2K630_item_day_20221115150442.csv"

df = pd.read_csv(file,encoding = 'big5',header=1)
df = df.iloc[:,1:]
df[['Year', 'Month', 'Day']] = df['觀測時間'].str.split("/",expand=True)
df['Day'] = [i.zfill(2) for i in df['Day']]
df['Month'] = [i.zfill(2) for i in df['Month']]
df['day'] = df['Month'] + '/' + df['Day']
df = df.drop(['觀測時間', 'Year', 'Month', 'Day'], axis=1)

df = df.groupby('day').mean()
df.columns = ['Tmax', 'Tmin']

df.to_csv(r'C:\Users\TARI\Downloads\366_A2K630_2y_avg.csv',header=True,index=True,encoding='utf-8-sig')

df1 = df.drop(index='02/29', axis=0)
df1.to_csv(r'C:\Users\TARI\Downloads\365_A2K630_2y_avg.csv',header=True,index=True,encoding='utf-8-sig')
