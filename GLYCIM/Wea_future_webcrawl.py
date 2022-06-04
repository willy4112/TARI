# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 17:10:47 2022

@author: CCW
"""

# 載入套件
from bs4 import BeautifulSoup # 網頁解析
import pandas as pd
import requests  # 發送 requests
import warnings
warnings.filterwarnings("ignore")


# 變數設置
headers = {"Content-Type": "text/html; charset=UTF-8d"}
url = 'https://www.cwb.gov.tw/V8/C/W/Town/MOD/Week/1001008_Week_PC.html?T=2022060419-4'
payload = {'T': '2022060416-4'}


# 發送 Requests
res = requests.post(url, headers=headers).content
# 解析網頁
soup = BeautifulSoup(res, 'html.parser')

# 捕捉所需的資料表頭
hader = [
    [i.text.strip() for i in item.find_all('th')]
    for item in soup.find_all('tr')
]
index = [i[0] for i in hader[3:]]
day = [i[0:5] for i in hader[0][1:]]
time = hader[1][1:3]
columns = pd.MultiIndex.from_product([day, time],names = [i[0] for i in hader[0:2]])
del hader,day,time

# 捕捉所需的資料內容
data = [
    [i.text.strip() for i in item.find_all('td')]
    for item in soup.find_all('tr')
]
data = data[3:]

# print(shareholdings_records)

df = pd.DataFrame(data, index=index,columns = columns)
df1 = df.iloc[0:2,:]
for i in range(df1.shape[0]):
    for j in range(df1.shape[1]):
        a = df1.iloc[i,j]
        df1.iloc[i,j] = a[:2]+'.'+a[2:]

df1 = df1.astype('float')
df1 = df1.mean(axis=1, level='日期')
