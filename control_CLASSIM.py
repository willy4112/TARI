# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 14:20:45 2022

@author: CWW
"""
#%% Step1. 製作run.csv
import pandas as pd

titel = ['site','rcp','model','year','start','fertilizer1','sowing','fertilizer2','end','path']
crop = {'s1':['01/15','01/30','02/02','03/02','08/15'],
        's2':['02/20','03/04','03/06','04/05','08/30'],
        'sn':['04/15','05/04','05/06','06/04','10/15'],
        'f':['07/20','08/06','08/08','09/01','12/30'],
        'w':['10/25','11/05','11/07','12/10','05/01']}

def makerunlist(site,rcp,model,ynin,ymax,Q):
    site = site
    rcp = rcp
    model = model
    ynin = ynin
    ymax = ymax+1
    time = crop[Q]
    day = time[0]
    day = ''.join( x for x in day if x not in '/')
    L = []
    for i in range(ynin,ymax):
        step = [site,rcp,model,i]
        step = step + time
        path = fr'C:\Users\TARI\Documents\CLASSIM\{site}{Q}\{site}_{rcp}_{model}_{i}{day}'
        step.append( path)
        L.append(step)
    df = L
    df = pd.DataFrame(df,columns=titel)
    df.to_csv(fr'C:\Users\TARI\Documents\CLASSIM\{site}{Q}.csv', header=True, index=None)


# =============================================================================
# 輸入
plant = ['s1', 's2','sn','f','w']
for p in plant:
    makerunlist('grd308','rcp45','bcc-csm1-1',2026,2055,p)
# =============================================================================




#%% Step2. 複製所需檔案與製作啟動檔

import os
import glob
import pandas as pd
import shutil

plant = ['s1', 's2','sn','f','w']
for p in plant:
    
    
    # =============================================================================
    # 輸入
    fileinput = fr'C:\Users\TARI\Documents\CLASSIM\grd308{p}.csv'
    dfin = pd.read_csv(fileinput)
    
    
    
    L = []
    for i in range(dfin.shape[0]):
        site = dfin.loc[i,'site']
        rcp = dfin.loc[i,'rcp']
        model = dfin.loc[i,'model']
        year = dfin.loc[i,'year']
        start = dfin.loc[i,'start']
        fertilizer1 = dfin.loc[i,'fertilizer1']
        sowing = dfin.loc[i,'sowing']
        fertilizer2 = dfin.loc[i,'fertilizer2']
        end = dfin.loc[i,'end']
        path = dfin.loc[i,'path']
        name = path.split('\\')[-1]
        crop = (fileinput.split('\\')[-1]).split('.')[0]
        key = fr'C:\Users\TARI\Documents\CLASSIM\2dmaizsim ./{crop}\{name}/Rungrd235.dat'
        L.append(key)
    
    # site = 'grd258'
    # rcp = 'rcp45'
    # model = 'bcc-csm1-1'
    # year = '2029'
    # start = '02/20'
    # fertilizer1 = '03/04'
    # sowing = '03/06'
    # fertilizer2 = '04/05'
    # end = '08/30'
    # path = r'C:\Users\TARI\Documents\CLASSIM\run\124'
    # =============================================================================
        
        files =  glob.glob(r'C:\Users\TARI\Documents\CLASSIM\run\*')
        files = [i for i in files if site in i ]
        org = files[0]
        files = glob.glob(f'{org}\*')
        
        def copy(site,path):
            L = ['BiologyDefault.bio','BrightJean.var','createError.log','dataGen2.dat','grd235.dat','grd235.drp','grd235.grd',
                 'grd235.drp','grd235.lyr','grd235.nit','grd235.nod','grd235-rcp45-bcc-csm1-1.cli',f'{site}s.dat',f'{site}s.soi',
                 'grid_bnd','NitrogenDefault.sol','Rosetta.log','Water.DAT','WatMovParam.dat']
            for i in L:
                old = f'{org}\{i}'
                new = f'{path}\{i}'
                shutil.copy(old,new)
        
        def write_ini(site,year,sowing,end,path):
            a = 'grd235.ini'
            file = [i for i in files if a in i ]
            file = file[0]
            df = pd.read_table(file,header=None)
            t1 = f'{sowing}/{year}'
            # 處理跨年問題
            if int(sowing[0:2]) >= 10:
                year = str(int(year)+1)
                t2 = f'{end}/{year}'
            else:
                t2 = f'{end}/{year}'
            df.iloc[8] = f"'{t1}'  '{t2}'  60"
            df.to_csv(f'{path}\grd235.ini', header=None, index=None, sep='\t',doublequote=False)
        
        def write_tim(site,year,start,end,path):
            a = 'grd235.tim'
            file = [i for i in files if a in i ]
            file = file[0]
            df = pd.read_table(file,header=None)
            t1 = f'{start}/{year}'
            # 處理跨年問題
            if int(sowing[0:2]) >= 10:
                year = str(int(year)+1)
                t2 = f'{end}/{year}'
            else:
                t2 = f'{end}/{year}'
            df.iloc[2] = f"'{t1}'  0.0001        0.0000001000  1.3000        0.3000        '{t2}'"
            df.to_csv(f'{path}\grd235.tim', header=None, index=None, sep='\t',doublequote=False)
        
        def write_man(site,year,fertilizer1,fertilizer2,path):
            a = 'grd235.man'
            file = [i for i in files if a in i ]
            file = file[0]
            df = pd.read_table(file,header=None)
            t1 = f'{fertilizer1}/{year}'
            t2 = f'{fertilizer2}/{year}'
            df.iloc[4] = f"'{t1}' 30.000000     5.000000      0.000000      0.000000      "
            df.iloc[5] = f"'{t2}' 30.000000     5.000000      0.000000      0.000000      "
            df.to_csv(f'{path}\grd235.man', header=None, index=None, sep='\t',doublequote=False)
        
        def write_rundat(site,path):
            a = 'Rungrd235.dat'
            file = [i for i in files if a in i ]
            file = file[0]
            df = pd.read_table(file,header=None)
            df1 = df.copy()
            for i in range(df.shape[0]):
                a = df.iloc[i,0].split('\\')[-1]
                df1.iloc[i] = f'{path}\{a}'
            df1.to_csv(f'{path}\Rungrd235.dat', header=None, index=None, sep='\t',doublequote=False)
        
        def write_wea(site,rcp,model,path):
            file =  glob.glob(r'C:\Users\TARI\Downloads\MAIZSIM WEA\wea file\*')
            file = [i for i in file if site in i ]
            file = [i for i in file if model in i ]
            df = pd.read_csv(file[0], sep='delimiter')
            for i in range(df.shape[0]):
                df.iloc[i,0] = df.iloc[i,0].replace(',',' ')
            file1 = r'C:\Users\TARI\Documents\CLASSIM\run\9\grd235-rcp45-bcc-csm1-1.wea'
            df1 = pd.read_table(file1,header=None)
            df.columns = df1.columns
            df2 = pd.concat([df1.iloc[:2,0],df.iloc[:,0]])
            df2 = pd.DataFrame(df2)
            df2.to_csv(f'{path}\{site}-{rcp}-{model}.wea', header=None, index=None, sep='\t')
            file2 = f'{path}\Rungrd235.dat'
            df3 = pd.read_table(file2,header=None)
            df3.iloc[0] = f'{path}\{site}-{rcp}-{model}.wea'
            df3.to_csv(f'{path}\Rungrd235.dat', header=None, index=None, sep='\t',doublequote=False)
        
        
        os.makedirs(path, exist_ok=True)
        copy(site,path)
        write_ini(site,year,sowing,end,path)
        write_tim(site,year,start,end,path)
        write_man(site,year,fertilizer1,fertilizer2,path)
        write_rundat(site,path)
        write_wea(site,rcp,model,path)
        
        print(f'<<<<<{name} Down!>>>>>')
    L.append('PAUSE')
    df = pd.DataFrame(L)
    bot_name = (fileinput.split('\\')[-1]).split('.')[0]
    df.to_csv(fr'C:\Users\TARI\Documents\CLASSIM\Runexp-{bot_name}.bat', header=None, index=None, sep='\t',doublequote=False)


#%% Step3. 讀取g01結果

'''
代辦：
(1) 未修改鮮重含水率
(2) 要改title
(3) 要改檔名
'''
import glob
import pandas as pd
import matplotlib.pyplot as plt

# model = ['bcc-csm1-1','canESM2','CCSM4','MIROC-ESM','MRI-CGCM3','norESM1-M']
model = ['bcc-csm1-1',]
plant = ['s1', 's2','sn','f','w']
place = 'grd308'


for m in model:
    for p in plant:
        
        # =============================================================================
        files = glob.glob(fr'G:\CLASSIM-rawdata\{place}\rcp45\{m}\{place}{p}\*\grd235.g01')
        # files = glob.glob(fr'C:\Users\TARI\Documents\CLASSIM\{place}{p}\*\grd235.g01')
        # =============================================================================
        
        L = []
        for i in files:
            
            file = i
            df = pd.read_csv(file)
            name = file.split('\\')[-2]
            year = int((df['date'].iloc[0]).split('/')[-1])
            Harvest = df['date'].iloc[-1]
            Gap = df['    jday'].iloc[-1]-df['    jday'].iloc[0]
            EarDM = df['earDM'].iloc[-1]    # 單位，g/plant
            # 種植密度，6.5 plants/m2，1 ha = 10000 m2
            Planting_density = 10000*6.5   # 單位，plants/ha
            # 鮮重水分含量
            Water_content = 0.7     # 單位，%
            EarDM = EarDM*Planting_density/1000   # 單位，Kg/ha
            Ear = EarDM*Planting_density/(1-Water_content)/1000   # 單位，Kg/ha
            L.append([year,name,Harvest,Gap,EarDM,Ear])
            # print(f'{name}    Harvest: {Harvest}({Gap} days)    EarDM: {EarDM} g/plant')
        data = pd.DataFrame(L,columns = ['year','name','harvest','use days','earDM','ear'])
        site = (file.split('\\')[-2])[:-9]
        crop = (file.split('\\')[-3])[6:]
        # Ear產量(鮮重)
        plt.figure(dpi=200)
        plt.plot(data['year'],data['ear'],marker='o')
        plt.grid(axis='x', color='0.80')
        plt.title(f'{site}_{crop}  Ear')
        plt.ylabel('(Kg/ha)')
        # plt.savefig(fr'C:\Users\TARI\Documents\CLASSIM\_report\{site}_{crop}_Ear.png', bbox_inches='tight',transparent=True)
        
        # # EarDM
        # plt.figure(dpi=200)
        # plt.plot(data['year'],data['earDM'],marker='o')
        # plt.grid(axis='x', color='0.80')
        # plt.title(f'{site}_{crop}  EarDM')
        # plt.ylabel('(Kg/ha)')
        # plt.savefig(fr'C:\Users\TARI\Documents\CLASSIM\_report\{site}_{crop}_EarDM.png', bbox_inches='tight',transparent=True)
        data.to_csv(fr'C:\Users\TARI\Documents\CLASSIM\_report\{site}_{crop}_Ear.csv',encoding='utf-8',index=False)

#%% Step4. 產量分析

import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta

# model = ['bcc-csm1-1','canESM2','CCSM4','MIROC-ESM','MRI-CGCM3','norESM1-M']
model = 'bcc-csm1-1'
plant = ['s1', 's2','sn','f','w']

files = glob.glob(r'C:\Users\TARI\Documents\CLASSIM\_report\*.csv')
files = [f for f in files if model in f]

def readdata(p):
    file = [f for f in files if p in f]
    data = pd.read_csv(file[0])
    mean = data['ear'].mean()
    data['dif'] = round((mean-data['ear'])/mean,2)*100
    data['dif1'] = data['dif']
    for i in range(data.shape[0]):
        if i==0:
            a = data.iloc[i+1,-3]
            b = data.iloc[i,-3]
            c = data.iloc[i+2,-3]
            data.iloc[i,-1] = abs(a-b)+abs(b-c)
        elif i==(data.shape[0]-1):
            a = data.iloc[i-1,-3]
            b = data.iloc[i,-3]
            c = data.iloc[i-2,-3]
            data.iloc[i,-1] = abs(a-b)+abs(b-c)
        else:
            a = data.iloc[i-1,-3]
            b = data.iloc[i,-3]
            c = data.iloc[i+1,-3]
            data.iloc[i,-1] = abs(a-b)+abs(b-c)
    L = []
    for i in range (data.shape[0]):
        if data.iloc[i,-1] >= 300000 and data.iloc[i,-2] >0:
            year = data.iloc[i,0]
            a = [f'{p}',year]
            L.append(a)
    return data,L

df1,L1 = readdata('s1')
df2,L2 = readdata('s2')
df3,L3 = readdata('sn')
df4,L4 = readdata('f')
df5,L5 = readdata('w')
L_all = L1+L2+L3+L4+L5


# 輸入區
# model = 'MIROC-ESM'
RCP = 'rcp45'
loc = 337
list_plant = {'s1':'0204','s2':'0306','sn':'0506','f':'0808','w':'1107'}
def drowraning(p,y):
    plant_time = list_plant[p]
    year = y     # 2029, 2044, 2054
    day_range = 30
    # =============================================================================
    
    
    file1 = fr'G:\Maize stage future\{model}\*\{RCP}_{year}*'
    
    list_time = [f for f in glob.glob(file1) if plant_time in f ]
    df_time = pd.read_csv(list_time[0],encoding = 'BIG5')
    df_time = df_time[(df_time['ID']==loc)]
    month,day = plant_time[:2],plant_time[2:]
    time_start = pd.to_datetime(f'{year}/{month}/{day}')
    time_end= pd.to_datetime(df_time.iloc[0,5]) + timedelta(days=day_range)
    time_flower = pd.to_datetime(df_time.iloc[0,3])
    # time_end= time_start + timedelta(days=day_range)
    
    file2 = fr'G:\TCCIP統計降尺度日資料_AR5\AR5_統計降尺度_日資料_南部_降雨量\AR5_統計降尺度_日資料_南部_降雨量_{RCP}_{model}*'
    list_model = [f for f in glob.glob(file2) if str(year) in f ]
    list_model = [f for f in list_model if f.split('_')[-2] == model]
    
    list_model_1 = [f for f in glob.glob(file2) if str(year+1) in f ]
    list_model_1 = [f for f in list_model_1 if f.split('_')[-2] == model]
    
    df_model = pd.read_csv(list_model[0],index_col=False)
    df_model = df_model[(df_model[' LON']==df_time.iloc[0,1])]
    df_model = df_model[(df_model[' LAT']==df_time.iloc[0,2])]
    df_model = df_model.iloc[0,2:]
    df_model.index = pd.DatetimeIndex(df_model.index)
    df_model.index = pd.date_range('2022/1/1', '2022/12/31').strftime('%j')
    
    df_model_1 = pd.read_csv(list_model_1[0],index_col=False)
    df_model_1 = df_model_1[(df_model_1[' LON']==df_time.iloc[0,1])]
    df_model_1 = df_model_1[(df_model_1[' LAT']==df_time.iloc[0,2])]
    df_model_1 = df_model_1.iloc[0,2:]
    df_model_1.index = pd.DatetimeIndex(df_model_1.index)
    df_model_1.index = pd.date_range('2023/1/1', '2023/12/31').strftime('%j')
    
    df_model = pd.concat([df_model,df_model_1])
    
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
    xaxis = [drow.index[plant_time] for plant_time in range(0,len(drow.index),7)]
    plt.xticks(xaxis,rotation =60)
    title_name = f'NO.{loc}    modle : {model}\n{year} 與2020降雨量差異'
    plt.title(title_name)
    plt.ylabel('降雨量 (mm)')
    num_model = round(np.sum(drow['model']),2)
    num_his = round(np.sum(drow['his']),2)
    days = (time_end-time_start).days
    plt.xlabel(f'\n觀測期間：{time1_1}-{time1_2} ({days} days)             開花時間：{time1_3}\n累積雨量-模型(mm)： {num_model}\n累積雨量-歷史(mm)： {num_his}',loc='left',size = 12)
    plt.axvline(x=time_flower.strftime('%m/%d'),ymin=0,color = 'Red')
    plt.legend(loc= 'upper left')
    plt.tight_layout()
    # plt.savefig(fr'G:\Maize stage future\_report\{loc}_{model}_{RCP}_{year}_{plant_time}.png', bbox_inches='tight',transparent=True)

for i in L_all:
    p,y = i
    drowraning(p,y)
