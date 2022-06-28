# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 16:26:49 2022

@author: CCW
"""
import os
import glob
import pandas as pd
import shutil

# =============================================================================
# 輸入
site = 'grd258'
model = 'bcc-csm1-1'
rcp = 'rcp45'
year = '2029'
start = '02/20'
fertilizer1 = '03/04'
sowing = '03/06'
fertilizer2 = '04/05'
end = '08/30'
path = r'C:\Users\TARI\Documents\CLASSIM\run\124'
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
