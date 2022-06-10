# -*- coding: utf-8 -*-
"""
Created on Fri May 13 10:04:48 2022

@author: CCW
"""
#%% 繪製GIS 地圖檔(.shp)

import geopandas as gpd
import matplotlib.pyplot as plt

# 輸入地圖檔
# TW_map = gpd.read_file(r'F:\Basemap(GIS地圖)\TWN_COUNTY_97.shp',encoding='utf-8')
TW_map = gpd.read_file(r'C:\Users\TARI\Downloads\mapdata202203151023\COUNTY_MOI_1090820.shp',encoding='utf-8')

# 如果地圖編碼非 WGS84(epsg=4326)，則須輸入原始地圖編碼 TWD97(epsg:3824)
# TW_map.crs = {'init' :'epsg:3826'}

# 改變地圖編碼為 WGS84(epsg=4326)，經緯度系統
TW_map = TW_map.to_crs(epsg=4326)

fig, ax = plt.subplots(1, figsize=(10, 10))
# 繪製邊界圖(boundary.plot)
TW_map.boundary.plot(color = 'Black', ax=ax)
# 設定邊界範圍
_ = ax.set_xlim([119.8, 122.2])
_ = ax.set_ylim([21.8, 25.4])
plt.xlabel('lon')
plt.ylabel('lat')

#%% 繪製資料

import pandas as pd 
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# 輸入地圖檔
# TW_map = gpd.read_file(r'F:\Basemap(GIS地圖)\TWN_COUNTY_97.shp',encoding='utf-8')
TW_map = gpd.read_file(r'C:\Users\TARI\Downloads\mapdata202203151023\COUNTY_MOI_1090820.shp',encoding='utf-8')
# 改變地圖編碼為 WGS84(epsg=4326)，經緯度系統
TW_map = TW_map.to_crs(epsg=4326)

# 匯入檔案
file = r'G:\Maize stage future\_Draw\His_1_spring.csv'
df = pd.read_csv(file)

# 將經緯度併入GIS編碼
geom = [Point(xy) for xy in zip(df.lon, df.lat)]
# 設定地圖編碼
crs = {'init': 'epsg:4326'}
gdf = gpd.GeoDataFrame(df, crs=crs, geometry=geom)
gdf_1 = gdf[(gdf['sum']<0)]

# 設定畫框
fig, ax = plt.subplots(1, figsize=(10, 10))
# 劃出縣市邊界
TW_map.boundary.plot(color = 'Black', ax=ax,alpha=0.25)
# 畫出數據
gdf.plot(column='sum', ax=ax,cmap='RdYlGn_r',vmin = 0,marker='s',markersize=50,legend=True,alpha=0.75)
gdf_1.plot(column='sum', ax=ax,color='black',marker='x',markersize=50,legend=True,alpha=0.5,label ='stress')

# 設定經緯度範圍
_ = ax.set_xlim([119.8, 122.2])
_ = ax.set_ylim([21.8, 25.4])

plt.xlabel('lon')
plt.ylabel('lat')
plt.title('1980-2019熱逆境天數-spring')
plt.legend(loc='lower right')

#%% 鄉鎮圈選

import pandas as pd 
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# 輸入地圖檔
# TW_map = gpd.read_file(r'F:\Basemap(GIS地圖)\TWN_COUNTY_97.shp',encoding='utf-8')
TW_map = gpd.read_file(r'C:\Users\TARI\Downloads\mapdata202203151023\COUNTY_MOI_1090820.shp',encoding='utf-8')
# 改變地圖編碼為 WGS84(epsg=4326)，經緯度系統
TW_map = TW_map.to_crs(epsg=4326)

# 建立目標清單
list_city = {'Taoyuan':['楊梅區','中壢區','平鎮區'],
             'Hsinchu':['竹北市','關西鎮','竹東鎮','橫山鄉','新豐鄉'],
             'Miaoli':['大湖鄉','通霄鎮','後龍鎮','公館鄉'],
             'Taichung':['大里區','沙鹿區','大雅區','大肚區','神岡區','豐原區','清水區','后里區'],
             'Changhua':['芳苑鄉','大城鄉','埔鹽鄉','溪州鄉','福興鄉','二林鎮','彰化市','埤頭鄉','溪湖鎮','和美鎮'],
             'Yunlin':['虎尾鎮','元長鄉','土庫鎮','東勢鄉','褒忠鄉','莿桐鄉','四湖鄉','口湖鄉','臺西鄉','水林鄉','林內鄉'],
             'Chiayi':['六腳鄉','太保市','水上鄉','新港鄉','義竹鄉','鹿草鄉'],
             'Tainan':['安南區','安定區','歸仁區','新市區','西港區','永康區','仁德區','山上區'],
             'Kaohsiung':['大寮區','永安區','美濃區','路竹區','湖內區','橋頭區','梓官區','岡山區'],
             'Pingtung':['高樹鄉','車城鄉','鹽埔鄉','新園鄉','牡丹鄉','萬丹鄉','恆春鎮']
                 }

list_name = list(list_city)

list_Taoyuan = list_city['Taoyuan']
list_Hsinchu = list_city['Hsinchu']
list_Miaoli = list_city['Miaoli']
list_Taichung = list_city['Taichung']
list_Changhua = list_city['Changhua']
list_Yunlin = list_city['Yunlin']
list_Chiayi = list_city['Chiayi']
list_Tainan = list_city['Tainan']
list_Kaohsiung = list_city['Kaohsiung']
list_Pingtung = list_city['Pingtung']

# 匯入城鎮資料
city = r'G:\臺灣歷史氣候重建資料_5公里\grid_5km_town2.csv'
df_city = pd.read_csv(city,encoding='BIG5')

# 將經緯度併入GIS編碼
geom = [Point(xy) for xy in zip(df_city.LON, df_city.LAT)] 
# 設定地圖編碼
crs = {'init': 'epsg:4326'}

gdf = gpd.GeoDataFrame(df_city, crs=crs, geometry=geom)

gdf_x = gdf[(gdf['note']<0)]

gdf01 = gdf[gdf['TOWNNAME'].isin(list_Taoyuan)]
gdf02 = gdf[gdf['TOWNNAME'].isin(list_Hsinchu)]
gdf03 = gdf[gdf['TOWNNAME'].isin(list_Miaoli)]
gdf04 = gdf[gdf['TOWNNAME'].isin(list_Taichung)]
gdf05 = gdf[gdf['TOWNNAME'].isin(list_Changhua)]
gdf06 = gdf[gdf['TOWNNAME'].isin(list_Yunlin)]
gdf07 = gdf[gdf['TOWNNAME'].isin(list_Chiayi)]
gdf08 = gdf[gdf['TOWNNAME'].isin(list_Tainan)]
gdf09 = gdf[gdf['TOWNNAME'].isin(list_Kaohsiung)]
gdf10 = gdf[gdf['TOWNNAME'].isin(list_Pingtung)]

# 設定畫框
fig, ax = plt.subplots(1, figsize=(10, 10),dpi = 200)
# 劃出縣市邊界
TW_map.boundary.plot(color = 'Black', ax=ax,alpha=0.25)
# 畫出數據
gdf.plot(column='note', ax=ax,color='#c8c8c8',vmin = 0,marker='s',markersize=50,legend=True,alpha=0.8)

gdf01.plot(column='note', ax=ax,color='#ff4c4c',marker='s',markersize=50,legend=True,alpha=0.75,label = '桃園')
gdf02.plot(column='note', ax=ax,color='#ffb74c',marker='s',markersize=50,legend=True,alpha=0.75,label = '新竹')
gdf03.plot(column='note', ax=ax,color='#dbff4c',marker='s',markersize=50,legend=True,alpha=0.75,label = '苗栗')
gdf04.plot(column='note', ax=ax,color='#70ff4c',marker='s',markersize=50,legend=True,alpha=0.75,label = '台中')
gdf05.plot(column='note', ax=ax,color='#4cff93',marker='s',markersize=50,legend=True,alpha=0.75,label = '彰化')
gdf06.plot(column='note', ax=ax,color='#4cffff',marker='s',markersize=50,legend=True,alpha=0.75,label = '雲林')
gdf07.plot(column='note', ax=ax,color='#4c93ff',marker='s',markersize=50,legend=True,alpha=0.75,label = '嘉義')
gdf08.plot(column='note', ax=ax,color='#704cff',marker='s',markersize=50,legend=True,alpha=0.75,label = '台南')
gdf09.plot(column='note', ax=ax,color='#db4cff',marker='s',markersize=50,legend=True,alpha=0.75,label = '高雄')
gdf10.plot(column='note', ax=ax,color='#ff4cb7',marker='s',markersize=50,legend=True,alpha=0.75,label = '屏東')

gdf_x.plot(column='note', ax=ax,color='black',vmin = 0,marker='x',markersize=50,legend=True,alpha=0.75,label = 'not use')

# 設定經緯度範圍
_ = ax.set_xlim([119.8, 122.2])
_ = ax.set_ylim([21.8, 25.4])

plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.rcParams["axes.unicode_minus"] = False

plt.xlabel('lon')
plt.ylabel('lat')
plt.title('選取位置')
plt.legend(loc='lower right')
