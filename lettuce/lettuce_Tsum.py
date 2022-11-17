# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 14:04:14 2022

@author: CWW
"""
#%% Step0. 控制區

# 以爬蟲抓取目標鄉鎮之最高最低溫，分別計算歷史平均與當年觀測資料，求出達到累積溫度的時間
# 限制：起始時間需比當下時間少1-2天

# 使用的套件
import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt

# step1用
# 設定觀測的起始與結束時間
now_t1 = '2022-01-01'
now_t2 = '2022-11-16'   # 需比當下時間少1-2天，至少要少1天。

# step2用
# 設定歷史平均的起始與結束時間
his_t1 = '2015-04-30'
his_t2 = '2021-12-31'   # 建議比當下時間少1-2天，至少要少1天。

# step3用
# 當下年分
year = 2022

# step4用
# 當下時間
t3 = 2022111609-1   #最後面的09-1不用更改

# step5用
Time_start = '20221120'     # 開始計算的時間
title = "二崙"              # 地點
Topt = 26                   # 溫度最上限
Tsum_stop = 1044.4          # 累積門檻值



#%% Step1. 二崙C0K440(2015-04-30)取至今年

# URL
url = f'https://agr.cwb.gov.tw/NAGR/history/station_day/create_report?station=C0K440&start_time={now_t1}&end_time={now_t2}&items=TxMaxAbs,TxMinAbs&report_type=csv_time&level=%e8%87%aa%e5%8b%95%e7%ab%99'
r = requests.get(url)

# 將資料取出並排列成list
raw = r.text
raw = list(map(lambda x: x.split(','),raw.split("\r\n")))

# 將資料轉換成DataFrame
df = pd.DataFrame(raw[2:])
df = df.iloc[:-1,1:]
df.columns = ['date', 'Tmax', 'Tmin']
df_now = df

#%% Step2. 二崙C0K440(2015-04-30)取至20211231

# URL
url = f'https://agr.cwb.gov.tw/NAGR/history/station_day/create_report?station=C0K440&start_time={his_t1}&end_time={his_t2}&items=TxMaxAbs,TxMinAbs&report_type=csv_time&level=%e8%87%aa%e5%8b%95%e7%ab%99'
r = requests.get(url)

# 將資料取出並排列成list
raw = r.text
raw = list(map(lambda x: x.split(','),raw.split("\r\n")))

# 將資料轉換成DataFrame
df = pd.DataFrame(raw[2:-1])
df = df.iloc[:,1:-1]
df.columns = ['date', 'Tmax', 'Tmin']

# 檢查缺失值，並移除
lost = df.loc[(df['Tmax'] == '') | (df['Tmin'] == '')]
df = df.drop(index = lost.index)

# 轉換資料型態為float
df[['Tmax', 'Tmin']] = df[['Tmax', 'Tmin']].astype(float)
df['date'] = [i[5:] for i in df['date']]
df = df.groupby('date').mean()
df = round(df,2)
df = df.reset_index()

df_avg366 = df
df_avg365 = df.drop(index = 59)
df_avg365 = df_avg365.reset_index(drop = True)

#%% Step3. 將缺值以歷史平均補上

if year%4 == 0:
    df_avg = df_avg366
else:
    df_avg = df_avg365

df_avg[['Month','Day']] = df_avg['date'].str.split("-",expand=True)
df_avg = df_avg[['Month', 'Day', 'Tmax', 'Tmin']].astype(float)

# 檢查缺失值
lost = df_now.loc[(df_now['Tmax'] == '') | (df_now['Tmin'] == '')]

# 取出有缺漏的index
L = lost.index

# 將df資料取代data中有缺值的部分
item = ['Tmax', 'Tmin']
for i in item:
    for j in L:
        if df_now.loc[j,i] == '':
            df_now.loc[j,i] = df_avg.loc[j,i]

# 改變資料型態為float
df_now[['Tmax', 'Tmin']] = df_now[['Tmax', 'Tmin']].astype(float)
df_now[['Year', 'Month','Day']] = df_now['date'].str.split("-",expand=True)
df_now = df_now[['Month', 'Day', 'Tmax', 'Tmin']].astype(float)

#%% Step4. 二崙1000911抓取未來一周資料

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
df_future = [raw_titel[i] + raw_data[i] for i in range(len(raw_titel))]

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
df_future = pd.DataFrame([day,Tmax,Tmin]).T
df_future.columns = ['Day', 'Tmax', 'Tmin']
df_future[['Month','Day']] = df_future['Day'].str.split("/",expand=True)
df_future = df_future[['Month', 'Day', 'Tmax', 'Tmin']].astype(float)


#%% Step5. 畫圖(含未來)
# 觀測資料與歷史比較

# Time_start = '20220910'     # 開始計算的時間

Year_start = int(Time_start[0:4])
Month_start = int(Time_start[4:6])
Day_strat = int(Time_start[6:])
# Year_end = int(Time_end[0:4])
# Month_end = int(Time_end[4:6])
# Day_end = int(Time_end[6:])


# 每日溫為(最高+最低)/2
# 超過26以26計算
def set_Topt(df,col_name,Topt):
    df = df
    
    for i in range(df.shape[0]):
        if df.loc[i,'Tmax'] >= Topt:
            df.loc[i,'Tmax'] = Topt
        elif df.loc[i,'Tmin'] >= Topt:
            df.loc[i,'Tmin'] = Topt
    
    df['Temp'] = (df['Tmax']+df['Tmin'])/2
    df['Month'] = df['Month'].astype('int')
    df['Day'] = df['Day'].astype('int')
    df['Time'] =  df['Month'].astype('str')+'/'+df['Day'].astype('str')
    df = df.loc[:,['Time','Temp']]
    df.columns=['Time',col_name]
    
    # for i in range(df.shape[0]):
    #     if df.iloc[i,1] >= Topt:
    #         df.iloc[i,1] = Topt
    return df

# 分別計算過去現在未來每日溫
Temperature_his = set_Topt(df_avg, 'Temp_his', Topt)
Temperature_now = set_Topt(df_now, 'Temp_now', Topt)
Temperature_fut = set_Topt(df_future, 'Temp_fut', Topt)


# 將歷史平均、現在觀測、未來氣象合併在一起
Temperature = pd.merge(Temperature_his,Temperature_now,how = 'outer')
Temperature = pd.merge(Temperature,Temperature_fut,how = 'outer')

# 增加年分
Temperature['Time'] = str(Year_start) + '/' + Temperature['Time']

for i in range(Temperature.shape[0]):
    if Temperature.loc[i,'Time'] == f'{Year_start}/{Month_start}/{Day_strat}':
        start = i
    elif (Temperature.loc[i,'Time'])[5:] == Temperature_now.iloc[-1,0]:
        now = i
    elif (Temperature.loc[i,'Time'])[5:] == Temperature_fut.iloc[-1,0]:
        fut = i


# 歷史累加溫度
Temperature['add_his'] = np.add.accumulate(Temperature.loc[start:,'Temp_his'])
# 判定歷史值是否由達門檻
if Temperature['add_his'].iloc[-1,] < Tsum_stop:
    # 增加一年度歷史平均資料
    Temperature_his['Time'] = str(Year_start+1) + '/' + Temperature_his['Time']
    Temperature = pd.concat([Temperature,Temperature_his])
    Temperature = Temperature.reset_index(drop = True)
    # 重新計算
    Temperature['add_his'] = np.add.accumulate(Temperature.loc[start:,'Temp_his'])
else:
    pass

# 現在與未來累加溫度
Temperature['add_now'] = np.add.accumulate(Temperature.loc[start:,'Temp_now'])
Temperature['add_fut'] = Temperature.loc[now,'add_now'] + np.add.accumulate(Temperature.loc[now+1:,'Temp_fut'])
Temperature['add_fut+his'] = Temperature.loc[fut,'add_fut'] + np.add.accumulate(Temperature.loc[fut+1:,'Temp_his'])

# 取得結束時間
T_his = Temperature[['Time', 'add_his']][(Temperature['add_his'] >= Tsum_stop)].iloc[0,0]
num_his = round(Temperature[['Time', 'add_his']][(Temperature['add_his'] >= Tsum_stop)].iloc[0,1],2)
end_his = Temperature[['Time', 'add_his']][(Temperature['add_his'] >= Tsum_stop)].index[0]





if Temperature['add_now'].dropna().iloc[-1,] >= Tsum_stop:
    T_obs = Temperature[['Time', 'add_now']][(Temperature['add_now'] >= Tsum_stop)].iloc[0,0]
    num_obs = round(Temperature[['Time', 'add_now']][(Temperature['add_now'] >= Tsum_stop)].iloc[0,1],2)
    end_obs = Temperature[['Time', 'add_now']][(Temperature['add_now'] >= Tsum_stop)].index[0]
elif Temperature['add_fut'].dropna().iloc[-1,] >= Tsum_stop:
    T_obs = Temperature[['Time', 'add_fut']][(Temperature['add_fut'] >= Tsum_stop)].iloc[0,0]
    num_obs = round(Temperature[['Time', 'add_fut']][(Temperature['add_fut'] >= Tsum_stop)].iloc[0,1],2)
    end_obs = Temperature[['Time', 'add_fut']][(Temperature['add_fut'] >= Tsum_stop)].index[0]
else:
    T_obs = Temperature[['Time', 'add_fut+his']][(Temperature['add_fut+his'] >= Tsum_stop)].iloc[0,0]
    num_obs = round(Temperature[['Time', 'add_fut+his']][(Temperature['add_fut+his'] >= Tsum_stop)].iloc[0,1],2)
    end_obs = Temperature[['Time', 'add_fut+his']][(Temperature['add_fut+his'] >= Tsum_stop)].index[0]

# 比較結束時間
if end_his > end_obs:
    end = end_his
else:
    end = end_obs


# 畫出累積溫度圖 (有未來預報)
plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=[8,5],dpi=300)
y = np.zeros(Temperature['Time'].size)
plt.plot(Temperature['Time'],Temperature['add_now'], label='現在觀測累積',linewidth=0,marker='o')
plt.plot(Temperature['Time'],Temperature['add_fut'], label='未來預測累積',linewidth=0,marker='*')
plt.plot(Temperature['Time'],Temperature['add_fut+his'], label='未來 + 歷史平均預測累積 ',linewidth=0,marker='x')
plt.fill_between(Temperature['Time'], y1 = Temperature['add_his'],y2 = y,color = '#844200',alpha = 0.25, label='歷史累積',)
xaxis = [Temperature.loc[i,'Time'] for i in range(start,end,7)]
plt.xlim(start, end)
plt.xticks(xaxis)
title_name = '累積溫度__'+title
plt.title(title_name)
plt.ylim(0, (int(Tsum_stop/100)+2)*100)
plt.ylabel('累積溫度 (℃)')

plt.xlabel(f'\n歷史達到期間： {T_his} ( {num_his} ℃ )' + f'\n觀測到達時間： {T_obs} ( {num_obs} ℃ )',loc='left')
plt.legend(loc = 'upper left')
plt.tight_layout()
