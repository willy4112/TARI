# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 09:50:26 2022

@author: CWW
"""
#%% 給Headwall用

# =============================================================================
# data type = 4 is 4-byte floating point
# =============================================================================

import numpy as np
import cv2
import pandas as pd
import glob
import time

start = time.time()

path = r'C:\Users\Thermo-IRMS\Desktop\hyperfine\Headwall_400-1700'

fileList = glob.glob(str(path+'\*bil'))
for i in fileList:
    name,a = i.split('.')
    print(name)
    
    imagePath = name+'.bil'
    rawImage = np.fromfile(imagePath,'float32')
    rawShap = rawImage.shape
    
    samples = 638
    lines = 466
    bands = 268
    
    formatImage = np.zeros((lines,samples,bands))
    for row in range(0,lines): #line
        for dim in range(0,bands): # bands
            formatImage[row,:,dim] = rawImage[(dim + row*bands) * samples :(dim + 1 + row * bands)*samples]
    
    # 調整提取RGB的波段
    imgR = formatImage[:,:,60]*256 #60
    imgG = formatImage[:,:,80]*256 #85
    imgB = formatImage[:,:,240]*256 #170
    
    # 將RGB從0-1轉成256，並將儲存格是修改
    rgbImg = cv2.merge([imgR,imgG,imgB]).astype(int)
    rgbImg = np.array(rgbImg, dtype=np.uint8)
    # 測試影像是否正常
    cv2.imwrite(name+'.jpg', rgbImg)
    
    '''
    # 設定遮罩數值用
    def empty(v):
        pass
    
    cv2.namedWindow('TrackBar')
    cv2.resizeWindow('TrackBar', 640, 320)
    
    cv2.createTrackbar('Hue Min', 'TrackBar', 0, 179, empty)
    cv2.createTrackbar('Hue Max', 'TrackBar', 179, 179, empty)
    cv2.createTrackbar('Sat Min', 'TrackBar', 0, 255, empty)
    cv2.createTrackbar('Sat Max', 'TrackBar', 255, 255, empty)
    cv2.createTrackbar('Val Min', 'TrackBar', 0, 255, empty)
    cv2.createTrackbar('Val Max', 'TrackBar', 255, 255, empty)
    
    
    hsv = cv2.cvtColor(rgbImg, cv2.COLOR_BGR2HSV)
    while True:
        h_min = cv2.getTrackbarPos('Hue Min', 'TrackBar')
        h_max = cv2.getTrackbarPos('Hue Max', 'TrackBar')
        s_min = cv2.getTrackbarPos('Sat Min', 'TrackBar')
        s_max = cv2.getTrackbarPos('Sat Max', 'TrackBar')
        v_min = cv2.getTrackbarPos('Val Min', 'TrackBar')
        v_max = cv2.getTrackbarPos('Val Max', 'TrackBar')
        # print(h_min, h_max, s_min, s_max, v_min, v_max)
    
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
    
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(rgbImg, rgbImg, mask=mask)
    
        cv2.imshow('img', rgbImg)
        cv2.imshow('hsv', hsv)
        cv2.imshow('mask', mask)
        cv2.imshow('reslut', result)
        cv2.waitKey(1)
       
        
    '''
    # 設定mask遮罩，取出香菇
    hsv = cv2.cvtColor(rgbImg, cv2.COLOR_BGR2HSV)
    lower1 = np.array([19, 80, 0])
    upper1 = np.array([55, 163, 255])
    mask1 = cv2.inRange(hsv, lower1, upper1)
    # 設定mask遮罩，取出陰影
    lower2 = np.array([0, 0, 0])
    upper2 = np.array([179, 255, 170])
    mask2 = cv2.inRange(hsv, lower2, upper2)
    
    mask = cv2.bitwise_or(mask1,mask2)
    
    
    # 將mask反轉
    (t,mask_t) = cv2.threshold(mask, 155, 255, cv2.THRESH_BINARY_INV)
    result = cv2.bitwise_and(rgbImg, rgbImg, mask=mask_t)
    # 測試影像是否正常
    cv2.imwrite(name+'_mask.jpg', result)
    
    # cv2.imshow('img', rgbImg)
    # cv2.imshow('hsv', hsv)
    # cv2.imshow('mask1', mask1)
    # cv2.imshow('mask2', mask2)
    # cv2.imshow('mask', mask)
    # cv2.imshow('reslut', result)
    # cv2.waitKey(1)
    
    # cv2.imshow('show',rgbImg)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    mask_data = mask_t/255
        
    # (x,y) = mask_data.shape
    
    # location = []
    # for row in range(0,x):
    #     for dim in range(0,y):
    #         if mask_data[row,dim] == 1.0 :
    #             loc = [row,dim]
    #             location.append(loc)
    #         else:
    #             pass
    
    # lis_data_n = []
    
    # for x,y in location:
    #     L = list(formatImage[x,y])
    #     lis_data_n.append(L)
    #     # print(x,y)
    
    # data = np.array(lis_data_n)
    
    
    mask_data_n = mask_data[:,:, np.newaxis]
    data = mask_data_n*formatImage
    data = data.reshape(lines*samples,bands)
    data = data[~np.all(data == 0, axis=1)]
    
    wavelength = [598.855 ,602.985 ,607.114 ,611.244 ,615.374 ,619.504 ,623.633 ,627.763 ,631.893 ,636.022 ,640.152 ,644.282 ,648.412 ,652.541 ,656.671 ,660.801 ,664.93 ,669.06 ,673.19 ,677.32 ,681.449 ,685.579 ,689.709 ,693.839 ,697.968 ,702.098 ,706.228 ,710.357 ,714.487 ,718.617 ,722.747 ,726.876 ,731.006 ,735.136 ,739.265 ,743.395 ,747.525 ,751.655 ,755.784 ,759.914 ,764.044 ,768.174 ,772.303 ,776.433 ,780.563 ,784.692 ,788.822 ,792.952 ,797.082 ,801.211 ,805.341 ,809.471 ,813.6 ,817.73 ,821.86 ,825.99 ,830.119 ,834.249 ,838.379 ,842.508 ,846.638 ,850.768 ,854.898 ,859.027 ,863.157 ,867.287 ,871.417 ,875.546 ,879.676 ,883.806 ,887.935 ,892.065 ,896.195 ,900.325 ,904.454 ,908.584 ,912.714 ,916.843 ,920.973 ,925.103 ,929.233 ,933.362 ,937.492 ,941.622 ,945.752 ,949.881 ,954.011 ,958.141 ,962.27 ,966.4 ,970.53 ,974.66 ,978.789 ,982.919 ,987.049 ,991.178 ,995.308 ,999.438 ,1003.57 ,1007.7 ,1011.83 ,1015.96 ,1020.09 ,1024.22 ,1028.35 ,1032.48 ,1036.61 ,1040.74 ,1044.86 ,1048.99 ,1053.12 ,1057.25 ,1061.38 ,1065.51 ,1069.64 ,1073.77 ,1077.9 ,1082.03 ,1086.16 ,1090.29 ,1094.42 ,1098.55 ,1102.68 ,1106.81 ,1110.94 ,1115.07,1119.2 ,1123.33 ,1127.46 ,1131.59 ,1135.72 ,1139.85 ,1143.98 ,1148.11 ,1152.24 ,1156.37 ,1160.5 ,1164.63 ,1168.76 ,1172.89 ,1177.02 ,1181.15 ,1185.28 ,1189.41 ,1193.53 ,1197.66 ,1201.79 ,1205.92 ,1210.05 ,1214.18 ,1218.31 ,1222.44 ,1226.57 ,1230.7 ,1234.83 ,1238.96 ,1243.09 ,1247.22 ,1251.35 ,1255.48 ,1259.61 ,1263.74 ,1267.87 ,1272 ,1276.13 ,1280.26 ,1284.39 ,1288.52 ,1292.65 ,1296.78 ,1300.91 ,1305.04 ,1309.17 ,1313.3 ,1317.43 ,1321.56 ,1325.69 ,1329.82 ,1333.95 ,1338.08 ,1342.2 ,1346.33 ,1350.46 ,1354.59 ,1358.72 ,1362.85 ,1366.98 ,1371.11 ,1375.24 ,1379.37 ,1383.5 ,1387.63 ,1391.76 ,1395.89 ,1400.02 ,1404.15 ,1408.28 ,1412.41 ,1416.54 ,1420.67 ,1424.8 ,1428.93 ,1433.06 ,1437.19 ,1441.32 ,1445.45 ,1449.58 ,1453.71 ,1457.84 ,1461.97 ,1466.1 ,1470.23 ,1474.36 ,1478.49 ,1482.62 ,1486.75 ,1490.87 ,1495 ,1499.13 ,1503.26 ,1507.39 ,1511.52 ,1515.65 ,1519.78 ,1523.91 ,1528.04 ,1532.17 ,1536.3 ,1540.43 ,1544.56 ,1548.69 ,1552.82 ,1556.95 ,1561.08 ,1565.21 ,1569.34 ,1573.47 ,1577.6 ,1581.73 ,1585.86 ,1589.99 ,1594.12 ,1598.25 ,1602.38 ,1606.51 ,1610.64 ,1614.77 ,1618.9 ,1623.03 ,1627.16 ,1631.29 ,1635.42 ,1639.54 ,1643.67 ,1647.8 ,1651.93 ,1656.06 ,1660.19 ,1664.32 ,1668.45 ,1672.58 ,1676.71 ,1680.84 ,1684.97 ,1689.1 ,1693.23 ,1697.36 ,1701.49]
    reoprt = pd.DataFrame(data,columns=wavelength)
    reoprt.to_csv(name+'.csv',header=True,index=False,encoding='utf-8-sig')
    
end = time.time()
print(end - start)



#%% 給Resonon用
'''
data type = 12 is 2-byte unsigned
'''

import numpy as np
import cv2
import pandas as pd
import glob


path = r'C:\Users\Thermo-IRMS\Desktop\hyperfine\Resonon_400-1000'

fileList = glob.glob(str(path+'\*bil'))
for i in fileList:
    name,a = i.split('.')
    print(name)
    
    imagePath = name+'.bil'
    rawImage = np.fromfile(imagePath,'int16')
    rawImage = rawImage/10000
    rawShap = rawImage.shape
    
    lines = 930
    samples = 900
    bands = 300
    
    formatImage = np.zeros((lines,samples,bands))
    for row in range(0,lines): #line
        for dim in range(0,bands): # bands
            formatImage[row,:,dim] = rawImage[(dim + row*bands) * samples :(dim + 1 + row * bands)*samples]
    # 調整提取RGB的波段
    imgR = formatImage[:,:,23]*256
    imgG = formatImage[:,:,76]*256
    imgB = formatImage[:,:,150]*256
    
    
    # 將RGB從0-1轉成256，並將儲存格是修改
    rgbImg = cv2.merge([imgR,imgG,imgB]).astype(int)
    rgbImg = np.array(rgbImg, dtype=np.uint8)
    # 測試影像是否正常
    cv2.imwrite(name+'.jpg', rgbImg)
    
    '''
    # 設定遮罩數值用
    def empty(v):
        pass
    
    cv2.namedWindow('TrackBar')
    cv2.resizeWindow('TrackBar', 640, 320)
    
    cv2.createTrackbar('Hue Min', 'TrackBar', 0, 179, empty)
    cv2.createTrackbar('Hue Max', 'TrackBar', 179, 179, empty)
    cv2.createTrackbar('Sat Min', 'TrackBar', 0, 255, empty)
    cv2.createTrackbar('Sat Max', 'TrackBar', 255, 255, empty)
    cv2.createTrackbar('Val Min', 'TrackBar', 0, 255, empty)
    cv2.createTrackbar('Val Max', 'TrackBar', 255, 255, empty)
    
    
    hsv = cv2.cvtColor(rgbImg, cv2.COLOR_BGR2HSV)
    while True:
        h_min = cv2.getTrackbarPos('Hue Min', 'TrackBar')
        h_max = cv2.getTrackbarPos('Hue Max', 'TrackBar')
        s_min = cv2.getTrackbarPos('Sat Min', 'TrackBar')
        s_max = cv2.getTrackbarPos('Sat Max', 'TrackBar')
        v_min = cv2.getTrackbarPos('Val Min', 'TrackBar')
        v_max = cv2.getTrackbarPos('Val Max', 'TrackBar')
        # print(h_min, h_max, s_min, s_max, v_min, v_max)
    
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
    
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(rgbImg, rgbImg, mask=mask)
    
        cv2.imshow('img', rgbImg)
        cv2.imshow('hsv', hsv)
        cv2.imshow('mask', mask)
        cv2.imshow('reslut', result)
        cv2.waitKey(1)
    '''
    # 設定mask遮罩，取出香菇
    hsv = cv2.cvtColor(rgbImg, cv2.COLOR_BGR2HSV)
    lower1 = np.array([25, 0, 0])
    upper1 = np.array([60, 255, 255])
    mask = cv2.inRange(hsv, lower1, upper1)
    
    # 將mask反轉
    (t,mask_t) = cv2.threshold(mask, 155, 255, cv2.THRESH_BINARY_INV)
    result = cv2.bitwise_and(rgbImg, rgbImg, mask=mask_t)
    # 測試影像是否正常
    cv2.imwrite(name+'_mask.jpg', result)
    
    mask_data = mask_t/255
    mask_data_n = mask_data[:,:, np.newaxis]
    data = mask_data_n*formatImage
    data = data.reshape(lines*samples,bands)
    data = data[~np.all(data == 0, axis=1)]
    
    wavelength = [389.42, 391.45, 393.48, 395.51, 397.54, 399.56, 401.59, 403.63, 405.66, 407.69, 409.72, 411.75, 413.79, 415.82, 417.86, 419.89, 421.93, 423.97, 426.0, 428.04, 430.08, 432.12, 434.16, 436.2, 438.24, 440.28, 442.32, 444.37, 446.41, 448.45, 450.5, 452.54, 454.59, 456.64, 458.68, 460.73, 462.78, 464.83, 466.88, 468.93, 470.98, 473.03, 475.08, 477.13, 479.19, 481.24, 483.3, 485.35, 487.41, 489.46, 491.52, 493.58, 495.63, 497.69, 499.75, 501.81, 503.87, 505.93, 507.99, 510.06, 512.12, 514.18, 516.25, 518.31, 520.38, 522.44, 524.51, 526.58, 528.64, 530.71, 532.78, 534.85, 536.92, 538.99, 541.06, 543.13, 545.21, 547.28, 549.35, 551.43, 553.5, 555.58, 557.66, 559.73, 561.81, 563.89, 565.97, 568.05, 570.13, 572.21, 574.29, 576.37, 578.45, 580.53, 582.62, 584.7, 586.79, 588.87, 590.96, 593.04, 595.13, 597.22, 599.31, 601.4, 603.48, 605.57, 607.67, 609.76, 611.85, 613.94, 616.03, 618.13, 620.22, 622.32, 624.41, 626.51, 628.61, 630.7, 632.8, 634.9, 637.0, 639.1, 641.2, 643.3, 645.4, 647.5, 649.61, 651.71, 653.82, 655.92, 658.03, 660.13, 662.24, 664.34, 666.45, 668.56, 670.67, 672.78, 674.89, 677.0, 679.11, 681.22, 683.34, 685.45, 687.56, 689.68, 691.79, 693.91, 696.02, 698.14, 700.26, 702.38, 704.49, 706.61, 708.73, 710.85, 712.98, 715.1, 717.22, 719.34, 721.47, 723.59, 725.71, 727.84, 729.97, 732.09, 734.22, 736.35, 738.48, 740.6, 742.73, 744.86, 746.99, 749.13, 751.26, 753.39, 755.52, 757.66, 759.79, 761.93, 764.06, 766.2, 768.34, 770.47, 772.61, 774.75, 776.89, 779.03, 781.17, 783.31, 785.45, 787.59, 789.74, 791.88, 794.03, 796.17, 798.32, 800.46, 802.61, 804.76, 806.9, 809.05, 811.2, 813.35, 815.5, 817.65, 819.8, 821.95, 824.11, 826.26, 828.41, 830.57, 832.72, 834.88, 837.03, 839.19, 841.35, 843.51, 845.67, 847.83, 849.99, 852.15, 854.31, 856.47, 858.63, 860.79, 862.96, 865.12, 867.29, 869.45, 871.62, 873.78, 875.95, 878.12, 880.29, 882.46, 884.63, 886.8, 888.97, 891.14, 893.31, 895.48, 897.66, 899.83, 902.0, 904.18, 906.36, 908.53, 910.71, 912.89, 915.06, 917.24, 919.42, 921.6, 923.78, 925.96, 928.15, 930.33, 932.51, 934.69, 936.88, 939.06, 941.25, 943.43, 945.62, 947.81, 950.0, 952.18, 954.37, 956.56, 958.75, 960.94, 963.14, 965.33, 967.52, 969.71, 971.91, 974.1, 976.3, 978.49, 980.69, 982.89, 985.08, 987.28, 989.48, 991.68, 993.88, 996.08, 998.28, 1000.48, 1002.68, 1004.89, 1007.09, 1009.3, 1011.5, 1013.71, 1015.91, 1018.12, 1020.33, 1022.53]
    reoprt = pd.DataFrame(data,columns=wavelength)
    reoprt.to_csv(name+'.csv',header=True,index=False,encoding='utf-8-sig')
