# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 14:40:38 2021

@author: WIN10
"""

import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# import glob

# In[]      <<< 一鍵懶人包 >>>

#L = glob.glob(r'C:\Users\WIN10\Desktop\香菇高光譜數據提取\*.csv')
# df = pd.concat([pd.read_csv(f) for f in L])
# df.reset_index(inplace=True)
# df.to_csv(r'C:\Users\WIN10\Desktop\香菇高光譜數據提取\123.txt',sep='\t',index=False)


# In[]
files1 = r'C:\Users\WIN10\Desktop\香菇高光譜數據提取\1102111378-2_C.csv'
files2 = r'C:\Users\WIN10\Desktop\香菇高光譜數據提取\1102111378_C.csv'
files3 = r'C:\Users\WIN10\Desktop\香菇高光譜數據提取\1102111503_V.csv'
files4 = r'C:\Users\WIN10\Desktop\香菇高光譜數據提取\1102111531_C.csv'
files5 = r'C:\Users\WIN10\Desktop\香菇高光譜數據提取\1102112320_JK.csv'
files6 = r'C:\Users\WIN10\Desktop\香菇高光譜數據提取\1102112352_CV.csv'
files7 = r'C:\Users\WIN10\Desktop\香菇高光譜數據提取\1102112366_CV.csv'
files8 = r'C:\Users\WIN10\Desktop\香菇高光譜數據提取\1102112379_J, K.csv'

df1 = pd.read_csv(files1)
# df1.to_csv(files1,index=False)
df2 = pd.read_csv(files2)
df3 = pd.read_csv(files3)
df4 = pd.read_csv(files4)
df5 = pd.read_csv(files5)
df6 = pd.read_csv(files6)
df7 = pd.read_csv(files6)
df8 = pd.read_csv(files8)

# In[]   <<<合併>>>           會很久
df_all = pd.concat([df1,df2,df3,df4,df5,df6,df7,df8],axis=0)


