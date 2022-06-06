# -*- coding: utf-8 -*-
"""
Created on Thu May 26 15:50:50 2022

@author: CCW
"""
#%% 單點資料彙整

import glob
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
# 請輸入要查找的位置
# =============================================================================
LON = 120.75
LAT = 21.9

y_min = 1980    # 1980
y_max = 2019    # 2019

# 資料位置
path = r'C:\Users\user_11\Downloads\CZMAIZE'
# 將所有資料列表
list_all = glob.glob(path+'\\*\\*')
list_all = [f for f in list_all if 'drow' not in f]
season = ['1_spring','2_summer','3_fall','4_winter']

for s in season:
    
    list_file = [f for f in list_all if s in f]
    list_file = [f for f in list_file if int(f[-12:-8]) >=y_min and int(f[-12:-8]) <=y_max]
    
    
    # 匯入城鎮資料
    city = r'F:\臺灣歷史氣候重建資料_5公里\grid_5km_town2.csv'
    df_city = pd.read_csv(city,encoding='BIG5')
    
    number_lon = df_city.index[(df_city['LON'] == LON)].tolist()
    number_lat = df_city.index[(df_city['LAT'] == LAT)].tolist()
    number = [n for n in number_lat if n in number_lon]
    
    # 取出目標ID之資料，並合併
    data_1 = pd.concat([pd.read_csv(f).iloc[number,:] for f in list_file])
    data_1['DAS_TNG1'] = data_1['DAS_TNG1'].astype(int)
    table_1 = data_1[['DAS_TNG1','DAS_TNG7','DAS_MF3']].describe()
    table_2 = data_1[['DAS_TNG1','DAS_TNG7','DAS_MF3']].quantile([.1, .25, .5, .75, .9])
    globals()[f'data_{s}'] = data_1
    globals()[f'table1_{s}'] = table_1
    globals()[f'table2_{s}'] = table_2

kind = ['DAS_TNG1','DAS_TNG7','DAS_MF3']
plt.figure(figsize=[10,6],dpi = 200)

for k in kind:
    n = kind.index(k)
    list_drow = [data_1_spring[k],data_2_summer[k],data_3_fall[k],data_4_winter[k]]
    
    plt.subplot(1,3,n+1)
    plt.boxplot(list_drow, labels=season)
    plt.title(f"({LON},{LAT})-"+k[4:])
    plt.xticks(rotation =270)
    if n ==0:
        plt.ylabel('Days')

plt.show()

#%% 鄉鎮資料 (box plot)

import glob
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
# 行政院農業委員會資料開放平台>雜糧生產概況
# 109,全年,食用玉米
# https://data.coa.gov.tw/open_search.aspx?id=8v9pJZ858uOz
# =============================================================================

# 建立目標清單
list_city = {'Taoyuan':['楊梅區','中壢區','平鎮區'],
             'Hsinchu':['竹北市','關西鎮','竹東鎮','橫山鄉','新豐鄉'],
             'Miaoli':['大湖鄉','通霄鎮','後龍鎮','公館鄉'],
             'Taichung':['大里區','沙鹿區','大雅區','大肚區','神岡區','豐原區','清水區','后里區'],
             'Changhua':['芳苑鄉','大城鄉','埔鹽鄉','溪州鄉','福興鄉','二林鎮','彰化市','埤頭鄉','溪湖鎮','和美鎮'],
             'Yunlin':['虎尾鎮','元長鄉','土庫鎮','東勢鄉','褒忠鄉','莿桐鄉','四湖鄉','口湖鄉','臺西鄉','水林鄉','林內鄉'],
             'Chiayi':['六腳鄉','太保市','水上鄉','新港鄉','義竹鄉','鹿草鄉'],
             'Tainan':['安南區','安定區','歸仁區','新市區','西港區','永康區','仁德區','山上區']
}


list_name = list(list_city)
# =============================================================================
# 請輸入要查找的區域與年分範圍
# =============================================================================

name = 'Tainan'
list_name = list_city[name]
y_min = 1980    # 1980
y_max = 2019    # 2019



# 匯入城鎮資料
city = r'F:\臺灣歷史氣候重建資料_5公里\grid_5km_town2.csv'
df_city = pd.read_csv(city,encoding='BIG5')
# 資料位置
path = r'C:\Users\user_11\Downloads\CZMAIZE'


# 篩選出目標地點        <<<<<<<<<<篩選清單
list_city = df_city[df_city['TOWNNAME'].isin(list_name)]

# 建立index list      <<<<<<<<<<建立index，需修改
number = list_city.index

# 模擬資料
file = r'C:\Users\user_11\Downloads\CZMAIZE\1_spring\HarvestDate19800204.csv'
df = pd.read_csv(file)

# 將所有資料列表
list_all = glob.glob(path+'\\*\\*')
list_all = [f for f in list_all if 'drow' not in f]
season = ['1_spring','2_summer','3_fall','4_winter']

adversity = []

for s in season:
    
    list_file = [f for f in list_all if s in f]
    list_file = [f for f in list_file if int(f[-12:-8]) >=y_min and int(f[-12:-8]) <=y_max]
    
    data_1 = pd.concat([pd.read_csv(f).iloc[number,:] for f in list_file])


    # 篩選程目標資料
    data = data_1.loc[number,:]
    
    # cold stress
    data_cold = data[data['Sowing']=='cold stress']
    data_0 = data[data['Sowing']!='cold stress']
    
    # snowing
    data_snow = data_0[data_0['TNG1']=='snowing']
    data_1 = data_0[data_0['TNG1']!='snowing']
    
    # astype
    data_1['DAS_TNG1'] = data_1['DAS_TNG1'].astype(int)
    
    table_1 = data_1[['DAS_TNG1','DAS_TNG7','DAS_MF3']].describe()
    # table_2 = data_1[['DAS_TNG1','DAS_TNG7','DAS_MF3']].quantile([.1, .25, .5, .75, .9])
    globals()[f'data_{s}'] = data_1
    globals()[f'table1_{s}'] = table_1
    # globals()[f'table2_{s}'] = table_2
    
    num_total = data.shape[0]
    num_coldl = data_cold.shape[0]
    num_snow = data_snow.shape[0]
    
    adversity.append([s,num_total,num_coldl,num_snow])
    
    print(f'<<<<< Analyze {name} {y_min}-{y_max} {s} done! >>>>>')


table_all = pd.concat([table1_1_spring,table1_2_summer,table1_3_fall,table1_4_winter],axis=1,keys = ['spring','summer','fall','winter'],names = ['from','itom'])


df_adversity = pd.DataFrame(adversity,index = season,columns = ['season','num_total','num_coldl','num_snow'])
df_adversity = df_adversity.iloc[:,1:].T


# 繪圖
kind = ['DAS_TNG1','DAS_TNG7','DAS_MF3']

plt.figure(figsize=[12,9],dpi = 200)
for k in kind:
    n = kind.index(k)
    list_drow = [data_1_spring[k],data_2_summer[k],data_3_fall[k],data_4_winter[k]]
    plt.subplot(1,3,n+1)
    plt.boxplot(list_drow, labels=season)
    plt.title('\n'+f'{name}-'+k[4:]+f' ({y_min}-{y_max})'+'\n')
    plt.xticks(rotation =75)
    if n ==0:
        plt.ylabel('Days')
    plt.tight_layout()
    
    report = table_all.loc[:,pd.IndexSlice[:, k]]
    report = round(report,1)
    report.columns = ['1_spring','2_summer','3_fall','4_winter']
    report = pd.concat([report,df_adversity])
    
    globals()[f'report_{k}'] = report
    
plt.savefig(fr'C:\Users\user_11\Downloads\CZMAIZE\drow\{name}_{y_min}-{y_max}.png', bbox_inches='tight',transparent=False)
plt.show()

report1 = pd.concat([report_DAS_TNG1,report_DAS_TNG7,report_DAS_MF3],keys =['TNG1','TNG7','MF3'],axis=1)
data1 = pd.concat([data_1_spring,data_2_summer,data_3_fall,data_4_winter],keys =season)

data1.to_csv(fr'C:\Users\user_11\Downloads\CZMAIZE\drow\{name}_{y_min}-{y_max}-data.csv',index=True)
report1.to_csv(fr'C:\Users\user_11\Downloads\CZMAIZE\drow\{name}_{y_min}-{y_max}-table.csv')



#%% 鄉鎮資料 (box plot + table)

import glob
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
# 資料來源：新竹縣政府>縣政統計>統計年報(109年)>4.農林漁牧>4-4.農產品收穫面積及生產量

# 資料來源：https://miaoli.dgbas.gov.tw/statweb/Page/stat01_1.aspx?Mid=3009
# 農業統計	苗栗縣雜糧生產概況 (109年)

# 資料來源：桃園縣政府 主計處>業務>資訊統計>109年
# =============================================================================
# 建立目標清單          <<<<<<<<<<建立清單
list_city_hsinchu = ['竹北市','關西鎮','竹東鎮','橫山鄉','新豐鄉']
list_city_miaoli = ['大湖鄉','通霄鎮','後龍鎮','公館鄉']
list_city_taoyuan = ['楊梅區','中壢區','平鎮區']


# =============================================================================
# 請輸入要查找的年分範圍
# =============================================================================
y_min = 1980    # 1980
y_max = 2019    # 2019


# 匯入城鎮資料
city = r'F:\臺灣歷史氣候重建資料_5公里\grid_5km_town2.csv'
df_city = pd.read_csv(city,encoding='BIG5')
# 資料位置
path = r'C:\Users\user_11\Downloads\CZMAIZE'
# 目標區域
name = 'taoyuan'
list_name = list_city_taoyuan

# 篩選出目標地點        <<<<<<<<<<篩選清單
list_city = df_city[df_city['TOWNNAME'].isin(list_name)]

# 建立index list      <<<<<<<<<<建立index，需修改
number = list_city.index

# 模擬資料
file = r'C:\Users\user_11\Downloads\CZMAIZE\1_spring\HarvestDate19800204.csv'
df = pd.read_csv(file)

# 將所有資料列表
list_all = glob.glob(path+'\\*\\*')
list_all = [f for f in list_all if 'drow' not in f]
season = ['1_spring','2_summer','3_fall','4_winter']

adversity = []

for s in season:
    
    list_file = [f for f in list_all if s in f]
    list_file = [f for f in list_file if int(f[-12:-8]) >=y_min and int(f[-12:-8]) <=y_max]
    
    data_1 = pd.concat([pd.read_csv(f).iloc[number,:] for f in list_file])


    # 篩選程目標資料
    data = data_1.loc[number,:]
    
    # cold stress
    data_cold = data[data['Sowing']=='cold stress']
    data_0 = data[data['Sowing']!='cold stress']
    
    # snowing
    data_snow = data_0[data_0['TNG1']=='snowing']
    data_1 = data_0[data_0['TNG1']!='snowing']
    
    # astype
    data_1['DAS_TNG1'] = data_1['DAS_TNG1'].astype(int)
    
    table_1 = data_1[['DAS_TNG1','DAS_TNG7','DAS_MF3']].describe()
    # table_2 = data_1[['DAS_TNG1','DAS_TNG7','DAS_MF3']].quantile([.1, .25, .5, .75, .9])
    globals()[f'data_{s}'] = data_1
    globals()[f'table1_{s}'] = table_1
    # globals()[f'table2_{s}'] = table_2
    
    num_total = data.shape[0]
    num_coldl = data_cold.shape[0]
    num_snow = data_snow.shape[0]
    
    adversity.append([s,num_total,num_coldl,num_snow])
    
    print(f'<<<<< Analyze {s} done! >>>>>')


table_all = pd.concat([table1_1_spring,table1_2_summer,table1_3_fall,table1_4_winter],axis=1,keys = ['spring','summer','fall','winter'],names = ['from','itom'])


df_adversity = pd.DataFrame(adversity,index = season,columns = ['season','num_total','num_coldl','num_snow'])
df_adversity = df_adversity.iloc[:,1:].T


# 繪圖
kind = ['DAS_TNG1','DAS_TNG7','DAS_MF3']

plt.figure(figsize=[12,9],dpi = 200)
for k in kind:
    n = kind.index(k)
    list_drow = [data_1_spring[k],data_2_summer[k],data_3_fall[k],data_4_winter[k]]
    

    plt.subplot(2,3,1+n)
    plt.boxplot(list_drow, labels=season)
    plt.title('\n'+f'{name}-'+k[4:]+f' ({y_min}-{y_max})'+'\n')
    plt.xticks(rotation =270)
    plt.ylabel('Days')
    plt.tight_layout()
    
    plt.subplot(2,3,4+n)
    plt.axis('tight')
    plt.axis('off')
    
    report = table_all.loc[:,pd.IndexSlice[:, k]]
    report = round(report,1)
    report.columns = ['1_spring','2_summer','3_fall','4_winter']
    report = pd.concat([report,df_adversity])
    
    # plt.table(cellText=data,colLabels=column_labels,loc="center")
    plt.table(cellText=report.values,colLabels=report.columns,rowLabels=report.index,loc="center")
    plt.tight_layout()
plt.show()

#%% 單年單期作全台地圖


import glob
import pandas as pd
import matplotlib.pyplot as plt

season = ['1_spring','2_summer','3_fall','4_winter']
season = season[0]


file = r'C:\Users\user_11\Downloads\CZMAIZE\1_spring\HarvestDate19800204.csv'

df = pd.read_csv(file)

year = file[-12:-8]

L = df.columns

# cold stress
df_cold = df[df['Sowing']=='cold stress']
df_0 = df[df['Sowing']!='cold stress']

# snowing
df_smow = df_0[df_0['TNG1']=='snowing']
df_1 = df_0[df_0['TNG1']!='snowing']

# astype
df_1['DAS_TNG1'] = df_1['DAS_TNG1'].astype(int)

# describe()
table = df_1[['DAS_TNG1','DAS_TNG7','DAS_MF3']].describe()

# 畫圖
plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.rcParams["axes.unicode_minus"] = False
plt.figure(figsize=[19,7],dpi = 200)

# TNG1
plt.subplot(131)
plt.scatter(df_1['lon'],df_1['lat'],marker='s',s=25, c=df_1[L[5]],vmin=80,vmax=180,cmap='viridis_r')
plt.plot(df_cold['lon'],df_cold['lat'],linewidth=0,marker='x',markersize = 5,label='cold stress',color = "#888888")
plt.plot(df_smow['lon'],df_smow['lat'],linewidth=0,marker='^',markersize = 5,label='smow',color = "#000000")

plt.xlim(119.5, 122.5)
plt.ylim(21.5, 25.5)
plt.axis('equal')
plt.colorbar()
plt.legend(loc='lower right')
Vmax = table.loc['max',L[5]]
Vmin = table.loc['min',L[5]]
Vavg = round(table.loc['mean',L[5]],2)
V25 = table.loc['25%',L[5]]
V50 = table.loc['50%',L[5]]
V75 = table.loc['75%',L[5]]
note = f"max= {Vmax}    min= {Vmin}    avg.= {Vavg} \n25%={V25}    50%={V50}    75%={V75}"
plt.xlabel('lon'+'\n\n'+note)
plt.ylabel('lat')
plt.title(year+'_'+season[2:]+'-'+L[5][4:])
plt.tight_layout()

# TNG7
plt.subplot(132)
plt.scatter(df_1['lon'],df_1['lat'],marker='s',s=25, c=df_1[L[7]],vmin=80,vmax=180,cmap='magma')
plt.plot(df_cold['lon'],df_cold['lat'],linewidth=0,marker='x',markersize = 5,label='cold stress',color = "#888888")
plt.plot(df_smow['lon'],df_smow['lat'],linewidth=0,marker='^',markersize = 5,label='smow',color = "#000000")

plt.xlim(119.5, 122.5)
plt.ylim(21.5, 25.5)
plt.axis('equal')
plt.colorbar()
plt.legend(loc='lower right')
Vmax = table.loc['max',L[7]]
Vmin = table.loc['min',L[7]]
Vavg = round(table.loc['mean',L[7]],2)
V25 = table.loc['25%',L[7]]
V50 = table.loc['50%',L[7]]
V75 = table.loc['75%',L[7]]
note = f"max= {Vmax}    min= {Vmin}    avg.= {Vavg} \n25%={V25}    50%={V50}    75%={V75}"
plt.xlabel('lon'+'\n\n'+note)
plt.ylabel('lat')
plt.title(year+'_'+season[2:]+'-'+L[7][4:])
plt.tight_layout()

# MF3
plt.subplot(133)
plt.scatter(df_1['lon'],df_1['lat'],marker='s',s=25, c=df_1[L[9]],vmin=80,vmax=180,cmap='inferno')
plt.plot(df_cold['lon'],df_cold['lat'],linewidth=0,marker='x',markersize = 5,label='cold stress',color = "#888888")
plt.plot(df_smow['lon'],df_smow['lat'],linewidth=0,marker='^',markersize = 5,label='smow',color = "#000000")

plt.xlim(119.5, 122.5)
plt.ylim(21.5, 25.5)
plt.axis('equal')
plt.colorbar()
plt.legend(loc='lower right')
Vmax = table.loc['max',L[9]]
Vmin = table.loc['min',L[9]]
Vavg = round(table.loc['mean',L[9]],2)
V25 = table.loc['25%',L[9]]
V50 = table.loc['50%',L[9]]
V75 = table.loc['75%',L[9]]
note = f"max= {Vmax}    min= {Vmin}    avg.= {Vavg} \n25%={V25}    50%={V50}    75%={V75}"
plt.xlabel('lon'+'\n\n'+note)
plt.ylabel('lat')
plt.title(year+'_'+season[2:]+'-'+L[9][4:])
plt.tight_layout()


