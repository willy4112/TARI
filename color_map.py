# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 16:16:20 2022

@author: Chai-Wei Waang
"""

import pandas as pd
import numpy as np
# import pylab as pl
import matplotlib.pyplot as plt
# from matplotlib.colors import hsv_to_rgb
import colorsys
# import seaborn as sns

# V, H = np.mgrid[0:1:100j, 0:1:360j]
# S = np.ones_like(V)*1   # 設定0-1之間
# HSV = np.dstack((H,S,V))
# RGB = hsv_to_rgb(HSV)
# pl.imshow(RGB, origin="lower", extent=[0, 360, 0, 1], aspect=150)
# pl.xlabel("H")
# pl.ylabel("V")
# pl.title("$S_{HSV}=0.1$")
# pl.show()


X = []
Y = []
C = []

number = 60
s =  0.75         # 0.75-0.5


table = np.ones((10,number))
table = pd.DataFrame(table)
for i in range(10):
    for j in range(number):
        v = round(i/10,2)
        h = round(j/number,2)
        # hsv = str((h,s,v))
        (r,g,b) = colorsys.hsv_to_rgb(h,s,v)
        r = hex(int(r*255))[2:].zfill(2)
        g = hex(int(g*255))[2:].zfill(2)
        b = hex(int(b*255))[2:].zfill(2)
        rgb = "#"+r+g+b
        table.iloc[i,j] = rgb
        X.append(j)
        Y.append(i)
        C.append(rgb)

# plt.figure(figsize=[10,3])
# plt.scatter(X, Y, s=200, color = C, marker="s")
# plt.title("$V_{HSV}=$"+str(v))
# plt.show()


L = [1]*number

# C0 = list(table.iloc[0,:])
# C1 = list(table.iloc[1,:])
# C2 = list(table.iloc[2,:])
# C3 = list(table.iloc[3,:])
# C4 = list(table.iloc[4,:])
# C5 = list(table.iloc[5,:])
# C6 = list(table.iloc[6,:])
# C7 = list(table.iloc[7,:])
# C8 = list(table.iloc[8,:])
# C9 = list(table.iloc[9,:])

# plt.pie(L, wedgeprops={'width': 0.50},colors=list(table.iloc[0,:]))
# plt.pie(L, wedgeprops={'width': 0.45},colors=list(table.iloc[1,:]))
# plt.pie(L, wedgeprops={'width': 0.40},colors=list(table.iloc[2,:]))
# plt.pie(L, wedgeprops={'width': 0.35},colors=list(table.iloc[3,:]))
# plt.pie(L, wedgeprops={'width': 0.30},colors=list(table.iloc[4,:]))
# plt.pie(L, wedgeprops={'width': 0.25},colors=list(table.iloc[5,:]))
# plt.pie(L, wedgeprops={'width': 0.20},colors=list(table.iloc[6,:]))
# plt.pie(L, wedgeprops={'width': 0.15},colors=list(table.iloc[7,:]))
# plt.pie(L, wedgeprops={'width': 0.10},colors=list(table.iloc[8,:]))
plt.pie(L, wedgeprops={'width': 0.3},colors=list(table.iloc[9,:]))
plt.title("$S_{HSV}=$"+str(s))
plt.show()

#%% 取出顏色

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import colorsys

Number = 360
S = 0.75
V = 0.9
start = 0
color_number = 3


color_list = np.ones((1,Number))
color_list = pd.DataFrame(color_list)
for i in range(Number):
    H = round(i/Number,2)
    (r,g,b) = colorsys.hsv_to_rgb(H,S,V)
    r = hex(int(r*255))[2:].zfill(2)
    g = hex(int(g*255))[2:].zfill(2)
    b = hex(int(b*255))[2:].zfill(2)
    rgb = "#"+r+g+b
    color_list.iloc[0,i] = rgb


X1 = []
Y1 = [1]*color_number
C1 = []

for i in range(color_number):
    X1.append(i)
    location = (start%Number+int(Number/color_number)*i)%Number
    C1.append(color_list.iloc[0,location])

plt.pie(Y1,colors=C1)
