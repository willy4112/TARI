# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 13:59:30 2021

@author: Chia-Wei Wang
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import glob


# =============================================================================
# 輸入區
# =============================================================================
path = r'L:\Corn_adversity'
season = '4_winter'       #1_spring       2_summer      3_fall     4_winter
fileList = glob.glob(str(path+'\\'+season+'\*csv'))

for i in fileList:
    filename = i.split('\\')[-1]
    save_name = i.split('.')[0]
    title_name = filename[3:-8]
    
    df = pd.read_csv(i,encoding='big5')
    df = df.fillna(-1)
    df = df.rename(columns={"TmasFS": "TmaxFS"})
    df['Grow'] = df['Startflower'] != '出土失敗'
    df['Grow'] = df['Grow']+0
    df_out = df.iloc[:,[0,1,2,11,6,7,8,9,10]]
    value_hand = list(df_out.columns)

# =============================================================================
# 運算區
# =============================================================================
    # 擷取所要的資料
    # 取得經緯度座標，並排列整齊
    lis_lon = set(list(df['lon']))
    lis_lon = sorted(lis_lon, reverse = False)
    
    lis_lat = set(list(df['lat']))
    lis_lat = sorted(lis_lat, reverse = True)
    
    # 製作放置heatmap的表格
    data = np.ones((len(lis_lat),len(lis_lon),len(value_hand)))*-1
    for i in range(df_out.shape[0]):
        L = []
        L = df.loc[i,value_hand]
        x = lis_lat.index(L['lat'])
        y = lis_lon.index(L['lon'])
        data[x,y] = list(df_out.iloc[i])
    
    mask_drow = data[:,:,0]
    
    report_Grow = data[:,:,3]
    report_hotDays = data[:,:,4]        # 0-5-10
    report_TmaxFS = data[:,:,5]         # 0-35-50
    report_HSI = data[:,:,6]            # 0-3-4
    report_FSDays = data[:,:,7]         # 0-10-15-30
    report_coldDays = data[:,:,8]       # 0-2
    
    x = [i for i in range(0,len(lis_lon)+1,5)]
    y = [i for i in range(0,len(lis_lat)+1,5)]
    
    print(title_name,max(df_out['hotDays']),max(df_out['TmaxFS']),max(df_out['HSI']),max(df_out['FSDays']),max(df_out['coldDays']))
    
    #%% Grow
    
    # 設定中文字型
    plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
    # 設定負號正確顯示
    plt.rcParams["axes.unicode_minus"] = False
    plt.figure(figsize=[7,5],dpi=200)
    
    cbar_kws = {"ticks":[0,1]}
    sns.heatmap(report_Grow, cbar_kws=cbar_kws,cmap='RdYlGn',square=True,xticklabels = 5,yticklabels = 5,mask=(mask_drow < 0 ))
    note = ' \n 1：正常出土\n 0：出土失敗'
    plt.xlabel(note,loc='left')
    plt.title(title_name+'_'+season[2:]+'_Grow')
    plt.xticks(x,lis_lon[::5],rotation =90)
    plt.yticks(y,lis_lat[::5],rotation =0)
    plt.tight_layout()
    plt.savefig(save_name+'_Grow', bbox_inches='tight',transparent=False)
    plt.clf()
    #%% hotDays
    
    # 設定中文字型
    plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
    # 設定負號正確顯示
    plt.rcParams["axes.unicode_minus"] = False
    plt.figure(figsize=[7,5],dpi=200)
    
    cbar_kws = {"ticks":[i for i in range(0,11,2)]}
    sns.heatmap(report_hotDays,vmin=-0.5,vmax=10,cmap='gist_heat_r', cbar_kws=cbar_kws,square=True,xticklabels = 5,yticklabels = 5,mask=(report_hotDays < 0 ))
    plt.title(title_name+'_'+season[2:]+'_hotDays')
    plt.xticks(x,lis_lon[::5],rotation =90)
    plt.yticks(y,lis_lat[::5],rotation =0)
    plt.tight_layout()
    plt.savefig(save_name+'_hotDays', bbox_inches='tight',transparent=False)
    plt.clf()
    
    #%% TmaxFS
    
    # 設定中文字型
    plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
    # 設定負號正確顯示
    plt.rcParams["axes.unicode_minus"] = False
    plt.figure(figsize=[7,5],dpi=200)
    
    cbar_kws = {"ticks":[i for i in range(25,51,5)]}
    sns.heatmap(report_TmaxFS,vmin=25,vmax=50,cmap='Oranges', cbar_kws=cbar_kws,square=True,xticklabels = 5,yticklabels = 5,mask=(report_TmaxFS < 0 ))
    plt.title(title_name+'_'+season[2:]+'_TmaxFS')
    plt.xticks(x,lis_lon[::5],rotation =90)
    plt.yticks(y,lis_lat[::5],rotation =0)
    plt.tight_layout()
    plt.savefig(save_name+'_TmaxFS', bbox_inches='tight',transparent=False)
    plt.clf()
    
    #%% HSI
    
    # 設定中文字型
    plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
    # 設定負號正確顯示
    plt.rcParams["axes.unicode_minus"] = False
    plt.figure(figsize=[7,5],dpi=200)
    
    cbar_kws = {"ticks":[i for i in range(0,5)]}
    sns.heatmap(report_HSI,vmin=-0.25,vmax=5,cmap='gist_heat_r', cbar_kws=cbar_kws,square=True,xticklabels = 5,yticklabels = 5,mask=(report_HSI < 0 ))
    plt.title(title_name+'_'+season[2:]+'_HSI')
    plt.xticks(x,lis_lon[::5],rotation =90)
    plt.yticks(y,lis_lat[::5],rotation =0)
    plt.tight_layout()
    plt.savefig(save_name+'_HSI', bbox_inches='tight',transparent=False)
    plt.clf()
    
    #%% FSDays
    
    # 設定中文字型
    plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
    # 設定負號正確顯示
    plt.rcParams["axes.unicode_minus"] = False
    plt.figure(figsize=[7,5],dpi=200)
    
    cbar_kws = {"ticks":[i for i in range(0,31,2)]}
    sns.heatmap(report_FSDays,vmin=-1,vmax=30, cbar_kws=cbar_kws,cmap='RdYlGn',square=True,xticklabels = 5,yticklabels = 5,mask=(report_Grow < 1 ))
    plt.title(title_name+'_'+season[2:]+'_FSDays')
    plt.xticks(x,lis_lon[::5],rotation =90)
    plt.yticks(y,lis_lat[::5],rotation =0)
    plt.tight_layout()
    plt.savefig(save_name+'_FSDays', bbox_inches='tight',transparent=False)
    plt.clf()
    #%% coldDays
    
    # 設定中文字型
    plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
    # 設定負號正確顯示
    plt.rcParams["axes.unicode_minus"] = False
    plt.figure(figsize=[7,5],dpi=200)
    
    cbar_kws = {"ticks":[i for i in range(0,3)]}
    sns.heatmap(report_coldDays,vmin=-0.5,vmax=2,cmap='Blues', cbar_kws=cbar_kws,square=True,xticklabels = 5,yticklabels = 5,mask=(report_Grow < 1 ))
    plt.title(title_name+'_'+season[2:]+'_coldDays')
    plt.xticks(x,lis_lon[::5],rotation =90)
    plt.yticks(y,lis_lat[::5],rotation =0)
    plt.tight_layout()
    plt.savefig(save_name+'_coldDays', bbox_inches='tight',transparent=False)
    plt.close('all')
