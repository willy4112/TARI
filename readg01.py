# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 14:13:57 2022

@author: CWW
"""
# # 處理網格縣市鄉鎮
# import pandas as pd

# file1 = r'G:\臺灣歷史氣候重建資料_5公里\grid_5km_town2.csv'
# file2 = r'G:\climate change model\to_run\city.csv'

# df1 = pd.read_csv(file1,encoding='big5')
# df2 = pd.read_csv(file2,encoding='big5')
# town = df2.iloc[:,:3]
# town = pd.merge(town, df1, how='left', left_on=['lon','lat'],right_on=['LON','LAT'])
# town = town.drop(['ID', 'LON', 'LAT', 'SITE', 'note'],axis=1)
# town.to_csv(r'G:\climate change model\to_run\town.csv',encoding='utf-8',index=False)


# green-soybean
import glob
import pandas as pd

# crop = ['green-soybean', 'soybean','sweet-corn', 'field-corn']

df_town = pd.read_csv(r'G:\climate change model\to_run\town.csv')

# crop = 'KH9'
# rcp = 'RCP45'
# model = 'bcc-csm1-1'
# year = 2030
# time = 'fall'

# rcp = ['RCP45','RCP85']
# model = ['bcc-csm1-1','canESM2','CCSM4','MIROC-ESM','MRI-CGCM3','norESM1-M']
# year = [2030,2040,2050]
# time = ['spring','fall']
# time_day= {'spring':'0215','fall':'0830'}

def writedata(crop,rcp,model,year,time):
    report = []
    for i in range(df_town.shape[0]):
        
        ID,lon,lat,city,town = df_town.iloc[i,:]
        
        path = fr'G:\climate change model\to_run\{model}\{crop}-{time}\{time}_{ID}*{year}'
        files = glob.glob(path)
        file = [f for f in files if int((f.split('\\')[-1]).split('_')[1])== ID][0]
        file_g01 =  glob.glob(f'{file}\*.g01')[0]
        g01 = pd.read_csv(file_g01,sep='\s+',header=None)
        g01.columns=["DAY","JDAY","LAREAB","LAREAM","LAREAT","LSTEMH","NBRNCH","NFLRS","PODS","RSTAGE","VSTAGE","SEEDP","GSEEDWT","CLIMAT2","CLIMAT3","CLIMAT4","CLIMAT1","CLIMAT5","SHTWT","ROOTWT","PSIM","WSTRESS","LSTRESS","LEAFWT","PETWT","STEMWT","SEEDWT","PODWT","NodWT","NRATIO","SCPOOL","RCPOOL","FIXCS","USEDCS","PLANTN","NODN"]
        plants_ha = round(10000/42*10000/6,2)  #株/ha
        podfw_plant = round(g01.loc[g01.shape[0]-1,'PODWT']/(1-0.78) + g01.loc[g01.shape[0]-1,'SEEDWT']/(1-0.67),2)  # g/株
        podfw_ha = round(podfw_plant*plants_ha/1000,0)     # kg/ha
        time_start = g01.loc[0,'JDAY']-3
        # Rstage未達6或6.1
        if g01.loc[g01.shape[0]-1,'RSTAGE'] >= 6.1:
            time_R6,R6 = g01[(g01.RSTAGE>=6)].iloc[0,[1,9]]
            time_R61,R61 = g01[(g01.RSTAGE>=6.1)].iloc[0,[1,9]]
        elif g01.loc[g01.shape[0]-1,'RSTAGE'] >= 6:
            time_R61,R61 = g01.loc[g01.shape[0]-1,['JDAY','RSTAGE']]
        else:
            time_R6,R6 = time_R61,R61 = g01.loc[g01.shape[0]-1,['JDAY','RSTAGE']]
        range_R6 = time_R6-time_start
        range_R61 = time_R61-time_start
        
        data = [lon,lat,city,town,podfw_ha,range_R6,range_R61]
        report.append(data)
    report = pd.DataFrame(report,columns = ['lon','lat','縣市','鄉鎮','產量(kg/ha)','到達R6日數','到達R6.1日數'])
    return report

time_day= {'spring':'0215','fall':'0830'}
crop = ['KH9', 'TN10']
time = ['spring', 'fall']
# model = ['bcc-csm1-1','canESM2','CCSM4','MIROC-ESM','MRI-CGCM3','norESM1-M']

r = 'RCP45'
m = 'norESM1-M'

for c in crop:
    for t in time:
        d = time_day[t]
        year = [2030,2040,2050]
        for i in year:
            a = writedata(c,r,m,i,t)
            a.to_csv(fr'G:\climate change model\report\{c}_{r}_{m}_{i}{d}.csv',encoding='utf-8',index=False) 
            print(c,t,i)
