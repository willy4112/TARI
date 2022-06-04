# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 18:36:12 2021
 
@author: CCW
"""
import Tomgro
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np


#%% 輸入區
weaName = "19D-GHwea_20220113.csv"       # 請更新觀測氣象檔
weaName_history = "Hiswea_20012020.csv"
outputName = "tomato_v0.csv"
# initial condition
plantingDate = "2021/10/12"              # 本次種植2021/10/12
endDate = "2022/1/19"
detect_leafarea = 25678                  # 請輸入從照片計算之葉面積(cm^2)


dayStart = datetime.strptime(plantingDate,"%Y/%m/%d")
dayEnd = datetime.strptime(endDate,"%Y/%m/%d")

#%% 農場調查資料
lis_datetime_lai = [dt.datetime(2021,10,13,23),dt.datetime(2021,10,20,23),dt.datetime(2021,10,27,23),dt.datetime(2021,11,3,23),dt.datetime(2021,11,10,23),dt.datetime(2021,11,17,23),dt.datetime(2021,11,24,23),dt.datetime(2021,12,1,23),dt.datetime(2021,12,8,23),dt.datetime(2021,12,15,23),dt.datetime(2021,12,22,23),dt.datetime(2021,12,29,23),dt.datetime(2022,1,5,23),dt.datetime(2022,1,12,23)]
lia_farm1 = [417.2058,882.74,3555.947,10849.06,20136.02,28385.32,32495.34,37621.56,38911.94,41680.71,44064.12,45460.52,46811.19,49860.05]
lis_lia_farm1 = np.array(lia_farm1)/12*2.98/10000
lis_lia_farm1 = lis_lia_farm1.tolist()

lia_farm2 = [333.8339,982.854,4018.52,12467.55,24575.02,36299.57,40995.54,48568.39,51114.37,54654.34,57520.22,59342.3,61712.1,65320.13]
lis_lia_farm2 = np.array(lia_farm2)/12*2.98/10000
lis_lia_farm2 = lis_lia_farm2.tolist()

lis_datetime_fruit = [dt.datetime(2022,1,5,23),dt.datetime(2022,1,12,23)]
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


detect_datetime = dt.datetime(2022, 1, 19)
detect_LAI = detect_leafarea/6/0.89*2.89/10000


#%% 繪圖區2-葉面積指數&每周鮮重
        
plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=[10,7.5],dpi=120)

plt.subplot(211)
plt.scatter(detect_datetime,detect_LAI,color = 'red')
plt.text(detect_datetime,detect_LAI-0.15,round(detect_LAI,2),horizontalalignment='center')
plt.plot(lst_datetime_his,lst_lai_his,label='history',color = "#C0C0C0")
plt.plot(lst_datetime,lst_lai,label='now',linewidth=3)
plt.plot(lis_datetime_lai,lis_lia_farm1,label='farm1',marker='o')
# plt.plot(lis_datetime_lai,lis_lia_farm2,label='farm2',marker='o')

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

