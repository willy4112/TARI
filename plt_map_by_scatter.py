# -*- coding: utf-8 -*-
"""
Created on Tue May 24 15:05:45 2022

@author: CCW
"""
#%% 用XY散佈來畫地圖

import pandas as pd
import matplotlib.pyplot as plt


file = r'F:\Maize stage future\_Draw\His_1_spring.csv'
df = pd.read_csv(file)

lis_lon = set(list(df['lon']))
lis_lon = sorted(lis_lon, reverse = False)
lis_lat = set(list(df['lat']))
lis_lat = sorted(lis_lat, reverse = True)

plt.figure(figsize=[7,8],dpi = 200)
plt.scatter(df['lon'],df['lat'],marker='s',s=25, c=df['sum'],vmin=0,cmap='RdYlGn_r')


plt.xlim(119.5, 122.5)
plt.ylim(21.5, 25.5)
plt.colorbar()

#%% 用點陣圖來畫地圖
import pandas as pd
import matplotlib.pyplot as plt


file = r'F:\Maize stage future\_Draw\His_1_spring.csv'
df = pd.read_csv(file)

lis_lon = set(list(df['lon']))
lis_lon = sorted(lis_lon, reverse = False)
lis_lat = set(list(df['lat']))
lis_lat = sorted(lis_lat, reverse = True)

# 分群
df['lable'] = pd.cut(df['sum'],[-99,-1,2,5,10],labels=['<0','0-2','3-5','6-10'])

# 取得分群list
lis_lable = set(list(df['lable']))
lis_lable = sorted(lis_lable, reverse = False)

# 將資料分類
df_1 = df[(df['lable']==lis_lable[0])]
df_2 = df[(df['lable']==lis_lable[1])]
df_3 = df[(df['lable']==lis_lable[2])]
df_4 = df[(df['lable']==lis_lable[3])]


# 請自行調整比例
plt.figure(figsize=[6,7.5],dpi = 200)

# 個別設定每一層
plt.plot(df_4['lon'],df_4['lat'],linewidth=0,marker='s',markersize = 6,label='<0',color = "#C8C8C8")
plt.plot(df_1['lon'],df_1['lat'],linewidth=0,marker='s',markersize = 6,label='0-2',color = "green")
plt.plot(df_2['lon'],df_2['lat'],linewidth=0,marker='s',markersize = 6,label='3-5',color = "orange")
plt.plot(df_3['lon'],df_3['lat'],linewidth=0,marker='s',markersize = 6,label='6-10',color = "red")

plt.xlim(119.5, 122.5)
plt.ylim(21.5, 25.5)
plt.legend(loc='lower right')
plt.xlabel('lon')
plt.ylabel('lat')
plt.title('1980-2019熱逆境天數')
plt.tight_layout()

