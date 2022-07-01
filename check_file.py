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
list_file.remove('_Draw_2D')
list_file.remove('_Draw_3D')
list_file.remove('舊程式碼')
list_file.remove('_report')


see = []

for i in list_file:
    L = []
    L.append(i)
    for j in season:
        n1 = fr'F:\Maize stage future\{i}\{j}'
        
        num = len(os.listdir(n1))
        L.append(num)
    see.append(L)

df = pd.DataFrame(see,columns=['file','1_spring','2_summer','3_fall','4_winter'])


#%% 檢查文件長度

L = []
for i in list_file:
    
    # i = list_file[3]
    for j in season:
        n1 = fr'F:\Maize stage future\{i}\{j}'
        num_file = os.listdir(n1)
        for k in num_file:
            a = pd.read_csv(n1+'\\'+k,encoding='big5')
            
            num = a.shape[0]
            if num != 1418:
                L.append(n1+'\\'+k)
                print(n1+'\\'+k)

#%% 檢查0306

L = []
for i in list_file:
    n1 = fr'F:\Maize stage future\{i}\1_spring'
    num_file = os.listdir(n1)
    num_file = [f for f in num_file if '0306' in f ]
    num = len(num_file)
    L.append([i,num])
df = pd.DataFrame(L)

#%% 0306資料hotDays彙整

import os
import glob
import pandas as pd

# 行政院農業委員會資料開放平台>雜糧生產概況
# 109,全年,食用玉米
# https://data.coa.gov.tw/open_search.aspx?id=8v9pJZ858uOz

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

# =============================================================================
# 請輸入要查找的區域與年分範圍
name = 'Tainan'
list_name = list_city[name]
y_min = 2026    # 2026
y_max = 2056    # 2056
date = '0808'   # 0204, 0306
# =============================================================================

# 匯入城鎮資料
city = r'G:\臺灣歷史氣候重建資料_5公里\grid_5km_town2.csv'
df_city = pd.read_csv(city,encoding='BIG5')
# 篩選出目標地點
list_city = df_city[df_city['TOWNNAME'].isin(list_name)]
# 建立index list
number = list_city.index

# 限制季節
season ='3_fall' #1_spring
# 選擇相同季節之檔案
list_all = glob.glob(fr'G:\Maize stage future\*\{season}\*')
# 檔名包含date
list_all = [f for f in list_all if date in f ]
# 檔案名包含rcp26之檔案
rcp = ["rcp26","rcp45","rcp60","rcp85"]
# rcp = ["rcp26",]
# 建立年份清單
Year = [i for i in range(y_min,y_max)]

for k in rcp:
    rcp = k
    # 篩選RCP
    list_all_1 = [f for f in list_all if rcp in f ]
    # 篩選年分
    for j in range(0,len(Year)):
        list_all_2 = [f for f in list_all_1 if str(Year[j]) == f[-12:-8] ]
        # 取hotdays
        df1 = pd.read_csv(list_all_2[0],usecols = [0,1,2,6],encoding='big5').iloc[number,:]
        df1.columns = ['ID','lon','lat',list_all_2[0].split('\\')[2]]
        df1_1 = df1
        for i in range(1,len(list_all_2)):
            df1 = pd.read_csv(list_all_2[i],usecols = [0,1,2,6],encoding='big5').iloc[number,:]
            df1.columns = ['ID','lon','lat',list_all_2[i].split('\\')[2]]
            df1_1 = pd.concat([df1_1,df1.iloc[:,-1]],axis=1)
        # 缺值補-1
        df1_1 = df1_1.fillna(-1)
        year = Year[j]
        globals()[f'data_{year}']=df1_1
        print(f'<<<<< Analyze {rcp} {year} , done! >>>>>')
    # 將所有年份合併
    L = [globals()[f'data_{n}'] for n in Year]
    data = pd.concat(L,keys=Year)
    globals()[f'data_{rcp}']=data
    # 儲存檔案
    globals()[f'data_{rcp}'].to_csv(fr'G:\Maize stage future\_report\{name}_data_{rcp}_{date}.csv')
    
    # # =====刪除用不到的變數=====
    for i in Year:
        del globals()[f'data_{i}']
# =====刪除用不到的變數=====
del df1,df1_1,i,j,k,L,rcp,year


# def report(rcp,num1,num2):
#     # 建立熱逆境日數清單
#     L = [i for i in range(num1,num2+1)]
#     # 建立檔名
#     a = f'times_{rcp}'
#     # 連結到data
#     b = globals()[f'data_{rcp}']
#     # 建立檔名
#     c = f'table_{rcp}'
#     # 開始計算各熱逆境日數
#     for i in L:
#         hotdays = i
#         # 判定是否大於熱逆境日數
#         a = b[b.columns[3:]] > hotdays
#         # 轉換為數字
#         a = a+0
#         # 將各模式結果平均
#         a[f'times-{hotdays:02}D (%)'] = a.mean(axis=1)*100
#         # 以年分為群組平均
#         a = round(a.groupby(level=[0]).mean(),2)
#         globals()[f'times_{rcp}_{hotdays:02}'] = a[f'times-{hotdays:02}D (%)']
#     # 合併不同各熱逆境日數結果
#     L = [globals()[f'times_{rcp}_{n:02}']  for n in range(num1,num2+1)]
#     globals()[f'report_times_{rcp}'] = pd.concat(L,axis=1)
#     # 連結到f'report_times_{rcp}'
#     d = globals()[f'report_times_{rcp}']
    
#     # 判定數值>=0
#     data_mask = b >=0
#     # 將缺值得-1改為0
#     b = b*data_mask
#     # 將data以年份為群組加總
#     c = b.iloc[:,3:].groupby(level=[0]).sum()
#     # 命'sum (days)'欄為平均化年分加總結果(方法平均化)
#     c['sum (days)'] = round(c.mean(axis=1),2)
    
    
#     # 合併times宇加總資料
#     globals()[f'report_{rcp}'] = pd.concat([d,c['sum (days)']],axis=1)
    
#     # 儲存檔案
#     globals()[f'report_{rcp}'].to_csv(fr'G:\Maize stage future\_report\{name}_report_{rcp}_{date}.csv')
    
#     # =====刪除用不到的變數=====
#     for i in range(num1,num2+1):
#         del globals()[f'times_{rcp}_{i:02}']
#     del L,i
#     del globals()[f'report_times_{rcp}']

# report('rcp26',1,11)
# report('rcp45',1,11)
# report('rcp60',1,11)
# report('rcp85',1,11)


# 資料散布情況
# table_rcp26 = data_rcp26.iloc[:,3:].groupby(level=[0]).sum()
# t_sum = table_rcp26.sum(axis=1)
# t_max = table_rcp26.max(axis=1)
# t_min = table_rcp26.min(axis=1)
# t_25 = table_rcp26.quantile(.25,axis=1)
# t_50 = table_rcp26.quantile(.50,axis=1)
# t_75 = table_rcp26.quantile(.75,axis=1)
# t_all = pd.concat([t_sum,t_max,t_min,t_25,t_50,t_75],axis=1)
# t_all.columns = ['sum','man','min','25%','50%','75%']


#%% 比對0204與0306差異

import os
import glob
import pandas as pd

path = r'G:\Maize stage future\_report'
list_all = glob.glob(path+'\*')
# 檔名包含_report_
list_all = [f for f in list_all if '_report_' in f ]
# 縣市清單
list_city = ['Taoyuan','Hsinchu','Miaoli','Taichung','Changhua',
             'Yunlin','Chiayi','Tainan','Kaohsiung','Pingtung']

# # 單一縣市清單
# list_data = sorted([f for f in list_all if city in f ])

# 計算最大熱天數
def hotday(df):
    hotday_list =df.sum()
    for i in range(len(hotday_list)):
        if hotday_list[i]==0:
            hotday = (hotday_list.index[i])[6:8]
            break
    return hotday
# 整理成表格
def table(city):
    city = city
    
    name_list = []
    data_list = []
    
    for i in list_data:
        
        name = i[-14:-4]
        df = pd.read_csv(i,index_col="Unnamed: 0")
        # 計算長熱天數
        # df_table = [hotday(df),df.iloc[:11,-1].sum(),df.iloc[11:21,-1].sum(),df.iloc[21:,-1].sum()]
        df_table = df.iloc[:,-1].tolist()
        df_table.insert(0, hotday(df))
        
        name_list.append(name)
        data_list.append(df_table)
    
    # table = pd.DataFrame(data_list,index = name_list,columns = ['Max hot days','sum 2026-2035','sum 2035-2045','sum 2046-2055'],dtype=(float))
    L = [i for i in range(2026,2056)]
    L.insert(0,'Max hot days')
    table = pd.DataFrame(data_list,index = name_list,columns = L,dtype=(float))
    table = table.T
    globals()[f'{city}_table'] = table
    globals()[f'{city}_table'].to_csv(fr'G:\Maize stage future\_report\{city}_table.csv')

for c in list_city:
    list_data = sorted([f for f in list_all if c in f ])
    table(c)

#%% 全台熱逆境統整

import os
import glob
import pandas as pd


# =============================================================================
# 請輸入要查找的區域與年分範圍
# name = 'Taoyuan'
# list_name = list_city[name]
y_min = 2046    # 2026, 2036, 2046
y_max = 2056    # 2036, 2046, 2056
date = '0808'   # 0204, 0306, 0808
# 限制季節
season ='3_fall'      # 1_spring, 3_fall
# =============================================================================

# 匯入城鎮資料
city = r'G:\臺灣歷史氣候重建資料_5公里\grid_5km_town2.csv'
df_city = pd.read_csv(city,encoding='BIG5')
# # 篩選出目標地點
# list_city = df_city[df_city['TOWNNAME'].isin(list_name)]
# # 建立index list
# number = list_city.index


# 選擇相同季節之檔案
list_all = glob.glob(fr'G:\Maize stage future\*\{season}\*')
# 檔名包含date
list_all = [f for f in list_all if date in f ]
# 檔案名包含rcp26之檔案
rcp = ["rcp26","rcp45","rcp60","rcp85"]
# rcp = ["rcp26",]
# 建立年份清單
Year = [i for i in range(y_min,y_max)]

for k in rcp:
    # 篩選RCP
    list_all_1 = [f for f in list_all if k in f ]
    # 篩選年分
    for j in range(0,len(Year)):
        list_all_2 = [f for f in list_all_1 if str(Year[j]) == f[-12:-8] ]
        # 取hotdays
        df1 = pd.read_csv(list_all_2[0],usecols = [0,1,2,6],encoding='big5')
        df1.columns = ['ID','lon','lat',list_all_2[0].split('\\')[2]]
        df1_1 = df1
        for i in range(1,len(list_all_2)):
            df1 = pd.read_csv(list_all_2[i],usecols = [0,1,2,6],encoding='big5')
            df1.columns = ['ID','lon','lat',list_all_2[i].split('\\')[2]]
            df1_1 = pd.concat([df1_1,df1.iloc[:,-1]],axis=1)
        # 缺值補-1
        df1_1 = df1_1.fillna(-1)
        year = Year[j]
        globals()[f'data_{year}']=df1_1
        print(f'<<<<< Analyze {k} {year} , done! >>>>>')
    # 將所有年份合併
    L = [globals()[f'data_{n}'] for n in Year]
    data = pd.concat(L,keys=Year)
    a = data.iloc[:,3:]
    # 平均方法
    data['mean_hotdays'] = a.mean(axis=1)
    globals()[f'data_{k}']=data
    # 儲存檔案
    # globals()[f'data_{k}'].to_csv(fr'G:\Maize stage future\_report\{name}_data_{k}_{date}.csv')
    
    # # =====刪除用不到的變數=====
    for i in Year:
        del globals()[f'data_{i}']
# =====刪除用不到的變數=====
del df1,df1_1,i,j,k,L,year,a


L = [globals()[f'data_{k}']['mean_hotdays'] for k in rcp]
# 方法平均的資料來合併
table = pd.concat(L,keys=rcp,axis=1)
# 將所有年份資料平均
table = table.groupby(level=[1]).mean()
table = round(table,2)
table = pd.merge(df_city,table,left_index=True, right_index=True)

table.to_csv(fr'G:\Maize stage future\_report\hotdays_{season}{date}_{y_min}-{y_max}.csv',encoding='BIG5',index=False)
#%% 單一鄉鎮各情境年份變化表

import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
# 請輸入區
# y_min = 2046    # 2026, 2036, 2046
# y_max = 2056    # 2036, 2046, 2056
date = '0808'   # 0204, 0306, 0808
Town = {'歸仁區':[235,258],
        '安南區':[279,280,306,307,308],
        '新市區':[337]}
# town_name = '歸仁區'
Town_all = [235,258,279,280,306,307,308,337]
# =============================================================================
for n in Town:

    # 選擇相同季節之檔案
    list_all = glob.glob(r'G:\Maize stage future\_report\Tainan_data*')
    # 檔名包含date
    list_all = [f for f in list_all if date in f ]
    # 將各RCP情境的方法平均
    for i in list_all:
        df = pd.read_csv(i)
        rcp = i[-14:-9]
        df[rcp] = round(df.iloc[:,5:].mean(axis=1),2)
        df1 = df.iloc[:,[0,2,3,4,-1]]
        globals()[f'df_{rcp}'] = df1
    # 將各RCP彙整在一張表
    table = pd.concat([df_rcp26,df_rcp45['rcp45'],df_rcp60['rcp60'],df_rcp85['rcp85']],axis=1)
    
    # # 描述全部點的年份變化
    # table1 = table[table['ID'].isin(Town_all)]
    # table1 = table1.groupby(table1.iloc[:,0]).mean()
    # table1['sum'] = table1.iloc[:,4:].sum(axis=1)
    # table1_1 = table1[table1.iloc[:,0].isin([i for i in range(2026,2036)])]
    # table1_2 = table1[table1.iloc[:,0].isin([i for i in range(2036,2046)])]
    # table1_3 = table1[table1.iloc[:,0].isin([i for i in range(2046,2056)])]
    
    # 篩選目標網格點
    num = Town[n]
    table = table[table['ID'].isin(num)]
    # 以年份為單位做平均
    table = table.groupby(table.iloc[:,0]).mean()
    # 將年份設為index
    table.iloc[:,0] = table.iloc[:,0].astype('int')
    table.set_index(table.iloc[:,0],inplace=True)
    table = table.drop(columns=table.columns[0])
    # table.to_csv(fr'G:\Maize stage future\_report\{n}_{date}.csv',encoding='UTF-8')
    # 畫圖隨年份變化折線圖
    plt.rcParams["figure.dpi"] = 140

    table.iloc[:,3:].plot.bar(alpha=0.75,xlabel='year',title = [f'{n}_{date}','','',''],subplots=True, layout=(4, 1),sharex=True, legend=True)

    plt.savefig(fr'G:\Maize stage future\_report\{n}_{date}.png', bbox_inches='tight',transparent=True)

#%% 單點溫度差異圖

import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta

# Town = {'歸仁區':[235,258],
#         '安南區':[279,280,306,307,308],
#         '新市區':[337]}

# =============================================================================
# 輸入區
model = 'MIROC-ESM'
RCP = 'rcp45'
loc = 337
plant = ['0204','0306','0808']

year = 2029     # 2029, 2044, 2054
day_range = 30
# =============================================================================

for i in plant:
    
    file1 = fr'G:\Maize stage future\{model}\*\{RCP}_{year}*'
    
    list_time = [f for f in glob.glob(file1) if i in f ]
    df_time = pd.read_csv(list_time[0])
    df_time = df_time[(df_time['ID']==loc)]
    month,day = i[:2],i[2:]
    time_start = pd.to_datetime(f'{year}/{month}/{day}')
    time_end= pd.to_datetime(df_time.iloc[0,5]) + timedelta(days=day_range)
    time_flower = pd.to_datetime(df_time.iloc[0,3])
    # time_end= time_start + timedelta(days=day_range)
    
    file2 = fr'G:\TCCIP統計降尺度日資料_AR5\AR5_統計降尺度_日資料_南部_最高溫\AR5_統計降尺度_日資料_南部_最高溫_{RCP}_{model}*'
    list_model = [f for f in glob.glob(file2) if str(year) in f ]
    list_model = [f for f in list_model if f.split('_')[-2] == model]
    
    df_model = pd.read_csv(list_model[0],index_col=False)
    df_model = df_model[(df_model[' LON']==df_time.iloc[0,1])]
    df_model = df_model[(df_model[' LAT']==df_time.iloc[0,2])]
    df_model = df_model.iloc[0,2:]
    df_model.index = pd.DatetimeIndex(df_model.index)
    # df_model.index = df_model.index.strftime('%m/%d')
    df_model.index = pd.date_range('2022/1/1', '2022/12/31').strftime('%j')
    
    file3 = r'G:\臺灣歷史氣候重建資料_5公里\TReAD_日資料_南部_最高溫\TReAD_日資料_南部_最高溫_2020.csv'
    df_his = pd.read_csv(file3,index_col=False)
    df_his = df_his[(df_his['LON']==df_time.iloc[0,1])]
    df_his = df_his[(df_his['LAT']==df_time.iloc[0,2])]
    df_his = df_his.iloc[0,2:-1]
    df_his.index = pd.DatetimeIndex(df_his.index)
    # df_his.index = df_his.index.strftime('%m/%d')
    # df_his.index = df_his.index.strftime('%j')
    df_his.index = pd.date_range('2022/1/1', '2022/12/31').strftime('%j')
    
    
    df_drow = pd.concat([df_his,df_model],keys=['his','model'],axis=1)
    df_drow['dif'] = round(df_drow['model'] - df_drow['his'],2)
    df_drow.index = pd.date_range('2022/1/1', '2022/12/31').strftime('%m/%d')
    time1_1 = time_start.strftime('%m/%d')
    time1_2 = time_end.strftime('%m/%d')
    time1_3 = time_flower.strftime('%m/%d')
    
    drow = df_drow.loc[time1_1:time1_2,]
    # 畫出觀測值減平均值的圖
    plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=[6,4],dpi=200)
    colors = np.where(np.array(drow['dif']) > 0,'red','blue')
    plt.bar(drow.index,drow['dif'],color=colors)
    xaxis = [drow.index[i] for i in range(0,len(drow.index),7)]
    plt.xticks(xaxis,rotation =60)
    title_name = f'NO.{loc}    modle : {model}\n{year}與2020最高溫差異'
    plt.title(title_name)
    plt.ylabel('溫度差 (℃)')
    num_dif = round(np.sum(drow['dif']),2)
    if num_dif > 0:
        icon_temp = '多'
    else:
        icon_temp = '少'
    num_dif = abs(num_dif)
    days = (time_end-time_start).days
    plt.xlabel(f'\n觀測期間：{time1_1}-{time1_2} ({days} days)             累積差異：{icon_temp} {num_dif}℃',loc='left',size = 12)
    plt.axvline(x=time_flower.strftime('%m/%d'),ymin=0,label = f'{time1_3}')
    plt.legend(loc= 'lower right')
    plt.tight_layout()
    plt.savefig(fr'G:\Maize stage future\_report\{loc}_{model}_{RCP}_{year}_{i}.png', bbox_inches='tight',transparent=True)

#%% 單點雨量圖

import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta

# Town = {'歸仁區':[235,258],
#         '安南區':[279,280,306,307,308],
#         '新市區':[337]}

# =============================================================================
# 輸入區
model = 'MIROC-ESM'
RCP = 'rcp45'
loc = 337
plant = ['0204','0306','0506','0808','1107']

year = 2029     # 2029, 2044, 2054
day_range = 30
# =============================================================================

for i in plant:
    
    file1 = fr'G:\Maize stage future\{model}\*\{RCP}_{year}*'
    
    list_time = [f for f in glob.glob(file1) if i in f ]
    df_time = pd.read_csv(list_time[0])
    df_time = df_time[(df_time['ID']==loc)]
    month,day = i[:2],i[2:]
    time_start = pd.to_datetime(f'{year}/{month}/{day}')
    time_end= pd.to_datetime(df_time.iloc[0,5]) + timedelta(days=day_range)
    time_flower = pd.to_datetime(df_time.iloc[0,3])
    # time_end= time_start + timedelta(days=day_range)
    
    file2 = fr'G:\TCCIP統計降尺度日資料_AR5\AR5_統計降尺度_日資料_南部_降雨量\AR5_統計降尺度_日資料_南部_降雨量_{RCP}_{model}*'
    list_model = [f for f in glob.glob(file2) if str(year) in f ]
    list_model = [f for f in list_model if f.split('_')[-2] == model]
    
    df_model = pd.read_csv(list_model[0],index_col=False)
    df_model = df_model[(df_model[' LON']==df_time.iloc[0,1])]
    df_model = df_model[(df_model[' LAT']==df_time.iloc[0,2])]
    df_model = df_model.iloc[0,2:]
    df_model.index = pd.DatetimeIndex(df_model.index)
    # df_model.index = df_model.index.strftime('%m/%d')
    df_model.index = pd.date_range('2022/1/1', '2022/12/31').strftime('%j')
    
    file3 = r'G:\臺灣歷史氣候重建資料_5公里\TReAD_日資料_南部_降雨量\TReAD_日資料_南部_降雨量_2020.csv'
    df_his = pd.read_csv(file3,index_col=False)
    df_his = df_his[(df_his['LON']==df_time.iloc[0,1])]
    df_his = df_his[(df_his['LAT']==df_time.iloc[0,2])]
    df_his = df_his.iloc[0,2:-1]
    df_his.index = pd.DatetimeIndex(df_his.index)
    # df_his.index = df_his.index.strftime('%m/%d')
    # df_his.index = df_his.index.strftime('%j')
    df_his.index = pd.date_range('2022/1/1', '2022/12/31').strftime('%j')
    
    
    df_drow = pd.concat([df_his,df_model],keys=['his','model'],axis=1)
    df_drow.index = pd.date_range('2022/1/1', '2022/12/31').strftime('%m/%d')
    time1_1 = time_start.strftime('%m/%d')
    time1_2 = time_end.strftime('%m/%d')
    time1_3 = time_flower.strftime('%m/%d')
    
    drow = df_drow.loc[time1_1:time1_2,]
    # 畫出觀測值減平均值的圖
    plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=[6,4],dpi=200)
    plt.bar(drow.index,drow['model'],label = 'model')
    plt.bar(drow.index,drow['his'],alpha=0.4,color='#C8C8C8',label = 'his')
    xaxis = [drow.index[i] for i in range(0,len(drow.index),7)]
    plt.xticks(xaxis,rotation =60)
    title_name = f'NO.{loc}    modle : {model}\n{year} 與2020降雨量差異'
    plt.title(title_name)
    plt.ylabel('降雨量 (mm)')
    num_model = round(np.sum(drow['model']),2)
    num_his = round(np.sum(drow['his']),2)
    plt.xlabel(f'\n觀測期間：{time1_1}-{time1_2} ({days} days)             開花時間：{time1_3}\n累積雨量-模型(mm)： {num_model}\n累積雨量-歷史(mm)： {num_his}',loc='left',size = 12)
    plt.axvline(x=time_flower.strftime('%m/%d'),ymin=0,color = 'Red')
    plt.legend(loc= 'upper left')
    plt.tight_layout()
    # plt.savefig(fr'G:\Maize stage future\_report\{loc}_{model}_{RCP}_{year}_{i}.png', bbox_inches='tight',transparent=True)

#%% 全台熱逆境報表與視覺化
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# 行政院農業委員會資料開放平台>雜糧生產概況
# 109,全年,食用玉米
# https://data.coa.gov.tw/open_search.aspx?id=8v9pJZ858uOz

# 建立目標清單，選取前30種植面積
dict_city = {'Changhua':['芳苑鄉','大城鄉'],
             'Yunlin':['虎尾鎮','元長鄉','土庫鎮','東勢鄉','褒忠鄉','莿桐鄉','四湖鄉','口湖鄉','臺西鄉','水林鄉','林內鄉','麥寮鄉','西螺鎮'],
             'Chiayi':['六腳鄉','太保市','水上鄉','新港鄉','義竹鄉','鹿草鄉'],
             'Tainan':['安南區','安定區','歸仁區','新市區','西港區','永康區'],
             'Kaohsiung':['大寮區','永安區'],
             'Hualien':['吉安鄉','壽豐鄉']
                 }

# =============================================================================
# 請輸入要查找的區域與年分範圍
rcp = ["rcp26","rcp45","rcp60","rcp85"]
r = rcp[0]
file = r'G:\Maize stage future\_report\hotdays_3_fall0808_2026-2056.csv'
# =============================================================================

# 匯入城鎮資料
city = r'G:\臺灣歷史氣候重建資料_5公里\grid_5km_town2.csv'

df_city = pd.read_csv(city,encoding='BIG5')

table = pd.read_csv(file,encoding='BIG5')
name = file[-18:-4]
# 輸入地圖檔
# TW_map = gpd.read_file(r'F:\Basemap(GIS地圖)\TWN_COUNTY_97.shp',encoding='utf-8')
TW_map = gpd.read_file(r'C:\Users\TARI\Downloads\mapdata202203151023\COUNTY_MOI_1090820.shp',encoding='utf-8')
# 改變地圖編碼為 WGS84(epsg=4326)，經緯度系統
TW_map = TW_map.to_crs(epsg=4326)

# 建立鄉鎮清單
list_town = []
for i in list(dict_city):
    a = dict_city[i]
    for j in a:
        list_town.insert(-1,j)
del i,j

# 選出目標鄉鎮
table_1 = table[table['TOWNNAME'].isin(list_town)]
# note=1
table_11 = table_1[table_1['note']==1]
# note!= 1
table_12 = table_1[table_1['note']!=1]

report = round(table_11.iloc[:,-6:].groupby('TOWNNAME').mean(),2)
report.to_csv(fr'G:\Maize stage future\_report\TOP31_{name}.csv',encoding='BIG5')




# 將經緯度併入GIS編碼

# 設定地圖編碼
crs = {'init': 'epsg:4326'}
# 加入GIS座標
geom = [Point(xy) for xy in zip(df_city.LON, df_city.LAT)] 
geom11 = [Point(xy) for xy in zip(table_11.LON, table_11.LAT)]
geom12 = [Point(xy) for xy in zip(table_12.LON, table_12.LAT)]
gdf = gpd.GeoDataFrame(df_city, crs=crs, geometry=geom)
gdf11 = gpd.GeoDataFrame(table_11, crs=crs, geometry=geom11)
gdf12 = gpd.GeoDataFrame(table_12, crs=crs, geometry=geom12)

# 設定畫框
fig, ax = plt.subplots(1, figsize=(10, 10),dpi = 200)
# 劃出縣市邊界
TW_map.boundary.plot(color = 'Black', ax=ax,alpha=0.25)
# 畫出數據
gdf.plot(column='note', ax=ax,color='#c8c8c8',vmin = 0,marker='s',markersize=50,legend=True,alpha=0.8)

gdf11.plot(column=r, ax=ax,cmap='RdYlGn_r',vmax = 1,marker='s',markersize=50,legend=True,alpha=0.75)
gdf12.plot(column=r, ax=ax,color='black',vmin = 0,marker='x',markersize=50,legend=True,alpha=0.75,label = 'not use')


# 設定經緯度範圍
_ = ax.set_xlim([119.8, 122.2])
_ = ax.set_ylim([21.8, 25.4])

plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.rcParams["axes.unicode_minus"] = False

plt.xlabel('lon')
plt.ylabel('lat')
plt.title(f'TOP30鄉鎮-種植{name}_{r}')
plt.legend(loc='lower right')

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

#%% 繪製Heatmap fall history

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import glob

list_draw = glob.glob(r'F:\Maize stage future\_Draw\*')

season = ['1_spring','2_summer','3_fall','4_winter']
season = season[2]
# for i in range(5):
    # num = i
num = 0

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

