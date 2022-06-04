# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 16:24:52 2022

@author: Chia-Wei Wang
"""

import tkinter as tk
import Tomgro
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np



def calculate_LAI_number():
    LeafArea = float(LeafArea_entry.get())
    LAI_value = round(LeafArea/2/3*2.89/10000, 2)
    result = 'LAI 指數為：{} '.format(LAI_value)
    result_label.configure(text=result)

def Show_now():
    #%% 輸入區
    weaName = wea_obs_entry.get()       # 請更新觀測氣象檔
    weaName_history = wea_his_entry.get()
    outputName = "tomato_v0.csv"
    # initial condition
    plantingDate = plantDate_entry.get()              # 本次種植2021/10/12
    endDate = "2022/1/19"
    detect_leafarea = float(LeafArea_entry.get())                  # 請輸入從照片計算之葉面積(cm^2)


    dayStart = datetime.strptime(plantingDate,"%Y/%m/%d")
    dayEnd = datetime.strptime(endDate,"%Y/%m/%d")

    #%% 農場調查資料

    lia_farm1 = [417.2058,882.74,3555.947,10849.06,20136.02,28385.32,32495.34,37621.56,38911.94,41680.71,44064.12,45460.52,46811.19,49860.05]
    lis_lia_farm1 = np.array(lia_farm1)/12*2.98/10000
    lis_lia_farm1 = lis_lia_farm1.tolist()

    lis_datetime_lai_lab = [dt.datetime(2021,10,15,23),dt.datetime(2021,10,21,23),dt.datetime(2021,11,3,23),dt.datetime(2021,11,10,23),dt.datetime(2021,11,16,23),dt.datetime(2021,11,22,23),dt.datetime(2021,12,6,23),dt.datetime(2021,12,13,23),dt.datetime(2021,12,20,23),dt.datetime(2021,12,28,23)]
    lis_lia_lab = [0.01,0.04,0.29,0.5,0.53,0.63,1.01,0.8,1,1.14]

    fruit_farm = [(1158.5+1592.9)/2,(1946.7+2741.5)/2]
    lis_fruit_farm = np.array(fruit_farm)/12*2.98/1000
    lis_fruit_farm = lis_fruit_farm.tolist()

    #%% 跑當下數值
    # assign class
    mainStemNode = Tomgro.Node()
    Assimilate = Tomgro.Source(410,mainStemNode)
    Sink1 = Tomgro.Sink(mainStemNode)

    # initialize variable
    dailyPg = 0
    dailyRm = 0
    dailyGRnet = 0 
    dNdday = 0
    TempSum = 0
    TempDay = 0

    # initilize list for ploting
    lst_datetime = []
    lst_node = []
    lst_lai = []
    lst_DWtotal = []
    lst_DWfruit = []
    lst_DWmature = []
    lst_Pg = []
    lst_Rm = []


    with open (outputName, 'w',newline='') as csvwrite:
        writer = csv.writer(csvwrite, delimiter=',')
        header = ["Date","Node","LAI","AboveGroundDW","FruitDW","MatureFruitDW"] 
        writer.writerow(header)
        
        # reading weather file
        with open (weaName, newline='',encoding='utf-8') as csvfile:
            rows = csv.reader(csvfile)
            next(rows) # header or weather file
            
            for row in rows:
                dateTime = datetime.strptime(row[0]+":"+row[1], "%Y/%m/%d:%H")
                hour = int(row[1])
                if dateTime < dayStart or dateTime > dayEnd:
                    continue
                # if hour == 10:
                #     print(dateTime)
                temperature = float(row[2])
                if row[4] == "NA":
                    ppfd = 0
                else:
                    ppfd = float (row[4]) 
                
                # start calculate
                
                mainStemNode.update(temperature)
                # if hour == 10:
                #     #print(dateTime,Node1.dNdt,Node1.dLAIdt())
                #     print(dateTime,round(Node1.node,1), round(Node1.LAI,1))
                Assimilate.update(temperature,ppfd,mainStemNode,Sink1)
                # daily accumulation of sink and source addtion rate
                dailyPg += Assimilate.Pg
                dailyRm += Assimilate.Rm
                dailyGRnet += Assimilate.GRnet
                dNdday += mainStemNode.dNdt
                
                #calculate temperature
                # sumation here output at hour = 23 (end of the day)
                TempSum += temperature
                if hour >= 6 and hour <= 18:
                    TempDay += temperature
                # finishing sum temperature
                if hour == 23: 
                    # calculate source
                    
                    Td = TempSum/24
                    Tdaytime = TempDay/13
                    Sink1.update(Td,Tdaytime,mainStemNode,dNdday,dailyGRnet)
                    print(dateTime,round(Sink1.W,1),round(Sink1.Wf,1))

                    # write to table 
                    toWrite = [dateTime,mainStemNode.node,mainStemNode.LAI,Sink1.W,Sink1.Wf,Sink1.Wm]
                    toWrite.extend([dailyPg,dailyRm,dailyGRnet])
                    writer.writerow(toWrite)
                    
                    # prepare list for ploting
                    lst_datetime.append(dateTime)
                    lst_node.append(mainStemNode.node)
                    lst_lai.append(mainStemNode.LAI)
                    lst_DWtotal.append(Sink1.W)
                    lst_DWfruit.append(Sink1.Wf)
                    lst_DWmature.append(Sink1.Wm)
                    lst_Pg.append(dailyPg)
                    lst_Rm.append(dailyRm)
                    
                    # reinitialized variable into 0
                    TempSum = 0
                    TempDay = 0
                    dailyPg = 0
                    dailyRm = 0
                    dailyGRnet = 0
                    dNdday = 0

    # %% 跑歷史值用
    # assign class
    mainStemNode = Tomgro.Node()
    Assimilate = Tomgro.Source(410,mainStemNode)
    Sink1 = Tomgro.Sink(mainStemNode)

    # initialize variable
    dailyPg = 0
    dailyRm = 0
    dailyGRnet = 0 
    dNdday = 0
    TempSum = 0
    TempDay = 0

    # initilize list for ploting
    lst_datetime = []
    lst_node = []
    lst_lai = []
    lst_DWtotal = []
    lst_DWfruit = []
    lst_DWmature = []
    lst_Pg = []
    lst_Rm = []


    with open (outputName, 'w',newline='') as csvwrite:
        writer = csv.writer(csvwrite, delimiter=',')
        header = ["Date","Node","LAI","AboveGroundDW","FruitDW","MatureFruitDW"] 
        writer.writerow(header)
        
        # reading weather file
        with open (weaName, newline='',encoding='utf-8') as csvfile:
            rows = csv.reader(csvfile)
            next(rows) # header or weather file
            
            for row in rows:
                dateTime = datetime.strptime(row[0]+":"+row[1], "%Y/%m/%d:%H")
                hour = int(row[1])
                if dateTime < dayStart or dateTime > dayEnd:
                    continue
                # if hour == 10:
                #     print(dateTime)
                temperature = float(row[2])
                if row[4] == "NA":
                    ppfd = 0
                else:
                    ppfd = float (row[4]) 
                
                # start calculate
                
                mainStemNode.update(temperature)
                # if hour == 10:
                #     #print(dateTime,Node1.dNdt,Node1.dLAIdt())
                #     print(dateTime,round(Node1.node,1), round(Node1.LAI,1))
                Assimilate.update(temperature,ppfd,mainStemNode,Sink1)
                # daily accumulation of sink and source addtion rate
                dailyPg += Assimilate.Pg
                dailyRm += Assimilate.Rm
                dailyGRnet += Assimilate.GRnet
                dNdday += mainStemNode.dNdt
                
                #calculate temperature
                # sumation here output at hour = 23 (end of the day)
                TempSum += temperature
                if hour >= 6 and hour <= 18:
                    TempDay += temperature
                # finishing sum temperature
                if hour == 23: 
                    # calculate source
                    
                    Td = TempSum/24
                    Tdaytime = TempDay/13
                    Sink1.update(Td,Tdaytime,mainStemNode,dNdday,dailyGRnet)
                    print(dateTime,round(Sink1.W,1),round(Sink1.Wf,1))

                    # write to table 
                    toWrite = [dateTime,mainStemNode.node,mainStemNode.LAI,Sink1.W,Sink1.Wf,Sink1.Wm]
                    toWrite.extend([dailyPg,dailyRm,dailyGRnet])
                    writer.writerow(toWrite)
                    
                    # prepare list for ploting
                    lst_datetime.append(dateTime)
                    lst_node.append(mainStemNode.node)
                    lst_lai.append(mainStemNode.LAI)
                    lst_DWtotal.append(Sink1.W)
                    lst_DWfruit.append(Sink1.Wf)
                    lst_DWmature.append(Sink1.Wm)
                    lst_Pg.append(dailyPg)
                    lst_Rm.append(dailyRm)
                    
                    # reinitialized variable into 0
                    TempSum = 0
                    TempDay = 0
                    dailyPg = 0
                    dailyRm = 0
                    dailyGRnet = 0
                    dNdday = 0

    # 開始計算歷史部分
    # initialize variable
    dailyPg_his = 0
    dailyRm_his = 0
    dailyGRnet_his = 0 
    dNdday_his = 0
    TempSum = 0
    TempDay = 0

    # initilize list for ploting
    lst_datetime_his = []
    lst_node_his = []
    lst_lai_his = []
    lst_DWtotal_his = []
    lst_DWfruit_his = []
    lst_DWmature_his = []
    lst_Pg_his = []
    lst_Rm_his = []

    dayStart_his = datetime.strptime(row[0] ,"%Y/%m/%d")

    with open (outputName, 'w',newline='') as csvwrite:
        writer = csv.writer(csvwrite, delimiter=',')
        header = ["Date","Node","LAI","AboveGroundDW","FruitDW","MatureFruitDW"] 
        writer.writerow(header)
        
        # reading weather file
        with open (weaName_history, newline='',encoding='utf-8') as csvfile:
            rows = csv.reader(csvfile)
            next(rows) # header or weather file
            
            for row in rows:
                dateTime = datetime.strptime(row[0]+":"+row[1], "%Y/%m/%d:%H")
                hour = int(row[1])
                if dateTime < dayStart_his or dateTime > dayEnd:
                    continue
                # if hour == 10:
                #     print(dateTime)
                temperature = float(row[2])
                if row[4] == "NA":
                    ppfd = 0
                else:
                    ppfd = float (row[4]) 
                
                # start calculate
                
                mainStemNode.update(temperature)
                # if hour == 10:
                #     #print(dateTime,Node1.dNdt,Node1.dLAIdt())
                #     print(dateTime,round(Node1.node,1), round(Node1.LAI,1))
                Assimilate.update(temperature,ppfd,mainStemNode,Sink1)
                # daily accumulation of sink and source addtion rate
                dailyPg_his += Assimilate.Pg
                dailyRm_his += Assimilate.Rm
                dailyGRnet_his += Assimilate.GRnet
                dNdday_his += mainStemNode.dNdt
                
                #calculate temperature
                # sumation here output at hour = 23 (end of the day)
                TempSum += temperature
                if hour >= 6 and hour <= 18:
                    TempDay += temperature
                # finishing sum temperature
                if hour == 23: 
                    # calculate source
                    
                    Td = TempSum/24
                    Tdaytime = TempDay/13
                    Sink1.update(Td,Tdaytime,mainStemNode,dNdday_his,dailyGRnet_his)
                    print(dateTime,round(Sink1.W,1),round(Sink1.Wf,1))

                    # write to table 
                    toWrite = [dateTime,mainStemNode.node,mainStemNode.LAI,Sink1.W,Sink1.Wf,Sink1.Wm]
                    toWrite.extend([dailyPg_his,dailyRm_his,dailyGRnet_his])
                    writer.writerow(toWrite)
                    
                    # prepare list for ploting
                    lst_datetime_his.append(dateTime)
                    lst_node_his.append(mainStemNode.node)
                    lst_lai_his.append(mainStemNode.LAI)
                    lst_DWtotal_his.append(Sink1.W)
                    lst_DWfruit_his.append(Sink1.Wf)
                    lst_DWmature_his.append(Sink1.Wm)
                    lst_Pg_his.append(dailyPg_his)
                    lst_Rm_his.append(dailyRm_his)
                    
                    # reinitialized variable into 0
                    TempSum = 0
                    TempDay = 0
                    dailyPg_his = 0
                    dailyRm_his = 0
                    dailyGRnet_his = 0
                    dNdday_his = 0


    #%% 繪圖區1-各種指標
    # ploting 
    plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=[15,7],dpi=125)
    plt.subplot(221)
    plt.plot(lst_datetime,lst_lai)
    plt.ylabel('葉面積指數')
    plt.title('葉面積指數變化')

    plt.subplot(222)
    plt.plot(lst_datetime,lst_node)
    plt.ylabel('主幹節數')
    plt.title('主幹節數變化')

    plt.subplot(223)
    plt.plot(lst_datetime,lst_DWtotal,label='地上部乾重')
    plt.plot(lst_datetime,lst_DWfruit, label='果實乾重')
    plt.plot(lst_datetime,lst_DWmature, label='成熟果實乾重')
    plt.legend()
    plt.ylabel('乾物質重 (g/m$^{2}$)')
    plt.title('乾物質變化')

    plt.subplot(224)
    plt.plot(lst_datetime, lst_Pg, label='總光合作用')
    plt.plot(lst_datetime, lst_Rm, label='呼吸作用')
    plt.legend()
    plt.title('碳平衡')
    plt.ylabel('速率(µmol m$^{-2}$ s$^{-1}$)')
    plt.tight_layout()
    plt.show()                


    #%% 計算每周鮮重&及時偵測的LAI
    # 增加每周為單位的列表，以每七天為單位，目前的輸出是乾重，要乘上水分含量
    # 才會得到鮮重的資料

    deltaDay = 7 # weekly
    counter = 0
    wk_date = [] # list for weekly date
    wk_DWmature = [] # list for weekly mature fruit weight
    fruitDW0 = 0 # set the initial condition of fruit weight to 0

    for d in range(len(lst_DWmature)):
        if counter%deltaDay == 0:
            wk_date.append( lst_datetime[d])
            fruitDW1 = lst_DWmature[d]
            deltaFruitDW = max(0,fruitDW1 - fruitDW0) # weekly accumulated
            deltaFruitFW = deltaFruitDW*20/1000 #假設水分含量95%，換算成kg/m2
            wk_DWmature.append(deltaFruitFW)
            fruitDW0 = fruitDW1 # pass到舊的fruitDW，作為下周的基礎
            
        counter += 1

    counter = 0
    wk_date_his = []
    wk_DWmature_his = []
    fruitDW0_his = lst_DWmature[-7]

    # 歷史平均值
    for d in range(len(lst_DWmature_his)):
        if counter%deltaDay == 0:
            wk_date_his.append( lst_datetime_his[d])
            fruitDW1_his = lst_DWmature_his[d]
            deltaFruitDW_his = max(0,fruitDW1_his - fruitDW0_his)
            deltaFruitFW_his = deltaFruitDW_his*20/1000
            wk_DWmature_his.append(deltaFruitFW_his)
            fruitDW0_his = fruitDW1_his

        counter += 1


    # 加入現在最後值到歷史模擬中
    wk_date_his.insert(0, wk_date[-1])
    wk_DWmature_his.insert(0, wk_DWmature[-1])
    
    Year = int(Year_entry.get())
    Month = int(Month_entry.get())
    Day = int(Day_entry.get())

    detect_datetime = dt.datetime(Year, Month, Day)
    detect_LAI = detect_leafarea/6*2.89/10000


    #%% 繪圖區2-葉面積指數&每周鮮重
            
    plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=[10,7.5],dpi=120)

    plt.subplot(211)

    plt.scatter(detect_datetime,detect_LAI,label='detect',color="#FF1100")
    # plt.text(detect_datetime,detect_LAI-0.25,round(detect_LAI,2),horizontalalignment='center',size = 24)
    plt.plot(lst_datetime_his,lst_lai_his,label='history',color = "#C0C0C0")
    plt.plot(lst_datetime,lst_lai,label='now',linewidth=3)
    # plt.plot(lis_datetime_lai,lis_lia_farm1,label='farm1',marker='o')
    plt.plot(lis_datetime_lai_lab,lis_lia_lab,label='Lab',marker='o',linestyle=' ')
    plt.annotate(round(detect_LAI,2), xy=(detect_datetime, detect_LAI-0.1), xytext=(detect_datetime, detect_LAI-0.5),
                xycoords='data',arrowprops=dict(facecolor='black', shrink=0.05),horizontalalignment='center',size = 24)

    plt.legend()
    plt.ylabel('葉面積指數')
    plt.title('葉面積指數變化')
    plt.subplot(212)


    plt.plot(wk_date, wk_DWmature,label='now',linewidth=3,marker='o')
    # plt.plot(lis_datetime_fruit, lis_fruit_farm,label='farm',marker='o')
    plt.legend()
    plt.ylabel('每周鮮重 (kg/m2)')
    plt.title('每周產量')
    plt.tight_layout()
    plt.show()

def Show_future():
        #%% 輸入區
    weaName = wea_obs_entry.get()       # 請更新觀測氣象檔
    weaName_history = wea_his_entry.get()
    outputName = "tomato_v0.csv"
    # initial condition
    plantingDate = plantDate_entry.get()              # 本次種植2021/10/12
    endDate = endDate_entry.get()
    Range_temperature = int(temperature_scale.get())                    # 輸入預計變化的溫度
    
    
    dayStart = datetime.strptime(plantingDate,"%Y/%m/%d")
    dayEnd = datetime.strptime(endDate,"%Y/%m/%d")
    
    #%% 跑當下數值
    # assign class
    mainStemNode = Tomgro.Node()
    Assimilate = Tomgro.Source(410,mainStemNode)
    Sink1 = Tomgro.Sink(mainStemNode)
    
    # initialize variable
    dailyPg = 0
    dailyRm = 0
    dailyGRnet = 0 
    dNdday = 0
    TempSum = 0
    TempDay = 0
    
    # initilize list for ploting
    lst_datetime = []
    lst_node = []
    lst_lai = []
    lst_DWtotal = []
    lst_DWfruit = []
    lst_DWmature = []
    lst_Pg = []
    lst_Rm = []
    
    
    
    
    with open (outputName, 'w',newline='') as csvwrite:
        writer = csv.writer(csvwrite, delimiter=',')
        header = ["Date","Node","LAI","AboveGroundDW","FruitDW","MatureFruitDW"] 
        writer.writerow(header)
        
        # reading weather file
        with open (weaName, newline='',encoding='utf-8') as csvfile:
            rows = csv.reader(csvfile)
            next(rows) # header or weather file
            
            for row in rows:
                dateTime = datetime.strptime(row[0]+":"+row[1], "%Y/%m/%d:%H")
                hour = int(row[1])
                if dateTime < dayStart or dateTime > dayEnd:
                    continue
                # if hour == 10:
                #     print(dateTime)
                temperature = float(row[2])
                if row[4] == "NA":
                    ppfd = 0
                else:
                    ppfd = float (row[4]) 
                
                # start calculate
                
                mainStemNode.update(temperature)
                # if hour == 10:
                #     #print(dateTime,Node1.dNdt,Node1.dLAIdt())
                #     print(dateTime,round(Node1.node,1), round(Node1.LAI,1))
                Assimilate.update(temperature,ppfd,mainStemNode,Sink1)
                # daily accumulation of sink and source addtion rate
                dailyPg += Assimilate.Pg
                dailyRm += Assimilate.Rm
                dailyGRnet += Assimilate.GRnet
                dNdday += mainStemNode.dNdt
                
                #calculate temperature
                # sumation here output at hour = 23 (end of the day)
                TempSum += temperature
                if hour >= 6 and hour <= 18:
                    TempDay += temperature
                # finishing sum temperature
                if hour == 23: 
                    # calculate source
                    
                    Td = TempSum/24
                    Tdaytime = TempDay/13
                    Sink1.update(Td,Tdaytime,mainStemNode,dNdday,dailyGRnet)
                    print(dateTime,round(Sink1.W,1),round(Sink1.Wf,1))
    
                    # write to table 
                    toWrite = [dateTime,mainStemNode.node,mainStemNode.LAI,Sink1.W,Sink1.Wf,Sink1.Wm]
                    toWrite.extend([dailyPg,dailyRm,dailyGRnet])
                    writer.writerow(toWrite)
                    
                    # prepare list for ploting
                    lst_datetime.append(dateTime)
                    lst_node.append(mainStemNode.node)
                    lst_lai.append(mainStemNode.LAI)
                    lst_DWtotal.append(Sink1.W)
                    lst_DWfruit.append(Sink1.Wf)
                    lst_DWmature.append(Sink1.Wm)
                    lst_Pg.append(dailyPg)
                    lst_Rm.append(dailyRm)
                    
                    # reinitialized variable into 0
                    TempSum = 0
                    TempDay = 0
                    dailyPg = 0
                    dailyRm = 0
                    dailyGRnet = 0
                    dNdday = 0
    
    
    # %% 跑歷史值用
    # assign class
    mainStemNode = Tomgro.Node()
    Assimilate = Tomgro.Source(410,mainStemNode)
    Sink1 = Tomgro.Sink(mainStemNode)
    
    # initialize variable
    dailyPg = 0
    dailyRm = 0
    dailyGRnet = 0 
    dNdday = 0
    TempSum = 0
    TempDay = 0
    
    # initilize list for ploting
    lst_datetime = []
    lst_node = []
    lst_lai = []
    lst_DWtotal = []
    lst_DWfruit = []
    lst_DWmature = []
    lst_Pg = []
    lst_Rm = []
    
    
    
    
    with open (outputName, 'w',newline='') as csvwrite:
        writer = csv.writer(csvwrite, delimiter=',')
        header = ["Date","Node","LAI","AboveGroundDW","FruitDW","MatureFruitDW"] 
        writer.writerow(header)
        
        # reading weather file
        with open (weaName, newline='',encoding='utf-8') as csvfile:
            rows = csv.reader(csvfile)
            next(rows) # header or weather file
            
            for row in rows:
                dateTime = datetime.strptime(row[0]+":"+row[1], "%Y/%m/%d:%H")
                hour = int(row[1])
                if dateTime < dayStart or dateTime > dayEnd:
                    continue
                # if hour == 10:
                #     print(dateTime)
                temperature = float(row[2])
                if row[4] == "NA":
                    ppfd = 0
                else:
                    ppfd = float (row[4]) 
                
                # start calculate
                
                mainStemNode.update(temperature)
                # if hour == 10:
                #     #print(dateTime,Node1.dNdt,Node1.dLAIdt())
                #     print(dateTime,round(Node1.node,1), round(Node1.LAI,1))
                Assimilate.update(temperature,ppfd,mainStemNode,Sink1)
                # daily accumulation of sink and source addtion rate
                dailyPg += Assimilate.Pg
                dailyRm += Assimilate.Rm
                dailyGRnet += Assimilate.GRnet
                dNdday += mainStemNode.dNdt
                
                #calculate temperature
                # sumation here output at hour = 23 (end of the day)
                TempSum += temperature
                if hour >= 6 and hour <= 18:
                    TempDay += temperature
                # finishing sum temperature
                if hour == 23: 
                    # calculate source
                    
                    Td = TempSum/24
                    Tdaytime = TempDay/13
                    Sink1.update(Td,Tdaytime,mainStemNode,dNdday,dailyGRnet)
                    print(dateTime,round(Sink1.W,1),round(Sink1.Wf,1))
    
                    # write to table 
                    toWrite = [dateTime,mainStemNode.node,mainStemNode.LAI,Sink1.W,Sink1.Wf,Sink1.Wm]
                    toWrite.extend([dailyPg,dailyRm,dailyGRnet])
                    writer.writerow(toWrite)
                    
                    # prepare list for ploting
                    lst_datetime.append(dateTime)
                    lst_node.append(mainStemNode.node)
                    lst_lai.append(mainStemNode.LAI)
                    lst_DWtotal.append(Sink1.W)
                    lst_DWfruit.append(Sink1.Wf)
                    lst_DWmature.append(Sink1.Wm)
                    lst_Pg.append(dailyPg)
                    lst_Rm.append(dailyRm)
                    
                    # reinitialized variable into 0
                    TempSum = 0
                    TempDay = 0
                    dailyPg = 0
                    dailyRm = 0
                    dailyGRnet = 0
                    dNdday = 0
    
    # 開始計算歷史部分
    # initialize variable
    dailyPg_his = 0
    dailyRm_his = 0
    dailyGRnet_his = 0 
    dNdday_his = 0
    TempSum = 0
    TempDay = 0
    
    # initilize list for ploting
    lst_datetime_his = []
    lst_node_his = []
    lst_lai_his = []
    lst_DWtotal_his = []
    lst_DWfruit_his = []
    lst_DWmature_his = []
    lst_Pg_his = []
    lst_Rm_his = []
    
    dayStart_his = datetime.strptime(row[0] ,"%Y/%m/%d")
    
    with open (outputName, 'w',newline='') as csvwrite:
        writer = csv.writer(csvwrite, delimiter=',')
        header = ["Date","Node","LAI","AboveGroundDW","FruitDW","MatureFruitDW"] 
        writer.writerow(header)
        
        # reading weather file
        with open (weaName_history, newline='',encoding='utf-8') as csvfile:
            rows = csv.reader(csvfile)
            next(rows) # header or weather file
            
            for row in rows:
                dateTime = datetime.strptime(row[0]+":"+row[1], "%Y/%m/%d:%H")
                hour = int(row[1])
                if dateTime < dayStart_his or dateTime > dayEnd:
                    continue
                # if hour == 10:
                #     print(dateTime)
                temperature = float(row[2])
                if row[4] == "NA":
                    ppfd = 0
                else:
                    ppfd = float (row[4]) 
                
                # start calculate
                
                mainStemNode.update(temperature)
                # if hour == 10:
                #     #print(dateTime,Node1.dNdt,Node1.dLAIdt())
                #     print(dateTime,round(Node1.node,1), round(Node1.LAI,1))
                Assimilate.update(temperature,ppfd,mainStemNode,Sink1)
                # daily accumulation of sink and source addtion rate
                dailyPg_his += Assimilate.Pg
                dailyRm_his += Assimilate.Rm
                dailyGRnet_his += Assimilate.GRnet
                dNdday_his += mainStemNode.dNdt
                
                #calculate temperature
                # sumation here output at hour = 23 (end of the day)
                TempSum += temperature
                if hour >= 6 and hour <= 18:
                    TempDay += temperature
                # finishing sum temperature
                if hour == 23: 
                    # calculate source
                    
                    Td = TempSum/24
                    Tdaytime = TempDay/13
                    Sink1.update(Td,Tdaytime,mainStemNode,dNdday_his,dailyGRnet_his)
                    print(dateTime,round(Sink1.W,1),round(Sink1.Wf,1))
    
                    # write to table 
                    toWrite = [dateTime,mainStemNode.node,mainStemNode.LAI,Sink1.W,Sink1.Wf,Sink1.Wm]
                    toWrite.extend([dailyPg_his,dailyRm_his,dailyGRnet_his])
                    writer.writerow(toWrite)
                    
                    # prepare list for ploting
                    lst_datetime_his.append(dateTime)
                    lst_node_his.append(mainStemNode.node)
                    lst_lai_his.append(mainStemNode.LAI)
                    lst_DWtotal_his.append(Sink1.W)
                    lst_DWfruit_his.append(Sink1.Wf)
                    lst_DWmature_his.append(Sink1.Wm)
                    lst_Pg_his.append(dailyPg_his)
                    lst_Rm_his.append(dailyRm_his)
                    
                    # reinitialized variable into 0
                    TempSum = 0
                    TempDay = 0
                    dailyPg_his = 0
                    dailyRm_his = 0
                    dailyGRnet_his = 0
                    dNdday_his = 0
    
    
    
    #%% 跑歷史值用升溫模式
    # assign class
    mainStemNode = Tomgro.Node()
    Assimilate = Tomgro.Source(410,mainStemNode)
    Sink1 = Tomgro.Sink(mainStemNode)
    
    # initialize variable
    dailyPg = 0
    dailyRm = 0
    dailyGRnet = 0 
    dNdday = 0
    TempSum = 0
    TempDay = 0
    
    # initilize list for ploting
    lst_datetime = []
    lst_node = []
    lst_lai = []
    lst_DWtotal = []
    lst_DWfruit = []
    lst_DWmature = []
    lst_Pg = []
    lst_Rm = []
    
    
    
    
    with open (outputName, 'w',newline='') as csvwrite:
        writer = csv.writer(csvwrite, delimiter=',')
        header = ["Date","Node","LAI","AboveGroundDW","FruitDW","MatureFruitDW"] 
        writer.writerow(header)
        
        # reading weather file
        with open (weaName, newline='',encoding='utf-8') as csvfile:
            rows = csv.reader(csvfile)
            next(rows) # header or weather file
            
            for row in rows:
                dateTime = datetime.strptime(row[0]+":"+row[1], "%Y/%m/%d:%H")
                hour = int(row[1])
                if dateTime < dayStart or dateTime > dayEnd:
                    continue
                # if hour == 10:
                #     print(dateTime)
                temperature = float(row[2])
                if row[4] == "NA":
                    ppfd = 0
                else:
                    ppfd = float (row[4]) 
                
                # start calculate
                
                mainStemNode.update(temperature)
                # if hour == 10:
                #     #print(dateTime,Node1.dNdt,Node1.dLAIdt())
                #     print(dateTime,round(Node1.node,1), round(Node1.LAI,1))
                Assimilate.update(temperature,ppfd,mainStemNode,Sink1)
                # daily accumulation of sink and source addtion rate
                dailyPg += Assimilate.Pg
                dailyRm += Assimilate.Rm
                dailyGRnet += Assimilate.GRnet
                dNdday += mainStemNode.dNdt
                
                #calculate temperature
                # sumation here output at hour = 23 (end of the day)
                TempSum += temperature
                if hour >= 6 and hour <= 18:
                    TempDay += temperature
                # finishing sum temperature
                if hour == 23: 
                    # calculate source
                    
                    Td = TempSum/24
                    Tdaytime = TempDay/13
                    Sink1.update(Td,Tdaytime,mainStemNode,dNdday,dailyGRnet)
                    print(dateTime,round(Sink1.W,1),round(Sink1.Wf,1))
    
                    # write to table 
                    toWrite = [dateTime,mainStemNode.node,mainStemNode.LAI,Sink1.W,Sink1.Wf,Sink1.Wm]
                    toWrite.extend([dailyPg,dailyRm,dailyGRnet])
                    writer.writerow(toWrite)
                    
                    # prepare list for ploting
                    lst_datetime.append(dateTime)
                    lst_node.append(mainStemNode.node)
                    lst_lai.append(mainStemNode.LAI)
                    lst_DWtotal.append(Sink1.W)
                    lst_DWfruit.append(Sink1.Wf)
                    lst_DWmature.append(Sink1.Wm)
                    lst_Pg.append(dailyPg)
                    lst_Rm.append(dailyRm)
                    
                    # reinitialized variable into 0
                    TempSum = 0
                    TempDay = 0
                    dailyPg = 0
                    dailyRm = 0
                    dailyGRnet = 0
                    dNdday = 0
    
    # initialize variable
    dailyPg_his = 0
    dailyRm_his = 0
    dailyGRnet_his = 0 
    dNdday_his = 0
    TempSum = 0
    TempDay = 0
    
    # initilize list for ploting
    lst_datetime_his_up = []
    lst_node_his_up = []
    lst_lai_his_up = []
    lst_DWtotal_his_up = []
    lst_DWfruit_his_up = []
    lst_DWmature_his_up = []
    lst_Pg_his_up = []
    lst_Rm_his_up = []
    
    
    
    with open (outputName, 'w',newline='') as csvwrite:
        writer = csv.writer(csvwrite, delimiter=',')
        header = ["Date","Node","LAI","AboveGroundDW","FruitDW","MatureFruitDW"] 
        writer.writerow(header)
        
        # reading weather file
        with open (weaName_history, newline='',encoding='utf-8') as csvfile:
            rows = csv.reader(csvfile)
            next(rows) # header or weather file
            
            for row in rows:
                dateTime = datetime.strptime(row[0]+":"+row[1], "%Y/%m/%d:%H")
                hour = int(row[1])
                if dateTime < dayStart_his or dateTime > dayEnd:
                    continue
                # if hour == 10:
                #     print(dateTime)
                temperature = float(row[2])+Range_temperature
                if row[4] == "NA":
                    ppfd = 0
                else:
                    ppfd = float (row[4]) 
                
                # start calculate
                
                mainStemNode.update(temperature)
                # if hour == 10:
                #     #print(dateTime,Node1.dNdt,Node1.dLAIdt())
                #     print(dateTime,round(Node1.node,1), round(Node1.LAI,1))
                Assimilate.update(temperature,ppfd,mainStemNode,Sink1)
                # daily accumulation of sink and source addtion rate
                dailyPg_his += Assimilate.Pg
                dailyRm_his += Assimilate.Rm
                dailyGRnet_his += Assimilate.GRnet
                dNdday_his += mainStemNode.dNdt
                
                #calculate temperature
                # sumation here output at hour = 23 (end of the day)
                TempSum += temperature
                if hour >= 6 and hour <= 18:
                    TempDay += temperature
                # finishing sum temperature
                if hour == 23: 
                    # calculate source
                    
                    Td = TempSum/24
                    Tdaytime = TempDay/13
                    Sink1.update(Td,Tdaytime,mainStemNode,dNdday_his,dailyGRnet_his)
                    print(dateTime,round(Sink1.W,1),round(Sink1.Wf,1))
    
                    # write to table 
                    toWrite = [dateTime,mainStemNode.node,mainStemNode.LAI,Sink1.W,Sink1.Wf,Sink1.Wm]
                    toWrite.extend([dailyPg_his,dailyRm_his,dailyGRnet_his])
                    writer.writerow(toWrite)
                    
                    # prepare list for ploting
                    lst_datetime_his_up.append(dateTime)
                    lst_node_his_up.append(mainStemNode.node)
                    lst_lai_his_up.append(mainStemNode.LAI)
                    lst_DWtotal_his_up.append(Sink1.W)
                    lst_DWfruit_his_up.append(Sink1.Wf)
                    lst_DWmature_his_up.append(Sink1.Wm)
                    lst_Pg_his_up.append(dailyPg_his)
                    lst_Rm_his_up.append(dailyRm_his)
                    
                    # reinitialized variable into 0
                    TempSum = 0
                    TempDay = 0
                    dailyPg_his = 0
                    dailyRm_his = 0
                    dailyGRnet_his = 0
                    dNdday_his = 0
    
    #%% 跑歷史值用降溫模式
    # assign class
    mainStemNode = Tomgro.Node()
    Assimilate = Tomgro.Source(410,mainStemNode)
    Sink1 = Tomgro.Sink(mainStemNode)
    
    # initialize variable
    dailyPg = 0
    dailyRm = 0
    dailyGRnet = 0 
    dNdday = 0
    TempSum = 0
    TempDay = 0
    
    # initilize list for ploting
    lst_datetime = []
    lst_node = []
    lst_lai = []
    lst_DWtotal = []
    lst_DWfruit = []
    lst_DWmature = []
    lst_Pg = []
    lst_Rm = []
    
    
    
    
    with open (outputName, 'w',newline='') as csvwrite:
        writer = csv.writer(csvwrite, delimiter=',')
        header = ["Date","Node","LAI","AboveGroundDW","FruitDW","MatureFruitDW"] 
        writer.writerow(header)
        
        # reading weather file
        with open (weaName, newline='',encoding='utf-8') as csvfile:
            rows = csv.reader(csvfile)
            next(rows) # header or weather file
            
            for row in rows:
                dateTime = datetime.strptime(row[0]+":"+row[1], "%Y/%m/%d:%H")
                hour = int(row[1])
                if dateTime < dayStart or dateTime > dayEnd:
                    continue
                # if hour == 10:
                #     print(dateTime)
                temperature = float(row[2])
                if row[4] == "NA":
                    ppfd = 0
                else:
                    ppfd = float (row[4]) 
                
                # start calculate
                
                mainStemNode.update(temperature)
                # if hour == 10:
                #     #print(dateTime,Node1.dNdt,Node1.dLAIdt())
                #     print(dateTime,round(Node1.node,1), round(Node1.LAI,1))
                Assimilate.update(temperature,ppfd,mainStemNode,Sink1)
                # daily accumulation of sink and source addtion rate
                dailyPg += Assimilate.Pg
                dailyRm += Assimilate.Rm
                dailyGRnet += Assimilate.GRnet
                dNdday += mainStemNode.dNdt
                
                #calculate temperature
                # sumation here output at hour = 23 (end of the day)
                TempSum += temperature
                if hour >= 6 and hour <= 18:
                    TempDay += temperature
                # finishing sum temperature
                if hour == 23: 
                    # calculate source
                    
                    Td = TempSum/24
                    Tdaytime = TempDay/13
                    Sink1.update(Td,Tdaytime,mainStemNode,dNdday,dailyGRnet)
                    print(dateTime,round(Sink1.W,1),round(Sink1.Wf,1))
    
                    # write to table 
                    toWrite = [dateTime,mainStemNode.node,mainStemNode.LAI,Sink1.W,Sink1.Wf,Sink1.Wm]
                    toWrite.extend([dailyPg,dailyRm,dailyGRnet])
                    writer.writerow(toWrite)
                    
                    # prepare list for ploting
                    lst_datetime.append(dateTime)
                    lst_node.append(mainStemNode.node)
                    lst_lai.append(mainStemNode.LAI)
                    lst_DWtotal.append(Sink1.W)
                    lst_DWfruit.append(Sink1.Wf)
                    lst_DWmature.append(Sink1.Wm)
                    lst_Pg.append(dailyPg)
                    lst_Rm.append(dailyRm)
                    
                    # reinitialized variable into 0
                    TempSum = 0
                    TempDay = 0
                    dailyPg = 0
                    dailyRm = 0
                    dailyGRnet = 0
                    dNdday = 0
    
    # initialize variable
    dailyPg_his = 0
    dailyRm_his = 0
    dailyGRnet_his = 0 
    dNdday_his = 0
    TempSum = 0
    TempDay = 0
    
    # initilize list for ploting
    lst_datetime_his_down = []
    lst_node_his_down = []
    lst_lai_his_down = []
    lst_DWtotal_his_down = []
    lst_DWfruit_his_down = []
    lst_DWmature_his_down = []
    lst_Pg_his_down = []
    lst_Rm_his_down = []
    
    
    
    with open (outputName, 'w',newline='') as csvwrite:
        writer = csv.writer(csvwrite, delimiter=',')
        header = ["Date","Node","LAI","AboveGroundDW","FruitDW","MatureFruitDW"] 
        writer.writerow(header)
        
        # reading weather file
        with open (weaName_history, newline='',encoding='utf-8') as csvfile:
            rows = csv.reader(csvfile)
            next(rows) # header or weather file
            
            for row in rows:
                dateTime = datetime.strptime(row[0]+":"+row[1], "%Y/%m/%d:%H")
                hour = int(row[1])
                if dateTime < dayStart_his or dateTime > dayEnd:
                    continue
                # if hour == 10:
                #     print(dateTime)
                temperature = float(row[2])-Range_temperature
                if row[4] == "NA":
                    ppfd = 0
                else:
                    ppfd = float (row[4]) 
                
                # start calculate
                
                mainStemNode.update(temperature)
                # if hour == 10:
                #     #print(dateTime,Node1.dNdt,Node1.dLAIdt())
                #     print(dateTime,round(Node1.node,1), round(Node1.LAI,1))
                Assimilate.update(temperature,ppfd,mainStemNode,Sink1)
                # daily accumulation of sink and source addtion rate
                dailyPg_his += Assimilate.Pg
                dailyRm_his += Assimilate.Rm
                dailyGRnet_his += Assimilate.GRnet
                dNdday_his += mainStemNode.dNdt
                
                #calculate temperature
                # sumation here output at hour = 23 (end of the day)
                TempSum += temperature
                if hour >= 6 and hour <= 18:
                    TempDay += temperature
                # finishing sum temperature
                if hour == 23: 
                    # calculate source
                    
                    Td = TempSum/24
                    Tdaytime = TempDay/13
                    Sink1.update(Td,Tdaytime,mainStemNode,dNdday_his,dailyGRnet_his)
                    print(dateTime,round(Sink1.W,1),round(Sink1.Wf,1))
    
                    # write to table 
                    toWrite = [dateTime,mainStemNode.node,mainStemNode.LAI,Sink1.W,Sink1.Wf,Sink1.Wm]
                    toWrite.extend([dailyPg_his,dailyRm_his,dailyGRnet_his])
                    writer.writerow(toWrite)
                    
                    # prepare list for ploting
                    lst_datetime_his_down.append(dateTime)
                    lst_node_his_down.append(mainStemNode.node)
                    lst_lai_his_down.append(mainStemNode.LAI)
                    lst_DWtotal_his_down.append(Sink1.W)
                    lst_DWfruit_his_down.append(Sink1.Wf)
                    lst_DWmature_his_down.append(Sink1.Wm)
                    lst_Pg_his_down.append(dailyPg_his)
                    lst_Rm_his_down.append(dailyRm_his)
                    
                    # reinitialized variable into 0
                    TempSum = 0
                    TempDay = 0
                    dailyPg_his = 0
                    dailyRm_his = 0
                    dailyGRnet_his = 0
                    dNdday_his = 0

    #%% 繪圖區2-葉面積指數&每周鮮重
    # 增加每周為單位的列表，以每七天為單位，目前的輸出是乾重，要乘上水分含量
    # 才會得到鮮重的資料
    
    deltaDay = 7 # weekly
    counter = 0
    wk_date = [] # list for weekly date
    wk_DWmature = [] # list for weekly mature fruit weight
    fruitDW0 = 0 # set the initial condition of fruit weight to 0
    
    for d in range(len(lst_DWmature)):
        if counter%deltaDay == 0:
            wk_date.append( lst_datetime[d])
            fruitDW1 = lst_DWmature[d]
            deltaFruitDW = max(0,fruitDW1 - fruitDW0) # weekly accumulated
            deltaFruitFW = deltaFruitDW*20/1000 #假設水分含量95%，換算成kg/m2
            wk_DWmature.append(deltaFruitFW)
            fruitDW0 = fruitDW1 # pass到舊的fruitDW，作為下周的基礎
            
        counter += 1
    
    counter = 0
    wk_date_his = []
    wk_DWmature_his = []
    fruitDW0_his = lst_DWmature[-7]
    
    wk_date_his_up = []
    wk_DWmature_his_up = []
    fruitDW0_his_up = lst_DWmature[-7]
    
    wk_date_his_down = []
    wk_DWmature_his_down = []
    fruitDW0_his_down = lst_DWmature[-7]
    
    # 歷史平均值
    for d in range(len(lst_DWmature_his)):
        if counter%deltaDay == 0:
            wk_date_his.append( lst_datetime_his[d])
            fruitDW1_his = lst_DWmature_his[d]
            deltaFruitDW_his = max(0,fruitDW1_his - fruitDW0_his)
            deltaFruitFW_his = deltaFruitDW_his*20/1000
            wk_DWmature_his.append(deltaFruitFW_his)
            fruitDW0_his = fruitDW1_his
    
    
    # 歷史平均值升溫
            wk_date_his_up.append( lst_datetime_his_up[d])
            fruitDW1_his_up = lst_DWmature_his_up[d]
            deltaFruitDW_his_up = max(0,fruitDW1_his_up - fruitDW0_his_up)
            deltaFruitFW_his_up = deltaFruitDW_his_up*20/1000
            wk_DWmature_his_up.append(deltaFruitFW_his_up)
            fruitDW0_his_up = fruitDW1_his_up
    
    
    # 歷史平均值降溫
            wk_date_his_down.append( lst_datetime_his_down[d])
            fruitDW1_his_down = lst_DWmature_his_down[d]
            deltaFruitDW_his_down = max(0,fruitDW1_his_down - fruitDW0_his_down)
            deltaFruitFW_his_down = deltaFruitDW_his_down*20/1000
            wk_DWmature_his_down.append(deltaFruitFW_his_down)
            fruitDW0_his_down = fruitDW1_his_down
            
        counter += 1
    
    
    # 加入現在最後值到歷史模擬中
    wk_date_his.insert(0, wk_date[-1])
    wk_date_his_up.insert(0, wk_date[-1])
    wk_date_his_down.insert(0, wk_date[-1])
    
    wk_DWmature_his.insert(0, wk_DWmature[-1])
    wk_DWmature_his_up.insert(0, wk_DWmature[-1])
    wk_DWmature_his_down.insert(0, wk_DWmature[-1])
    # plot weekly        
            
    plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=[10,7.5],dpi=120)
    
    plt.subplot(211)
    plt.plot(lst_datetime_his,lst_lai_his,label='history',color = "#C0C0C0")
    # plt.plot(lst_datetime_his_up,lst_lai_his_up,label='history_up',color = "#FF0000",linestyle='--',alpha = 0.5)
    # plt.plot(lst_datetime_his_down,lst_lai_his_down,label='history_down',color = "#0000FF",linestyle='--',alpha = 0.5)
    plt.plot(lst_datetime,lst_lai,label='now',linewidth=3)
    plt.legend()
    plt.ylabel('葉面積指數')
    plt.title('葉面積指數變化')
    plt.subplot(212)
    
    plt.plot(wk_date_his, wk_DWmature_his,label='history',color = "#C0C0C0")
    plt.plot(wk_date_his_up, wk_DWmature_his_up,label='history_up',color = "#FF0000",linestyle='--',alpha = 0.5)
    plt.plot(wk_date_his_down, wk_DWmature_his_down,label='history_down',color = "#0000FF",linestyle='--',alpha = 0.5)
    plt.fill_between(wk_date_his_up, y1 = wk_DWmature_his_up,y2 = wk_DWmature_his_down,color = "#FFFF00",alpha = 0.25)
    plt.plot(wk_date, wk_DWmature,label='now',linewidth=3,marker='o')
    plt.legend()
    plt.ylabel('每周鮮重 (kg/m2)')
    plt.title('每周產量')
    plt.xlabel('\n※ 溫度幅度為正負 '+ str(Range_temperature)+' 度',loc='left')
    plt.tight_layout()
    plt.show()


#%% GUI介面
# 建立主視窗 Frame
window = tk.Tk()
# 設定視窗標題
window.title('Tomgro GUI')
window.configure(background='#C0C0C0')

# 第零層，標題
header_label = tk.Label(window, text='Tomgro 模型',bg="#C0C0C0",font=("", 32))
header_label.grid(row=0, column=0,columnspan=2)

# 第一層，輸入日期
header1_label = tk.Label(window, text='-'*12+'LAI計算與比較'+'-'*12,bg="#C0C0C0",font=("", 16))
header1_label.grid(row=1, column=0,columnspan=2, ipady=10,pady=10)

# 第二層，輸入日期
Date_label = tk.Label(window, text='觀測日期 :',font=("", 16))
Date_label.grid(row=2, column=0, ipadx=5,padx=5)

Layer1_frame = tk.Frame(window)
Layer1_frame.grid(row=2, column=1, padx=5)

Year_entry = tk.Entry(Layer1_frame,width=6,font=("", 16))
Year_entry.insert(0, "2022")
Year_entry.grid(row=0, column=0, ipadx=5)
Year_label = tk.Label(Layer1_frame, text='/',font=("", 16))
Year_label.grid(row=0, column=1)

Month_entry = tk.Entry(Layer1_frame,width=3,font=("", 16))
Month_entry.insert(0, "01")
Month_entry.grid(row=0, column=2)
Month_label = tk.Label(Layer1_frame, text='/',font=("", 16))
Month_label.grid(row=0, column=3)

Day_entry = tk.Entry(Layer1_frame,width=3,font=("", 16))
Day_entry.insert(0, "19")
Day_entry.grid(row=0, column=4)

# 第三層，輸入頁面積
LeafArea_label = tk.Label(window, text='LeafArea（cm2）:',font=("", 16))
LeafArea_label.grid(row=3, column=0, ipadx=5,padx=5)

LeafArea_entry = tk.Entry(window,font=("", 16))
LeafArea_entry.grid(row=3, column=1, ipadx=5,padx=5)

# 第四層，計算指數結果
result_label = tk.Label(window,bg="#C0C0C0",font=("", 16))
result_label.grid(row=4, column=0,columnspan=2, ipadx=5,padx=5)

# 第五層，執行按鈕
calculate_btn = tk.Button(window, text='馬上計算', command=calculate_LAI_number, width=15,font=("", 16))
calculate_btn.grid(row=5, column=0, ipadx=5,padx=5)

Show_now_btn = tk.Button(window, text='完整模擬', command=Show_now, width=15,font=("", 16))
Show_now_btn.grid(row=5, column=1, ipadx=5,padx=5)

# 第六層，溫度範圍
header2_label = tk.Label(window, text='-'*12+'溫度變化模擬'+'-'*12,bg="#C0C0C0",font=("", 16))
header2_label.grid(row=6, column=0,columnspan=2, ipady=10,pady=10)

# 第七層，溫度範圍
Layer5_frame = tk.Frame(window)
Layer5_frame.grid(row=7, column=0, padx=5)

temperature_label = tk.Label(Layer5_frame, text='溫度變化:',font=("", 16))
temperature_label.grid(row=0, column=0, ipadx=5,padx=5)
temperature_scale = tk.Scale(Layer5_frame, to = 15, orient="horizontal")
temperature_scale.grid(row=0, column=1)

Show_future_btn = tk.Button(window, text='完整未來模擬', command=Show_future, width=15,font=("", 16))
Show_future_btn.grid(row=7, column=1, ipadx=5,padx=5)

# 第八層，預設輸入資料
header3_label = tk.Label(window, text='-'*12+'輸入資料'+'-'*12,bg="#C0C0C0",font=("", 16))
header3_label.grid(row=8, column=0,columnspan=2, ipady=10,pady=10)

# 第九層，預設輸入資料
Layer9_frame = tk.Frame(window)
Layer9_frame.grid(row=9, column=0,columnspan=2, padx=5)

wea_obs_label = tk.Label(Layer9_frame, text='觀測氣象檔 :',font=("", 16))
wea_obs_label.grid(row=1, column=0, ipadx=5,padx=5)
wea_obs_entry = tk.Entry(Layer9_frame)
wea_obs_entry.insert(0, "19D-GHwea_20220113.csv")
wea_obs_entry.grid(row=1, column=1, ipadx=5)

wea_his_label = tk.Label(Layer9_frame, text='歷史氣象檔 :',font=("", 16))
wea_his_label.grid(row=2, column=0, ipadx=5,padx=5)
wea_his_entry = tk.Entry(Layer9_frame)
wea_his_entry.insert(0, "Hiswea_20012020.csv")
wea_his_entry.grid(row=2, column=1, ipadx=5)

plantDate_label = tk.Label(Layer9_frame, text='種植日期 :',font=("", 16))
plantDate_label.grid(row=3, column=0, ipadx=5,padx=5)
plantDate_entry = tk.Entry(Layer9_frame)
plantDate_entry.insert(0, "2021/10/12")
plantDate_entry.grid(row=3, column=1, ipadx=5)

endDate_label = tk.Label(Layer9_frame, text='結束日期 :',font=("", 16))
endDate_label.grid(row=4, column=0, ipadx=5,padx=5)
endDate_entry = tk.Entry(Layer9_frame)
endDate_entry.insert(0, "2022/5/15")
endDate_entry.grid(row=4, column=1, ipadx=5)


window.mainloop()
