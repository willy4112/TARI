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
TW_map = gpd.read_file(r'C:\Users\user_11\Downloads\mapdata202203151023\COUNTY_MOI_1090820.shp',encoding='utf-8')

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


# 匯入檔案
file = r'F:\Maize stage future\_Draw\His_1_spring.csv'
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
gdf_1.plot(column='sum', ax=ax,color='black',marker='x',markersize=50,legend=True,alpha=0.5)

# 設定經緯度範圍
_ = ax.set_xlim([119.8, 122.2])
_ = ax.set_ylim([21.8, 25.4])

plt.xlabel('lon')
plt.ylabel('lat')
plt.title('1980-2019熱逆境天數-spring')
plt.legend(loc='lower right')
