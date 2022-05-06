# -*- coding: utf-8 -*-
"""
Created on Thu May  5 08:26:35 2022

@author: CCW
"""

import os
import glob
import pandas as pd


path = r'L:\Maize stage future'

season = ['1_spring','2_summer','3_fall','4_winter']

# 取得資料夾下，之子資料夾(檔名不含'.')
list_file = [f for f in os.listdir(path) if '.' not in f]
list_file.remove('__pycache__')


see = []

for i in list_file:
    n = os.path.abspath(i)
    L = []
    L.append(i)
    for j in season:
        n1 = n+'\\'+j
        num = len(os.listdir(n1))
        L.append(num)
    see.append(L)

df = pd.DataFrame(see,columns=['file','1_spring','2_summer','3_fall','4_winter'])

#%% y 資料比對彙整

# 選擇相同季節之檔案
list_all = glob.glob(r'L:\Maize stage future\*\1_spring\*')     # ['1_spring','2_summer','3_fall','4_winter']
# 檔案名包含rcp26之檔案
rcp = ["rcp26","rcp45","rcp60","rcp85"]
Year = [i for i in range(2026,2056)]


list_all_1 = [f for f in list_all if 'rcp26' in f ]
list_all_2 = [f for f in list_all_1 if str(Year[0]) in f ]

# 取hotdays
df1 = pd.read_csv(list_all_2[0],usecols = [0,1,2,6],encoding='big5')
df1.columns = ['ID','lon','lat',list_all_2[0].split('\\')[2]]
df1 = df1.fillna(-100)
# df1[df1.columns[-1]] = df1[df1.columns[-1]].replace('-99.9',-1)
# df1[df1.columns[-1]] = df1[df1.columns[-1]].replace('出土失敗',1)
# df1[df1.columns[-1]] = df1[df1.columns[-1]].replace('no emergence',1)
df3 = df1
for i in range(1,len(list_all_2)):
    
    df2 = pd.read_csv(list_all_2[i],usecols = [0,1,2,6],encoding='big5')
    df2.columns = ['ID','lon','lat',list_all_2[i].split('\\')[2]]
    df2 = df2.fillna(-100)
    df2[df2.columns[-1]] = df2[df2.columns[-1]]+0


    df3 = pd.merge(df3,df2,on=['ID','lon','lat'])
df3['sum'] = df3.iloc[:,3:].sum(axis=1)
df4 = df3.iloc[:,[0,1,2,-1]]
df4.rename(columns = {'sum':rcp[0]+'_'+str(Year[0])+'_sum'}, inplace = True)
df5 = df4

for j in range(1,len(Year)):
    
    list_all_2 = [f for f in list_all_1 if str(Year[j]) in f ]
    
    # 取hotdays
    df1 = pd.read_csv(list_all_2[0],usecols = [0,1,2,6],encoding='big5')
    df1.columns = ['ID','lon','lat',list_all_2[0].split('\\')[2]]
    df1 = df1.fillna(-100)
    # df1[df1.columns[-1]] = df1[df1.columns[-1]].replace('-99.9',-1)
    # df1[df1.columns[-1]] = df1[df1.columns[-1]].replace('出土失敗',1)
    # df1[df1.columns[-1]] = df1[df1.columns[-1]].replace('no emergence',1)
    df3 = df1
    for i in range(1,len(list_all_2)):
        
        df2 = pd.read_csv(list_all_2[i],usecols = [0,1,2,6],encoding='big5')
        df2.columns = ['ID','lon','lat',list_all_2[i].split('\\')[2]]
        df2 = df2.fillna(-100)
        df2[df2.columns[-1]] = df2[df2.columns[-1]]+0
    
    
        df3 = pd.merge(df3,df2,on=['ID','lon','lat'])
    df3['sum'] = df3.iloc[:,3:].sum(axis=1)
    df4 = df3.iloc[:,[0,1,2,-1]]
    df4.rename(columns = {'sum':rcp[0]+'_'+str(Year[j])+'_sum'}, inplace = True)
    df5 = pd.merge(df5,df4,on=['ID','lon','lat'])
    
#%% 查看單年度

rcp = 'rcp26'
year = str(2028)

list_all_1 = [f for f in list_all if 'rcp26' in f ]
list_all_2 = [f for f in list_all_1 if year in f ]

# 取hotdays
df1 = pd.read_csv(list_all_2[0],usecols = [0,1,2,6],encoding='big5')
df1.columns = ['ID','lon','lat',list_all_2[0].split('\\')[2]]
df1 = df1.fillna(-100)
# df1[df1.columns[-1]] = df1[df1.columns[-1]].replace('-99.9',-1)
# df1[df1.columns[-1]] = df1[df1.columns[-1]].replace('出土失敗',1)
# df1[df1.columns[-1]] = df1[df1.columns[-1]].replace('no emergence',1)
df3 = df1
for i in range(1,len(list_all_2)):
    
    df2 = pd.read_csv(list_all_2[i],usecols = [0,1,2,6],encoding='big5')
    df2.columns = ['ID','lon','lat',list_all_2[i].split('\\')[2]]
    df2 = df2.fillna(-100)
    df2[df2.columns[-1]] = df2[df2.columns[-1]]+0


    df3 = pd.merge(df3,df2,on=['ID','lon','lat'])
df3['sum'] = df3.iloc[:,3:].sum(axis=1)
df4 = df3.iloc[:,[0,1,2,-1]]
df4.rename(columns = {'sum':rcp[0]+'_'+year+'_sum'}, inplace = True)
