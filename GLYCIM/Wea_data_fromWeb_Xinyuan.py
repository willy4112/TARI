# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 14:51:12 2022

@author: Chia-Wei Wang
"""
#%% Step1. CODIS資料_C0R560_新園

# from bs4 import BeautifulSoup
# import numpy as np
# import pandas as pd
# import requests


import pandas as pd
import requests

# =============================================================================
# 設定起始與結束時間
t1 = '2022-01-01'
t2 = '2022-12-27'   # 當天。
# =============================================================================

# 東港專用URL
url = f'https://agr.cwb.gov.tw/NAGR/history/station_day/create_report?station=C0R560&start_time={t1}&end_time={t2}&items=TxMaxAbs,TxMinAbs,WS,Precp&report_type=csv_time&level=%e8%87%aa%e5%8b%95%e7%ab%99'
r = requests.get(url)

# 將資料取出並排列成list
raw = r.text
raw = list(map(lambda x: x.split(','),raw.split("\r\n")))

# 將資料轉換成DataFrame
df = pd.DataFrame(raw[2:-1])
df = df.iloc[:-1,1:6]
df.columns = ['date', 'Tmax', 'Tmin', 'WS', 'Precp']
df[['Year','Month','Day']] = df['date'].str.split("-",expand=True)
df = df.drop(['date'],axis=1)
data_n = df.copy()


#%% Step2. 農業氣象觀測網監測系統_72V140

import pandas as pd
import requests

# =============================================================================
# # 設定起始與結束時間
t1 = '2022-01-01'
t2 = '2022-12-26'   # 建議比當下時間少1-2天，至少要少1天。
# =============================================================================

# 東港專用URL
url = f'https://agr.cwb.gov.tw/NAGR/history/station_day/create_report?station=12Q970&start_time={t1}&end_time={t2}&items=TxMaxAbs,TxMinAbs,WS,Precp,GloblRad&report_type=csv_time&level=%E6%96%B0%E8%BE%B2%E6%A5%AD%E7%AB%99'
r = requests.get(url)

# 將資料取出並排列成list
raw = r.text
raw = list(map(lambda x: x.split(','),raw.split("\r\n")))

# 將資料轉換成DataFrame
df = pd.DataFrame(raw[2:-1])
df = df.iloc[:,1:7]
df.columns = ['date', 'Tmax', 'Tmin', 'WS', 'Precp', 'SolRad']

# 轉換資料型態為float
df[['Tmax', 'Tmin', 'WS', 'Precp', 'SolRad']] = df[['Tmax', 'Tmin', 'WS', 'Precp', 'SolRad']].astype(float)


#%% Step3. 將缺值補上

# data 資料，由CODIS抓取，容易有缺值，且無日射量。
# df 資料，由農業氣象觀測網監測系統抓取，較為詳細的資料。

# 利用以之時間的df來裁切多餘的data
# data = data.iloc[:df.shape[0],:]

# 檢查缺失值
lost = data_n.loc[(data_n['Tmax'] == '') | (data_n['Tmin'] == '') | (data_n['WS'] == '') | (data_n['Precp'] == '')]

# 取出有缺漏的index
L = lost.index

# 將df資料取代data中有缺值的部分
item = ['Tmax', 'Tmin', 'WS', 'Precp']
for i in item:
    for j in L:
        if data_n.loc[j,i] == '':
            data_n.loc[j,i] = df.loc[j,i]

# 加入日射量資料
data_n['SolRad'] = df['SolRad']

# 重新排列資料順序
data_n = data_n[['Year', 'Month', 'Day', 'Tmax', 'Tmin', 'WS', 'SolRad', 'Precp']]

# 改變資料型態為float
data_n[['Tmax', 'Tmin', 'WS', 'Precp', 'SolRad']] = data_n[['Tmax', 'Tmin', 'WS', 'Precp', 'SolRad']].astype(float)


#%% Step 4. 抓取未來一周資料

from bs4 import BeautifulSoup
import pandas as pd
import requests

t3 = 2022122607-1
year = 2022
num_year_days = 365
avg = r'G:\GLYCIM\Weather\average\365_Xinyuan_20152019.csv'

headers = {"Content-Type": "text/html; charset=UTF-8"}
url = f'https://www.cwb.gov.tw/V8/C/W/Town/MOD/Week/1001317_Week_PC.html?T={t3}'

# 發送 Requests
res_f = requests.post(url, headers=headers).content

# 解析網頁
soup = BeautifulSoup(res_f, 'html.parser')

# 取得資料
# table = soup.find_all('tr')
raw_data = [
    [i.text.strip() for i in item.find_all('td')] 
    for item in soup.find_all('tr')
]
raw_titel = [
    [i.text.strip() for i in item.find_all('th')] 
    for item in soup.find_all('tr')
]
data_f = [raw_titel[i] + raw_data[i] for i in range(len(raw_titel))]


# def add_item(num):
#     L1 = data_f[num]
#     L1_n = []
#     for i in range(len(L1)):
#         j = L1[i]
#         L1_n.append(j)
#         if i > 0:
#             L1_n.append(j)
#     return L1_n

# data_f[0] = add_item(0)
# data_f[12] = add_item(12)


def average(num):
    
    L = raw_data[num]
    L_n = []
    for i in range(7):
        n = 2 * i
        a = int(L[n])
        b = int(L[n + 1])
        j = round((a + b) /2 / 100,2)
        L_n.append(j)
    return L_n

Tmax = average(3)
Tmin = average(4)
day = [i[0:5] for i in raw_titel[0] if len(i) > 5]
data_f = pd.DataFrame([day,Tmax,Tmin]).T
data_f.columns = ['Day', 'Tmax', 'Tmin']
data_f[['Month','Day']] = data_f['Day'].str.split("/",expand=True)
data_f = data_f[['Month', 'Day', 'Tmax', 'Tmin']].astype(float)

data_avg = pd.read_csv(avg)
loc = [data_avg[(data_avg['Month']==data_f['Month'][i]) & ((data_avg['Day']==data_f['Day'][i]))] for i in data_f.index]
loc = [i.index[0] for i in loc]

data_cut = data_avg.iloc[loc,:]
data_cut = data_cut.reset_index(drop = True)
data_f['Year'] = year
if loc[0] >= num_year_days -7 -1:
    loc_newyear = num_year_days -7 -loc[0]
    data_f.iloc[loc_newyear:,-1] = (year + 1)
data_f['Precp'] = data_cut['Precp']
data_f['WS'] = data_cut['WS']
data_f['SolRad'] = data_cut['SolRad']
data_f = data_f[['Year','Month','Day','Tmax','Tmin','WS','SolRad','Precp']]
data_f['Year'] = data_f['Year'].astype('str')
data_f['Month'] = data_f['Month'].astype(int).apply(lambda x : '{:0>2d}'.format(x))
data_f['Day'] = data_f['Day'].astype(int).apply(lambda x : '{:0>2d}'.format(x))

#%% Step5. 合併資料,儲存，並改寫wea檔
# =============================================================================
# 存檔路徑
file1 = r'G:\GLYCIM\Weather_fromWeb\20221212\屏東新園C0R560.csv'
file2 = r'G:\GLYCIM\Weather\Xinyuan2022.csv'
# =============================================================================

report = pd.concat([data_n,data_f], axis = 0)
report = report.reset_index(drop = True)
report.to_csv(file1,header=True,index=False,encoding='utf-8-sig')

wea = pd.read_csv(file2)
wea['Year'] = report['Year']
wea = pd.DataFrame(columns =wea.columns)
wea[['Year','Month','Day','Tmax','Tmin','WS','SolRad','Precp']] = report[['Year','Month','Day','Tmax','Tmin','WS','SolRad','Precp']]
wea.to_csv(file2,header=True,index=False,encoding='utf-8-sig')

#%% Step6. 畫圖(含未來)
# 觀測資料與歷史比較
import numpy as np
import matplotlib.pyplot as plt

Time_start = '20220928'     # 旗山0124    新園0126      六腳0211
Time_end = '20230115'       # 旗山0428    新園0504      六腳0531
title = "屏東新園"      # 高雄旗山      屏東新園    嘉義六腳

Year_start = int(Time_start[0:4])
Month_start = int(Time_start[4:6])
Day_strat = int(Time_start[6:])
Year_end = int(Time_end[0:4])
Month_end = int(Time_end[4:6])
Day_end = int(Time_end[6:])

# 全部的歷史平均資料
report_history = data_avg.iloc[:,1:]
Temperature_his = report_history.loc[:,['Month','Day','Tmax','Tmin']]
Temperature_his['Temp'] = (Temperature_his['Tmax']+Temperature_his['Tmin'])/2
Temperature_his['Time'] = Temperature_his['Month'].astype('str')+'/'+Temperature_his['Day'].astype('str')
Temperature_his = Temperature_his.loc[:,['Time','Temp']]
Temperature_his.columns=['Time','Temp_his']
Temperature_his = pd.concat([Temperature_his, Temperature_his])
Temperature_his.reset_index(drop = True,inplace=True)
Temperature_his = Temperature_his.iloc[:390,:]

# 全部的觀測資料
Temperature_now = data_n.loc[:,['Month','Day','Tmax','Tmin']]
Temperature_now['Temp'] = (Temperature_now['Tmax']+Temperature_now['Tmin'])/2
Temperature_now['Month'] = Temperature_now['Month'].astype('int')
Temperature_now['Day'] = Temperature_now['Day'].astype('int')
Temperature_now['Time'] = Temperature_now['Month'].astype('str')+'/'+Temperature_now['Day'].astype('str')
Temperature_now = Temperature_now.loc[:,['Time','Temp']]
Temperature_now.columns=['Time','Temp_now']

# 全部的未來資料
Temperature_fut = data_f.loc[:,['Month','Day','Tmax','Tmin']]
Temperature_fut['Temp'] = (Temperature_fut['Tmax']+Temperature_fut['Tmin'])/2
Temperature_fut['Month'] = Temperature_fut['Month'].astype('int')
Temperature_fut['Day'] = Temperature_fut['Day'].astype('int')
Temperature_fut['Time'] = Temperature_fut['Month'].astype('str')+'/'+Temperature_fut['Day'].astype('str')
Temperature_fut = Temperature_fut.loc[:,['Time','Temp']].copy()
Temperature_fut.columns=['Time','Temp_fut']
Temperature_fut['new_loc'] = [i+Temperature_now.index[-1]+1 for i in range(Temperature_fut.shape[0])]
Temperature_fut.set_index('new_loc', drop=True,inplace=True)


# 將歷史平均、現在觀測、未來氣象合併在一起
Temperature = pd.concat([Temperature_his,Temperature_now['Temp_now']], axis = 1)
Temperature = pd.concat([Temperature,Temperature_fut['Temp_fut']], axis = 1)
# Temperature = pd.merge(Temperature_his,Temperature_now,how = 'outer')
# Temperature = pd.merge(Temperature,Temperature_fut,how = 'outer')
Temperature['now-his'] = Temperature['Temp_now']-Temperature['Temp_his']


for i in range(len(Temperature.axes[0])):
    if Temperature.loc[i,'Time'] == str(str(Month_start)+'/'+str(Day_strat)):
        start = i
    elif Temperature.loc[i,'Time'] == Temperature_now.iloc[-1,0]:
        now = i
    elif Temperature.loc[i,'Time'] == Temperature_fut.iloc[-1,0]:
        fut = i
    elif Temperature.loc[i,'Time'] == str(str(Month_end)+'/'+str(Day_end)):
        end = i

Temperature['now-his_cut'] = Temperature.loc[start:now,'now-his']
Temperature['add_his'] = np.add.accumulate(Temperature.loc[start:end,'Temp_his'])
Temperature['add_now'] = np.add.accumulate(Temperature.loc[start:now,'Temp_now'])
Temperature['add_fut'] = Temperature.loc[now,'add_now'] + np.add.accumulate(Temperature.loc[now+1:end,'Temp_fut'])


# 畫出觀測值減平均值的圖
plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=[6,4],dpi=200)
colors = np.where(np.array(Temperature['now-his_cut']) > 0,'red','blue')
plt.bar(Temperature['Time'],Temperature['now-his_cut'],color=colors)
xaxis = [Temperature.loc[i,'Time'] for i in range(start,now,7)]
plt.xticks(xaxis,rotation =60)
title_name = '觀測值減歷史平均__'+title
plt.title(title_name)
plt.ylabel('溫度差 (℃)')
num_dif = round(np.sum(Temperature['now-his_cut']),2)
if num_dif > 0:
    icon_temp = '多'
else:
    icon_temp = '少'
num_dif = abs(num_dif)
plt.xlabel('\n觀測期間：'+str(Temperature.loc[start,'Time'])+'-'+str(Temperature.loc[now,'Time'])+'                累積差異： '+icon_temp+str(num_dif)+'℃',loc='left',size = 12)
plt.tight_layout()


# 畫出累積溫度圖 (有未來預報)
plt.figure(figsize=[8,5],dpi=200)
y = np.zeros(Temperature['Time'].size)
plt.plot(Temperature['Time'],Temperature['add_now'], label='現在觀測累積',linewidth=0,marker='o')
plt.plot(Temperature['Time'],Temperature['add_fut'], label='未來預測累積',linewidth=0,marker='*')
plt.fill_between(Temperature.index, y1 = Temperature['add_his'],y2 = y,color = '#844200',alpha = 0.25, label='歷史累積',)
xaxis = [Temperature.loc[i,'Time'] for i in range(start,end,7)]
plt.xticks(xaxis)
plt.xlim(start,end)
title_name = '累積溫度__'+title
plt.title(title_name)
plt.ylabel('累積溫度 (℃)')
num_add_his = round(Temperature.loc[fut,'add_his'],2)
num_add_fut = round(Temperature.loc[fut,'add_fut'],2)
num_add_dif = round(num_add_fut-num_add_his,2)
if num_add_dif > 0:
    icon_temp_add = '多'
else:
    icon_temp_add = '少'
num_dif_day = round((num_add_dif/Temperature.loc[fut,'Temp_his']),2)
if num_add_dif > 0:
    icon_temp_dif = '早'
else:
    icon_temp_dif = '晚'

plt.xlabel('\n觀測期間：'+str(Temperature.loc[start,'Time'])+'-'+str(Temperature.loc[now,'Time'])+'                未來預測：'+str(Temperature.loc[now+1,'Time'])+'-'+str(Temperature.loc[fut,'Time'])+'\n歷史累積： '+str(num_add_his)+'℃'+'            預測累積： '+str(num_add_fut)+'℃'+'            累積差異： '+icon_temp_add+str(abs(num_add_dif))+'℃'+'            相當於： '+icon_temp_dif+str(abs(num_dif_day))+'天',loc='left')
plt.legend(loc = 'upper left')
plt.tight_layout()

#%% Step7. 畫圖(觀測與歷史比較)
import numpy as np
import matplotlib.pyplot as plt

Time_start = '20220928'     # 旗山0124    新園0126      六腳0211
Time_end = '20221231'       # 旗山0428    新園0504      六腳0531
title = "屏東新園"      # 高雄旗山      屏東新園    嘉義六腳

Year_start = int(Time_start[0:4])
Month_start = int(Time_start[4:6])
Day_strat = int(Time_start[6:])
Year_end = int(Time_end[0:4])
Month_end = int(Time_end[4:6])
Day_end = int(Time_end[6:])

# 全部的歷史平均資料
report_history = data_avg.iloc[:,1:]
Temperature_his = report_history.loc[:,['Month','Day','Tmax','Tmin']]
Temperature_his['Temp'] = (Temperature_his['Tmax']+Temperature_his['Tmin'])/2
Temperature_his['Time'] = Temperature_his['Month'].astype('str')+'/'+Temperature_his['Day'].astype('str')
Temperature_his = Temperature_his.loc[:,['Time','Temp']]
Temperature_his.columns=['Time','Temp_his']

# 全部的觀測資料
Temperature_now = data_n.loc[:,['Month','Day','Tmax','Tmin']]
Temperature_now['Temp'] = (Temperature_now['Tmax']+Temperature_now['Tmin'])/2
Temperature_now['Month'] = Temperature_now['Month'].astype('int')
Temperature_now['Day'] = Temperature_now['Day'].astype('int')
Temperature_now['Time'] = Temperature_now['Month'].astype('str')+'/'+Temperature_now['Day'].astype('str')
Temperature_now = Temperature_now.loc[:,['Time','Temp']]
Temperature_now.columns=['Time','Temp_now']

# 全部的未來資料
Temperature_fut = data_f.loc[:,['Month','Day','Tmax','Tmin']]
Temperature_fut['Temp'] = (Temperature_fut['Tmax']+Temperature_fut['Tmin'])/2
Temperature_fut['Month'] = Temperature_fut['Month'].astype('int')
Temperature_fut['Day'] = Temperature_fut['Day'].astype('int')
Temperature_fut['Time'] = Temperature_fut['Month'].astype('str')+'/'+Temperature_fut['Day'].astype('str')
Temperature_fut = Temperature_fut.loc[:,['Time','Temp']]
Temperature_fut.columns=['Time','Temp_fut']

# 將歷史平均、現在觀測、未來氣象合併在一起
Temperature = pd.merge(Temperature_his,Temperature_now,how = 'outer')
Temperature = pd.merge(Temperature,Temperature_fut,how = 'outer')
Temperature['now-his'] = Temperature['Temp_now']-Temperature['Temp_his']


for i in range(len(Temperature.axes[0])):
    if Temperature.loc[i,'Time'] == str(str(Month_start)+'/'+str(Day_strat)):
        start = i
    elif Temperature.loc[i,'Time'] == Temperature_now.iloc[-1,0]:
        now = i
    elif Temperature.loc[i,'Time'] == Temperature_fut.iloc[-1,0]:
        fut = i
    elif Temperature.loc[i,'Time'] == str(str(Month_end)+'/'+str(Day_end)):
        end = i

Temperature['now-his_cut'] = Temperature.loc[start:now,'now-his']
Temperature['add_his'] = np.add.accumulate(Temperature.loc[start:end,'Temp_his'])
Temperature['add_now'] = np.add.accumulate(Temperature.loc[start:now,'Temp_now'])
Temperature['add_fut'] = Temperature.loc[now,'add_now'] + np.add.accumulate(Temperature.loc[now+1:end,'Temp_fut'])

Temperature = Temperature.iloc[:end+1,:]

if end < now :
    now = end
    fut = end

# 畫出觀測值減平均值的圖
plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=[6,4],dpi=200)
colors = np.where(np.array(Temperature['now-his_cut']) > 0,'red','blue')
plt.bar(Temperature['Time'],Temperature['now-his_cut'],color=colors)
xaxis = [Temperature.loc[i,'Time'] for i in range(start,now,7)]
plt.xticks(xaxis,rotation =60)
title_name = '觀測值減歷史平均__'+title
plt.title(title_name)
plt.ylabel('溫度差 (℃)')
num_dif = round(np.sum(Temperature['now-his_cut']),2)
if num_dif > 0:
    icon_temp = '多'
else:
    icon_temp = '少'
num_dif = abs(num_dif)
plt.xlabel('\n觀測期間：'+str(Temperature.loc[start,'Time'])+'-'+str(Temperature.loc[now,'Time'])+'                累積差異： '+icon_temp+str(num_dif)+'℃',loc='left',size = 12)
plt.tight_layout()

plt.figure(figsize=[8,5],dpi=200)
y = np.zeros(Temperature['Time'].size)
plt.plot(Temperature['Time'],Temperature['add_now'], label='現在觀測累積',linewidth=0,marker='o')
plt.fill_between(Temperature['Time'], y1 = Temperature['add_his'],y2 = y,color = '#844200',alpha = 0.25, label='歷史累積',)
xaxis = [Temperature.loc[i,'Time'] for i in range(start,end,7)]
plt.xticks(xaxis)
title_name = '累積溫度__'+title
plt.title(title_name)
plt.ylabel('累積溫度 (℃)')
num_add_his = round(Temperature.loc[fut,'add_his'],2)
num_add_now = round(Temperature.loc[fut,'add_now'],2)
num_add_dif = round(num_add_now-num_add_his,2)
if num_add_dif > 0:
    icon_temp_add = '多'
else:
    icon_temp_add = '少'
num_dif_day = round((num_add_dif/Temperature.loc[fut,'Temp_his']),2)
if num_add_dif > 0:
    icon_temp_dif = '早'
else:
    icon_temp_dif = '晚'

plt.xlabel('\n觀測期間：'+str(Temperature.loc[start,'Time'])+'-'+str(Temperature.loc[now,'Time'])+'\n歷史累積： '+str(num_add_his)+'℃'+'            觀測累積： '+str(num_add_now)+'℃'+'            累積差異： '+icon_temp_add+str(abs(num_add_dif))+'℃'+'            相當於： '+icon_temp_dif+str(abs(num_dif_day))+'天',loc='left')
plt.legend(loc = 'upper left')
plt.tight_layout()
