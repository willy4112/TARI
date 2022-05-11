# -*- coding: utf-8 -*-
"""
Created on Thu May  5 08:26:35 2022

@author: CCW
"""
#%% 查看資料數量
import os
import glob
import pandas as pd


path = r'F:\Maize stage future'

season = ['1_spring','2_summer','3_fall','4_winter']

# 取得資料夾下，之子資料夾(檔名不含'.')
list_file = [f for f in os.listdir(path) if '.' not in f]
list_file.remove('__pycache__')
list_file.remove('_Draw')
list_file.remove('舊程式碼')


see = []

for i in list_file:
    L = []
    L.append(i)
    for j in season:
        n1 = r'F:\Maize stage future\\'+i+'\\'+'\\'+j
        
        num = len(os.listdir(n1))
        L.append(num)
    see.append(L)

df = pd.DataFrame(see,columns=['file','1_spring','2_summer','3_fall','4_winter'])


#%% 檢查文件長度

L = []
for i in list_file:
    
    # i = list_file[3]
    for j in season:
        n1 = r'F:\Maize stage future\\'+i+'\\'+'\\'+j
        num_file = os.listdir(n1)
        for k in num_file:
            a = pd.read_csv(n1+'\\'+k,encoding='big5')
            
            num = a.shape[0]
            if num != 1418:
                L.append(n1+'\\'+k)
                print(n1+'\\'+k)




#%% 歷史資料彙整

import os
import glob
import pandas as pd

path = r'F:\Maize stage future\5 km'
season = ['1_spring','2_summer','3_fall','4_winter']

for s in season:
        
    season = s
    # season = season[1]
    list_all = glob.glob(path+'\\'+season+'\\*')
    list_all_1 = [f for f in list_all if 'HSI' in f ]
    
    # 取hotdays
    hotdays = 3
    
    df1 = pd.read_csv(list_all_1[0],usecols = [0,1,2,6],encoding='big5')
    name = list_all_1[0].split('\\')[-1]
    df1.columns = ['ID','lon','lat',name[3:7]]
    df1 = df1.fillna(-1)
    df1_1 = df1[df1.columns[-1]] > hotdays
    df1_1 = df1_1+0
    df1_2 = df1[df1.columns[-1]] < 0
    df1_2 = df1_2+0
    df1[df1.columns[-1]] = df1_2*df1[df1.columns[-1]]+df1_1
    
    df3 = df1
    for i in range(1,len(list_all_1)):
        
        df2 = pd.read_csv(list_all_1[i],usecols = [0,1,2,6],encoding='big5')
        name = list_all_1[i].split('\\')[-1]
        df2.columns = ['ID','lon','lat',name[3:7]]
        df2 = df2.fillna(-1)
        df2_1 = df2[df2.columns[-1]] > hotdays
        df2_1 = df2_1+0
        df2_2 = df2[df2.columns[-1]] < 0
        df2_2 = df2_2+0
        df2[df2.columns[-1]] = df2_2*df2[df2.columns[-1]]+df2_1
    
    
        df3 = pd.merge(df3,df2,on=['ID','lon','lat'])
    df3['sum'] = df3.iloc[:,3:].sum(axis=1)
    df3['1986-1995'] = df3.loc[:,'1986':'1995'].mean(axis=1)*100
    df3['1996-2005'] = df3.loc[:,'1996':'2005'].mean(axis=1)*100
    df3['2006-2015'] = df3.loc[:,'2006':'2015'].mean(axis=1)*100
    
    df3.to_csv(r'F:\Maize stage future\_Draw_3D'+'\\His_'+season+'.csv',index=False,encoding='utf-8')


#%% 資料比對彙整

import os
import glob
import pandas as pd

season = ['1_spring','2_summer','3_fall','4_winter']
season = season[3]

# 選擇相同季節之檔案
list_all = glob.glob(r'F:\Maize stage future\*\\'+season+'\\*')     # ['1_spring','2_summer','3_fall','4_winter']
# 檔案名包含rcp26之檔案
rcp = ["rcp26","rcp45","rcp60","rcp85"]
# rcp = ["rcp85",]
# rcp = rcp[0]

Year = [i for i in range(2026,2056)]
hotdays = 3

for k in rcp:
    rcp = k

    list_all_1 = [f for f in list_all if rcp in f ]
    list_all_2 = [f for f in list_all_1 if str(Year[0]) in f ]
    
    # 取hotdays
    df1 = pd.read_csv(list_all_2[0],usecols = [0,1,2,6],encoding='big5')
    df1.columns = ['ID','lon','lat',list_all_2[0].split('\\')[2]]
    df1 = df1.fillna(-1)
    df1_1 = df1[df1.columns[-1]] > hotdays
    df1_1 = df1_1+0
    df1_2 = df1[df1.columns[-1]] < 0
    df1_2 = df1_2+0
    df1[df1.columns[-1]] = df1_2*df1[df1.columns[-1]]+df1_1
    # df1[df1.columns[-1]] = df1[df1.columns[-1]].replace('-99.9',-1)
    # df1[df1.columns[-1]] = df1[df1.columns[-1]].replace('出土失敗',1)
    # df1[df1.columns[-1]] = df1[df1.columns[-1]].replace('no emergence',1)
    df3 = df1
    for i in range(1,len(list_all_2)):
        
        df2 = pd.read_csv(list_all_2[i],usecols = [0,1,2,6],encoding='big5')
        df2.columns = ['ID','lon','lat',list_all_2[i].split('\\')[2]]
        df2 = df2.fillna(-1)
        df2_1 = df2[df2.columns[-1]] > hotdays
        df2_1 = df2_1+0
        df2_2 = df2[df2.columns[-1]] < 0
        df2_2 = df2_2+0
        df2[df2.columns[-1]] = df2_2*df2[df2.columns[-1]]+df2_1
        df3 = pd.merge(df3,df2,on=['ID','lon','lat'])
    df3['mean'] = df3.iloc[:,3:].mean(axis=1)
    df4 = df3.iloc[:,[0,1,2,-1]]
    df4.rename(columns = {'mean':rcp+'_'+str(Year[0])+'_mean'}, inplace = True)
    df5 = df4
    
    for j in range(1,len(Year)):
        
        list_all_2 = [f for f in list_all_1 if str(Year[j]) in f ]
        
        # 取hotdays
        df1 = pd.read_csv(list_all_2[0],usecols = [0,1,2,6],encoding='big5')
        df1.columns = ['ID','lon','lat',list_all_2[0].split('\\')[2]]
        df1 = df1.fillna(-1)
        df1_1 = df1[df1.columns[-1]] > hotdays
        df1_1 = df1_1+0
        df1_2 = df1[df1.columns[-1]] < 0
        df1_2 = df1_2+0
        df1[df1.columns[-1]] = df1_2*df1[df1.columns[-1]]+df1_1
        df3 = df1
        for i in range(1,len(list_all_2)):
            
            df2 = pd.read_csv(list_all_2[i],usecols = [0,1,2,6],encoding='big5')
            df2.columns = ['ID','lon','lat',list_all_2[i].split('\\')[2]]
            df2 = df2.fillna(-1)
            df2_1 = df2[df2.columns[-1]] > hotdays
            df2_1 = df2_1+0
            df2_2 = df2[df2.columns[-1]] < 0
            df2_2 = df2_2+0
            df2[df2.columns[-1]] = df2_2*df2[df2.columns[-1]]+df2_1
        
            df3 = pd.merge(df3,df2,on=['ID','lon','lat'])
        df3['mean'] = df3.iloc[:,3:].mean(axis=1)
        df4 = df3.iloc[:,[0,1,2,-1]]
        df4.rename(columns = {'mean':rcp+'_'+str(Year[j])+'_mean'}, inplace = True)
        df5 = pd.merge(df5,df4,on=['ID','lon','lat'])
    df5['2026-2035'] = (df5.iloc[:,3:13].mean(axis=1))*100
    df5['2036-2045'] = (df5.iloc[:,13:23].mean(axis=1))*100
    df5['2046-2055'] = (df5.iloc[:,23:33].mean(axis=1))*100
    df5.to_csv(r'F:\Maize stage future\_Draw_3D'+'\\'+rcp+'_'+season+'.csv',index=False,encoding='utf-8')
    print(df5.shape)

#%% 查看單年度

import os
import glob
import pandas as pd

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

#%% 繪製Heatmap

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import glob

list_draw = glob.glob(r'F:\Maize stage future\_Draw_3D\*')

season = ['1_spring','2_summer','3_fall','4_winter']
season = season[2]
for i in range(5):
    num = i
    
    list_draw_1 = [f for f in list_draw if season in f ]
    list_draw_1 = [f for f in list_draw_1 if '.csv' in f ]
    list_draw_1.sort()
    
    
    drow_1 = pd.read_csv(list_draw_1[num])
    name = (list_draw_1[num].split('\\')[-1]).split('_')[0]
    
    drow_1 = drow_1.iloc[:,[0,1,2,-3,-2,-1]]
    
    # 擷取所要的資料
    # 取得經緯度座標，並排列整齊
    lis_lon = set(list(drow_1['lon']))
    lis_lon = sorted(lis_lon, reverse = False)
    
    lis_lat = set(list(drow_1['lat']))
    lis_lat = sorted(lis_lat, reverse = True)
    
    value_hand = list(drow_1.columns)
    
    
    # 製作放置heatmap的表格
    data = np.ones((len(lis_lat),len(lis_lon),len(value_hand)))*-1
    for i in range(drow_1.shape[0]):
        L = []
        L = drow_1.loc[i,value_hand]
        x = lis_lat.index(L['lat'])
        y = lis_lon.index(L['lon'])
        data[x,y] = list(drow_1.iloc[i])
    
    mask_drow = data[:,:,0]
    
    report_2030s = data[:,:,3]
    report_2040s = data[:,:,4]
    report_2050s = data[:,:,5]
    
    x = [i for i in range(0,len(lis_lon)+1,5)]
    y = [i for i in range(0,len(lis_lat)+1,5)]
    
    plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
    plt.rcParams["axes.unicode_minus"] = False
    plt.figure(figsize=[15,7],dpi=200)
    
    
    cbar_kws = {"ticks":[i for i in range(0,26,5)] }
    plt.subplot(131)
    sns.heatmap(report_2030s,vmin=0,vmax=25,cmap='RdYlGn_r', cbar_kws=cbar_kws,square=True,xticklabels = 5,yticklabels = 5,mask=(mask_drow < 0 ))
    plt.title(season+'   '+name+'_'+value_hand[-3]+'\n',size = 20)
    plt.xticks(x,lis_lon[::5],rotation =90)
    plt.yticks(y,lis_lat[::5],rotation =0)
    plt.xlabel('lon')
    plt.ylabel('lat')
    plt.tight_layout()
    
    
    # plt.figure(figsize=[7,5],dpi=200)
    plt.subplot(132)
    cbar_kws = {"ticks":[i for i in range(0,26,5)] }
    sns.heatmap(report_2040s,vmin=0,vmax=25,cmap='RdYlGn_r', cbar_kws=cbar_kws,square=True,xticklabels = 5,yticklabels = 5,mask=(mask_drow < 0 ))
    plt.title(season+'   '+name+'_'+value_hand[-2]+'\n',size = 20)
    plt.xticks(x,lis_lon[::5],rotation =90)
    plt.yticks(y,lis_lat[::5],rotation =0)
    plt.xlabel('lon')
    plt.ylabel('lat')
    plt.tight_layout()
    
    
    # plt.figure(figsize=[7,5],dpi=200)
    plt.subplot(133)
    cbar_kws = {"ticks":[i for i in range(0,26,5)] }
    sns.heatmap(report_2050s,vmin=0,vmax=25,cmap='RdYlGn_r', cbar_kws=cbar_kws,square=True,xticklabels = 5,yticklabels = 5,mask=(mask_drow < 0 ))
    plt.title(season+'   '+name+'_'+value_hand[-1]+'\n',size = 20)
    plt.xticks(x,lis_lon[::5],rotation =90)
    plt.yticks(y,lis_lat[::5],rotation =0)
    plt.xlabel('lon')
    plt.ylabel('lat')
    plt.tight_layout()
    
    name = list_draw_1[num].split('.')[0]
    # plt.savefig(name+'.png', bbox_inches='tight',transparent=True)


#%%  繪製Heatmap - summer

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import glob

list_draw = glob.glob(r'F:\Maize stage future\_Draw_3D\*')

season = ['1_spring','2_summer','3_fall','4_winter']
season = season[1]
for i in range(5):
    num = i
    
    list_draw_1 = [f for f in list_draw if season in f ]
    list_draw_1 = [f for f in list_draw_1 if '.csv' in f ]
    list_draw_1.sort()
    
    
    drow_1 = pd.read_csv(list_draw_1[num])
    name = (list_draw_1[num].split('\\')[-1]).split('_')[0]
    
    drow_1 = drow_1.iloc[:,[0,1,2,-3,-2,-1]]
    
    # 擷取所要的資料
    # 取得經緯度座標，並排列整齊
    lis_lon = set(list(drow_1['lon']))
    lis_lon = sorted(lis_lon, reverse = False)
    
    lis_lat = set(list(drow_1['lat']))
    lis_lat = sorted(lis_lat, reverse = True)
    
    value_hand = list(drow_1.columns)
    
    
    # 製作放置heatmap的表格
    data = np.ones((len(lis_lat),len(lis_lon),len(value_hand)))*-1
    for i in range(drow_1.shape[0]):
        L = []
        L = drow_1.loc[i,value_hand]
        x = lis_lat.index(L['lat'])
        y = lis_lon.index(L['lon'])
        data[x,y] = list(drow_1.iloc[i])
    
    mask_drow = data[:,:,0]
    
    report_2030s = data[:,:,3]
    report_2040s = data[:,:,4]
    report_2050s = data[:,:,5]
    
    x = [i for i in range(0,len(lis_lon)+1,5)]
    y = [i for i in range(0,len(lis_lat)+1,5)]
    
    plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
    plt.rcParams["axes.unicode_minus"] = False
    plt.figure(figsize=[15,7],dpi=200)
    
    
    cbar_kws = {"ticks":[i for i in range(25,101,25)] }
    plt.subplot(131)
    sns.heatmap(report_2030s,vmin=25,vmax=100,cmap='YlOrRd', cbar_kws=cbar_kws,square=True,xticklabels = 5,yticklabels = 5,mask=(mask_drow < 0 ))
    plt.title(season+'   '+name+'_'+value_hand[-3]+'\n',size = 20)
    plt.xticks(x,lis_lon[::5],rotation =90)
    plt.yticks(y,lis_lat[::5],rotation =0)
    plt.xlabel('lon')
    plt.ylabel('lat')
    plt.tight_layout()
    
    
    # plt.figure(figsize=[7,5],dpi=200)
    plt.subplot(132)
    cbar_kws = {"ticks":[i for i in range(25,101,25)] }
    sns.heatmap(report_2040s,vmin=25,vmax=100,cmap='YlOrRd', cbar_kws=cbar_kws,square=True,xticklabels = 5,yticklabels = 5,mask=(mask_drow < 0 ))
    plt.title(season+'   '+name+'_'+value_hand[-2]+'\n',size = 20)
    plt.xticks(x,lis_lon[::5],rotation =90)
    plt.yticks(y,lis_lat[::5],rotation =0)
    plt.xlabel('lon')
    plt.ylabel('lat')
    plt.tight_layout()
    
    
    # plt.figure(figsize=[7,5],dpi=200)
    plt.subplot(133)
    cbar_kws = {"ticks":[i for i in range(25,101,25)] }
    sns.heatmap(report_2050s,vmin=25,vmax=100,cmap='YlOrRd', cbar_kws=cbar_kws,square=True,xticklabels = 5,yticklabels = 5,mask=(mask_drow < 0 ))
    plt.title(season+'   '+name+'_'+value_hand[-1]+'\n',size = 20)
    plt.xticks(x,lis_lon[::5],rotation =90)
    plt.yticks(y,lis_lat[::5],rotation =0)
    plt.xlabel('lon')
    plt.ylabel('lat')
    plt.tight_layout()
    
    name = list_draw_1[num].split('.')[0]
    plt.savefig(name+'_forsummer'+'.png', bbox_inches='tight',transparent=True)
