# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 18:36:12 2021
 
@author: user
"""
import Tomgro
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#import matplotlib.dates as mdates

#%% 輸入區
weaName = "19D-GHwea_20220113.csv"       # 請更新觀測氣象檔
weaName_history = "Hiswea_20012020.csv"
outputName = "tomato_v0.csv"
# initial condition
plantingDate = "2021/10/12"              # 本次種植2021/10/12
endDate = "2022/5/15"
Range_temperature = 3                    # 輸入預計變化的溫度


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
plt.plot(lst_datetime,lst_DWtotal,label='莖乾重')
plt.plot(lst_datetime,lst_DWfruit, label='果實乾重')
plt.plot(lst_datetime,lst_DWmature, label='成熟果實乾重')
plt.legend()
plt.ylabel('乾物質重 (g/m2)')
plt.title('乾物質變化')

plt.subplot(224)
plt.plot(lst_datetime, lst_Pg, label='總光合作用')
plt.plot(lst_datetime, lst_Rm, label='呼吸作用')
plt.legend()
plt.title('碳平衡')
plt.ylabel('速率(µmol m-2 s-1)')
plt.tight_layout()
plt.show()                


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

#%% 繪圖區3 葉面積指數變化
plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=[8,6],dpi=150)

plt.subplot(312)
plt.plot(lst_datetime_his,lst_lai_his,label='history',color = "#C0C0C0")
plt.plot(lst_datetime,lst_lai,label='now',linewidth=3)
plt.ylabel('葉面積指數')
plt.legend()
plt.subplot(311)
plt.plot(lst_datetime_his_up,lst_lai_his_up,label='history_up',color = "#FF0000",linestyle='--',alpha = 0.5)
plt.plot(lst_datetime,lst_lai,label='now',linewidth=3)
plt.ylabel('葉面積指數')
plt.title('葉面積指數變化')
plt.legend()
plt.subplot(313)
plt.plot(lst_datetime_his_down,lst_lai_his_down,label='history_down',color = "#0000FF",linestyle='--',alpha = 0.5)
plt.plot(lst_datetime,lst_lai,label='now',linewidth=3)
plt.legend()
plt.ylabel('葉面積指數')
plt.xlabel('\n※ 溫度幅度為正負 '+ str(Range_temperature)+' 度',loc='left')
plt.tight_layout()
plt.show()

#%% 繪圖區4 每周鮮重

plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=[10,5],dpi=150)

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

#%% 繪圖區5 主幹節數變化

plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=[10,5],dpi=150)

plt.plot(lst_datetime_his,lst_node_his,label='history',color = "#C0C0C0")
plt.plot(lst_datetime_his_up,lst_node_his_up,label='history_up',color = "#FF0000",linestyle='--',alpha = 0.5)
plt.plot(lst_datetime_his_down,lst_node_his_down,label='history_down',color = "#0000FF",linestyle='--',alpha = 0.5)
plt.fill_between(lst_datetime_his, y1 = lst_node_his_up,y2 = lst_node_his_down,color = "#FFFF00",alpha = 0.25)
plt.plot(lst_datetime,lst_node)
plt.ylabel('主幹節數')
plt.title('主幹節數變化')
plt.legend()
plt.xlabel('\n※ 溫度幅度為正負 '+ str(Range_temperature)+' 度',loc='left')
plt.tight_layout()
plt.show()

#%% 繪圖區6 碳平衡

plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=[10,5],dpi=150)

plt.fill_between(lst_datetime_his, y1 = lst_Pg_his_up,y2 = lst_Pg_his_down,color = "#0000FF",alpha = 0.25)
plt.plot(lst_datetime_his, lst_Pg_his,linestyle='--',color = "#C0C0FF")
plt.plot(lst_datetime, lst_Pg, label='總光合作用')

plt.fill_between(lst_datetime_his, y1 = lst_Rm_his_up,y2 = lst_Rm_his_down,color = "#FF0000",alpha = 0.25)
plt.plot(lst_datetime_his, lst_Rm_his,linestyle='--',color = "#ffC0C0")
plt.plot(lst_datetime, lst_Rm, label='呼吸作用',color = "red")
plt.legend()
plt.title('碳平衡')
plt.ylabel('速率(µmol m-2 s-1)')
plt.xlabel('\n※ 溫度幅度為正負 '+ str(Range_temperature)+' 度',loc='left')
plt.tight_layout()
plt.show()

#%% 繪圖區7 乾物質變化

plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=[10,5],dpi=150)

plt.fill_between(lst_datetime_his, y1 = lst_DWtotal_his_up,y2 = lst_DWtotal_his_down,color = "#0000FF",alpha = 0.25)
plt.plot(lst_datetime,lst_DWtotal,label='莖乾重')
plt.fill_between(lst_datetime_his, y1 = lst_DWfruit_his_up,y2 = lst_DWfruit_his_down,color = "Orange",alpha = 0.25)
plt.plot(lst_datetime,lst_DWfruit, label='果實乾重')
plt.fill_between(lst_datetime_his, y1 = lst_DWmature_his_up,y2 = lst_DWmature_his_down,color = "#00FF00",alpha = 0.25)
plt.plot(lst_datetime,lst_DWmature, label='成熟果實乾重')
plt.legend(loc=2)
plt.ylabel('乾物質重 (g/m2)')
plt.xlabel('\n※ 溫度幅度為正負 '+ str(Range_temperature)+' 度',loc='left')
plt.tight_layout()
plt.title('乾物質變化')

#%% 匯出LIA來與實驗值比較

columns_name = ['Date','Node','LAI']
data_LAI = np.array([lst_datetime,lst_node,lst_lai])
data_LAI = data_LAI.T
reoprt_LAI = pd.DataFrame(data_LAI,columns=columns_name)
# 檢查資料型態
# reoprt_LAI.dtypes

# reoprt_LAI.to_csv(r'D:\我的雲端硬碟\work\3.TARI\番茄\Data\2021 數據\模擬Tomato.csv',encoding='utf-8-sig')
