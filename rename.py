# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 14:37:13 2022

@author: Chia-Wei Wang
"""

import glob
import os

# 輸入區
# 設定要執行之資料夾的資料夾路徑，最後請用\\結尾
filename = r'C:\Users\acer\Desktop\HW\\'
find = 'data'

# 執行區
path = filename
# 純粹好看不想結尾有\\，而是\
path = path[:-1]
# 取得資料夾下的個別資料夾名稱，也就是得到檔案名
fileList = os.listdir(path)

for i in range(len(fileList)):
    # 取得要命名之檔名
    name = fileList[i]
    
    # 取得要改寫檔明知檔案
    L = glob.glob(path+name+'\\'+find+'*.*')
    
    for j in range(len(L)):
        # 原先的完整路徑
        oldname = L[j]
        # 取得副檔名
        (file,extension) = os.path.splitext(oldname)
        # 命名新黨名與路徑
        newname = path+name+'\\'+name+extension
        # 改寫
        os.rename(oldname,newname)
