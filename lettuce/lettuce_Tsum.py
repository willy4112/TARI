# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 14:04:14 2022

@author: CWW
"""

#%% Step1. CODIS資料_C0K440_二崙

from bs4 import BeautifulSoup
import pandas as pd
import requests

# =============================================================================
# 設定要抓取年分與月份
year = 2022
month = 11
# =============================================================================

data = pd.DataFrame()
for i in range(1,month+1):
    
    month = i
    month = '{0:02d}'.format(month)
    
    
    headers = {"Content-Type": "text/html;charset=utf-8"}
    # C0K440_二崙URL
    url = f'https://e-service.cwb.gov.tw/HistoryDataQuery/MonthDataController.do?command=viewMain&station=C0K440&stname=%25E4%25BA%258C%25E5%25B4%2599&datepicker={year}-{month}&altitude=35.0m'
    
    # 發送 Requests
    res = requests.post(url, headers=headers).content
    
    # 解析網頁
    soup = BeautifulSoup(res, 'html.parser')
    
    # 取得資料
    table = soup.find('table', {'id': 'MyTable'})
    df = pd.read_html(str(table))[0]
    # 資料處理
    df = df.iloc[:,[0,8,10]]
    df.columns = ['Day', 'Tmax', 'Tmin']
    df['Year'] = year
    df['Month'] = int(month)
    df = df[['Year', 'Month', 'Day', 'Tmax', 'Tmin']]
    
    data = pd.concat([data,df])
    data = data.reset_index(drop = True)

#%% Step2. 農業氣象觀測網監測系統_A2K630

import pandas as pd
import requests

#  =============================================================================
# 設定起始與結束時間
t1 = '2022-01-01'
t2 = '2022-11-14'   # 建議比當下時間少1-2天，至少要少1天。
# =============================================================================

# 臺大雲林校區URL
url = f'https://agr.cwb.gov.tw/NAGR/history/station_day/create_report?station=A2K630&start_time={t1}&end_time={t2}&items=TxMaxAbs,TxMinAbs&report_type=csv_time&level=%E6%96%B0%E8%BE%B2%E6%A5%AD%E7%AB%99'
r = requests.get(url)

# 將資料取出並排列成list
raw = r.text
raw = list(map(lambda x: x.split(','),raw.split("\r\n")))

# 將資料轉換成DataFrame
df = pd.DataFrame(raw[2:-1])
df = df.iloc[:,1:]
df.columns = ['date', 'Tmax', 'Tmin']

# 轉換資料型態為float
df[['Tmax', 'Tmin']] = df[['Tmax', 'Tmin']].astype(float)


#%% Step3. 將缺值補上
import pandas as pd

# data 資料，由CODIS抓取，容易有缺值，且無日射量。
# df 資料，由農業氣象觀測網監測系統抓取，較為詳細的資料。

# 利用以之時間的df來裁切多餘的data
data = data.iloc[:df.shape[0],:]

# 檢查缺失值
lost = data.loc[(data['Tmax'] == '...') | (data['Tmin'] == '...')]

# 取出有缺漏的index
L = lost.index

# 將df資料取代data中有缺值的部分
item = ['Tmax', 'Tmin']
for i in item:
    for j in L:
        if data.loc[j,i] == '...':
            data.loc[j,i] = df.loc[j,i]

# 重新排列資料順序
data = data[['Year', 'Month', 'Day', 'Tmax', 'Tmin']]

# 改變資料型態為float
data[['Tmax', 'Tmin']] = data[['Tmax', 'Tmin']].astype(float)
data_n = data

#%% Step4. 抓取未來一周資料

from bs4 import BeautifulSoup
import pandas as pd
import requests

# =============================================================================
# 輸入資料
t3 = 2022111409-1
year = 2022
avg = r"C:\Users\TARI\Downloads\365_A2K630_2y_avg.csv"
# =============================================================================


headers = {"Content-Type": "text/html; charset=UTF-8"}
url = f'https://www.cwb.gov.tw/V8/C/W/Town/MOD/Week/1000911_Week_PC.html?T={t3}'

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
data_avg[['Month','Day']] = data_avg['day'].str.split("/",expand=True)
data_avg = data_avg[['Month', 'Day', 'Tmax', 'Tmin']].astype(float)
loc = data_avg[(data_avg['Month']==data_f['Month'][0]) & ((data_avg['Day']==data_f['Day'][0]))]
loc = [i for i in loc.index][0]

data_cut = data_avg.iloc[loc:loc+7,:]
data_cut = data_cut.reset_index(drop = True)
data_f['Year'] = year
data_f = data_f[['Year','Month','Day','Tmax','Tmin']]

#%% Step5. 畫圖(含未來)
# 觀測資料與歷史比較
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# 輸入資料
Time_start = '20220928'     # 旗山0124    新園0126      六腳0211
Time_end = '20221231'       # 旗山0428    新園0504      六腳0531
title = "二崙"      # 高雄旗山      屏東新園    嘉義六腳
# =============================================================================


Year_start = int(Time_start[0:4])
Month_start = int(Time_start[4:6])
Day_strat = int(Time_start[6:])
Year_end = int(Time_end[0:4])
Month_end = int(Time_end[4:6])
Day_end = int(Time_end[6:])

# 全部的歷史平均資料
report_history = data_avg.iloc[:,:]
Temperature_his = report_history.loc[:,['Month','Day','Tmax','Tmin']]
Temperature_his['Temp'] = (Temperature_his['Tmax']+Temperature_his['Tmin'])/2
Temperature_his['Month'] = Temperature_his['Month'].astype('int')
Temperature_his['Day'] = Temperature_his['Day'].astype('int')
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


# # 畫出觀測值減平均值的圖
# plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
# plt.rcParams['axes.unicode_minus'] = False
# plt.figure(figsize=[6,4],dpi=200)
# colors = np.where(np.array(Temperature['now-his_cut']) > 0,'red','blue')
# plt.bar(Temperature['Time'],Temperature['now-his_cut'],color=colors)
# xaxis = [Temperature.loc[i,'Time'] for i in range(start,now,7)]
# plt.xticks(xaxis,rotation =60)
# title_name = '觀測值減歷史平均__'+title
# plt.title(title_name)
# plt.ylabel('溫度差 (℃)')
# num_dif = round(np.sum(Temperature['now-his_cut']),2)
# if num_dif > 0:
#     icon_temp = '多'
# else:
#     icon_temp = '少'
# num_dif = abs(num_dif)
# plt.xlabel('\n觀測期間：'+str(Temperature.loc[start,'Time'])+'-'+str(Temperature.loc[now,'Time'])+'                累積差異： '+icon_temp+str(num_dif)+'℃',loc='left',size = 12)
# plt.tight_layout()


# 畫出累積溫度圖 (有未來預報)
plt.figure(figsize=[8,5],dpi=200)
y = np.zeros(Temperature['Time'].size)
plt.plot(Temperature['Time'],Temperature['add_now'], label='現在觀測累積',linewidth=0,marker='o')
plt.plot(Temperature['Time'],Temperature['add_fut'], label='未來預測累積',linewidth=0,marker='*')
plt.fill_between(Temperature['Time'], y1 = Temperature['add_his'],y2 = y,color = '#844200',alpha = 0.25, label='歷史累積',)
xaxis = [Temperature.loc[i,'Time'] for i in range(start,end,7)]
plt.xticks(xaxis)
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
