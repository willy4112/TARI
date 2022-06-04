# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 18:36:12 2021
 
@author: CCW
"""
import Tomgro
import csv
from datetime import datetime
import matplotlib.pyplot as plt
#import matplotlib.dates as mdates

#%% 輸入區
weaName = "19D-GHwea_20211228.csv"       # 展示時使用GHwea.csv
weaName_history = "Hiswea_20012020.csv"
outputName = "tomato_v0.csv"
# initial condition
plantingDate = "2021/10/12"              # 本次種植2021/10/12, 展示資料2020/10/14
endDate = "2022/5/15"                    # 展示資料2021/5/15
Range_temperature = 0


dayStart = datetime.strptime(plantingDate,"%Y/%m/%d")
dayEnd = datetime.strptime(endDate,"%Y/%m/%d")

#%% 初始化變數
## --- 初始化物件 ---
# 觀測氣象 + 歷史氣象
MainStemNode = Tomgro.Node()
Assimilate = Tomgro.Source(410,MainStemNode)
Sink1 = Tomgro.Sink(MainStemNode)
# 觀測氣象 + 升溫情境(Up)
MainStemNodeUp = Tomgro.Node()
AssimilateUp = Tomgro.Source(410,MainStemNodeUp)
SinkUp = Tomgro.Sink(MainStemNodeUp)
# 觀測氣象 + 降溫情境(Down)
MainStemNodeDn = Tomgro.Node()
AssimilateDn = Tomgro.Source(410,MainStemNodeDn)
SinkDn = Tomgro.Sink(MainStemNodeDn)

## --- 初始化變數 ---
#  觀測氣象 - variable
dailyPg, dailyRm, dailyGRnet = (0,)*3
dNdday, tempSum, tempDay = (0,)*3
# 升溫情境 - variable
dailyPg_up, dailyRm_up, dailyGRnet_up = (0,)*3
dNdday_up, tempSum_up, tempDay_up = (0,)*3
# 降溫情境 - variable
dailyPg_dn, dailyRm_dn, dailyGRnet_dn = (0,)*3
dNdday_dn, tempSum_dn, tempDay_dn = (0,)*3

## --- 畫圖用的 list ---
# 觀測氣象
lst_datetime, lst_node, lst_lai, lst_DWtotal, lst_DWfruit = ([] for i in range(5))
lst_DWmature, lst_Pg, lst_Rm = ([] for i in range(3))
# 歷史氣象
lst_datetime_his, lst_node_his, lst_lai_his, lst_DWtotal_his = ([] for i in range(4))
lst_DWfruit_his, lst_DWmature_his, lst_Pg_his, lst_Rm_his = ([] for i in range(4))
# 升溫氣象
lst_datetime_Up, lst_node_Up, lst_lai_Up, lst_DWtotal_Up = ([] for i in range(4))
lst_DWfruit_Up, lst_DWmature_Up, lst_Pg_Up, lst_Rm_Up = ([] for i in range(4))
# 降溫情境
lst_datetime_Dn, lst_node_Dn, lst_lai_Dn, lst_DWtotal_Dn = ([] for i in range(4))
lst_DWfruit_Dn, lst_DWmature_Dn, lst_Pg_Dn, lst_Rm_Dn = ([] for i in range(4))


#%% 跑程式
# 當年度觀測數值
with open (outputName, 'w',newline='') as csvwrite:
    writer = csv.writer(csvwrite, delimiter=',')
    header = ["Date","Node","LAI","AboveGroundDW","FruitDW","MatureFruitDW","Pg","Rm","GRnet","Note"] 
    writer.writerow(header)
    
    # reading observd weather file
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
                       
            #1 start calculate - observed           
            MainStemNode.update(temperature)
            Assimilate.update(temperature,ppfd,MainStemNode,Sink1)
            # daily accumulation of sink and source addtion rate
            dailyPg += Assimilate.Pg
            dailyRm += Assimilate.Rm
            dailyGRnet += Assimilate.GRnet
            dNdday += MainStemNode.dNdt
            #2 更新物件屬性-升溫情境 (這邊都跟observe一樣)
            MainStemNodeUp.update(temperature)
            AssimilateUp.update(temperature, ppfd, MainStemNodeUp,SinkUp)
            # dailyPg_up += AssimilateUp.Pg
            # dailyRm_up += AssimilateUp.Rm
            # dailyGRnet_up += AssimilateUp.GRnet
            # dNdday_up += MainStemNodeUp.dNdt
            
            #3 更新物件屬性 - 降溫情境 (和observed一樣)
            MainStemNodeDn.update(temperature)
            AssimilateDn.update(temperature,ppfd, MainStemNodeDn,SinkDn)
            # dailyPg_dn += AssimilateDn.Pg
            # dailyRm_dn += AssimilateDn.Rm
            # dailyGRnet_dn += AssimilateDn.GRnet
            # dNdday_dn += MainStemNodeDn.dNdt
            
            #calculate temperature
            # sumation here output at hour = 23 (end of the day)
            tempSum += temperature 
            if hour >= 6 and hour <= 18:
                tempDay += temperature 
            # finishing sum temperature
            if hour == 23: 
                # calculate source                
                Td = tempSum/24  # daily average
                Tdaytime = tempDay/13 # daytime average
                # calculate sink, which is in daily timestep
                Sink1.update(Td,Tdaytime,MainStemNode,dNdday,dailyGRnet)
                print(dateTime,round(Sink1.W,1),round(Sink1.Wf,1))
                # 更新物件屬性 直接使用observed的變數
                SinkUp.update(Td,Tdaytime,MainStemNodeUp,dNdday,dailyGRnet)
                SinkDn.update(Td,Tdaytime,MainStemNodeDn,dNdday,dailyGRnet)

                # write to table 
                toWrite = [dateTime,MainStemNode.node,MainStemNode.LAI,Sink1.W,Sink1.Wf,Sink1.Wm]
                toWrite.extend([dailyPg,dailyRm,dailyGRnet,"Observed"])
                writer.writerow(toWrite)
                
                # prepare list for ploting
                lst_datetime.append(dateTime)
                lst_node.append(MainStemNode.node)
                lst_lai.append(MainStemNode.LAI)
                lst_DWtotal.append(Sink1.W)
                lst_DWfruit.append(Sink1.Wf)
                lst_DWmature.append(Sink1.Wm)
                lst_Pg.append(dailyPg)
                lst_Rm.append(dailyRm)
                
                # reinitialized variable into 0
                tempSum,tempDay, dailyPg,dailyRm,dailyGRnet,dNdday = (0,)*6

            # 最後一天
            dayStart_his = dateTime # updating the presenting date
            # ---- end of runding observed wea

    # reading history weather file, 同時跑升溫和降溫情境
    # 接續寫入輸出文字檔，如此一來output file就會有所有情境資料
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

            # 計算source - hourly timestep
            #1 start calculate - history           
            MainStemNode.update(temperature)
            Assimilate.update(temperature,ppfd,MainStemNode,Sink1)
            # daily accumulation of sink and source addtion rate
            dailyPg += Assimilate.Pg
            dailyRm += Assimilate.Rm
            dailyGRnet += Assimilate.GRnet
            dNdday += MainStemNode.dNdt
            
            #2 更新物件屬性 - 升溫情境 使用tmpUpHour計算
            tmpUpHour = temperature + Range_temperature
            MainStemNodeUp.update(tmpUpHour)
            AssimilateUp.update(tmpUpHour, ppfd, MainStemNodeUp,SinkUp)
            # daily accumulation of sink and source
            dailyPg_up += AssimilateUp.Pg
            dailyRm_up += AssimilateUp.Rm
            dailyGRnet_up += AssimilateUp.GRnet
            dNdday_up += MainStemNodeUp.dNdt
                       
            #3 更新物件屬性 - 降溫情境  使用tmpDnHour
            tmpDnHour = max(0,temperature - Range_temperature)
            MainStemNodeDn.update(tmpDnHour)
            AssimilateDn.update(tmpDnHour,ppfd, MainStemNodeDn,SinkDn)
            # daily accumulation
            dailyPg_dn += AssimilateDn.Pg
            dailyRm_dn += AssimilateDn.Rm
            dailyGRnet_dn += AssimilateDn.GRnet
            dNdday_dn += MainStemNodeDn.dNdt
            
            # 計算每日平均溫度與日間溫度，用於計算Sink strength
            # sumation here output at hour = 23 (end of the day)
            tempSum += temperature
            tempSum_dn += max(0, temperature - Range_temperature )
            # 日間溫度累計
            if hour >= 6 and hour <= 18:
                tempDay += temperature 
                tempDay_dn += max(0, temperature - Range_temperature)
            # finishing sum temperature          
            if hour == 23: 
                # calculate source                
                Td = tempSum/24  # daily average
                Tdaytime = tempDay/13 # daytime average
                Td_up = Td + Range_temperature 
                Tdaytime_up = Tdaytime + Range_temperature
                Td_dn = tempSum_dn/24 - Range_temperature 
                Tdaytime_dn = Tdaytime - Range_temperature
                
                ## -- Sink strength -- 這裡是 daily time step
                #1 history
                Sink1.update(Td,Tdaytime,MainStemNode,dNdday,dailyGRnet)
                print(dateTime,round(Sink1.W,1),round(Sink1.Wf,1))
                #1 write to table in csv
                toWrite = [dateTime,MainStemNode.node,MainStemNode.LAI,Sink1.W,Sink1.Wf,Sink1.Wm]
                toWrite.extend([dailyPg,dailyRm,dailyGRnet,"History"])
                writer.writerow(toWrite)
                #2 升溫情境
                SinkUp.update(Td_up,Tdaytime_up,MainStemNodeUp,dNdday_up,dailyGRnet_up)
                toWrite = [dateTime,MainStemNodeUp.node,MainStemNodeUp.LAI,SinkUp.W,SinkUp.Wf,SinkUp.Wm]
                toWrite.extend([dailyPg_up,dailyRm_up,dailyGRnet_up,"ElevatedTemp"])               
                #3 降溫情境
                SinkDn.update(Td_dn,Tdaytime_dn,MainStemNodeDn,dNdday_dn,dailyGRnet_dn)
                toWrite = [dateTime,MainStemNodeDn.node,MainStemNodeDn.LAI,SinkDn.W,SinkDn.Wf,SinkDn.Wm]
                toWrite.extend([dailyPg_dn,dailyRm_dn,dailyGRnet_dn,"ReducedTemp"])  
                
                # prepare list for ploting
                #1 歷史標準
                lst_datetime_his.append(dateTime)
                lst_node_his.append(MainStemNode.node)
                lst_lai_his.append(MainStemNode.LAI)
                lst_DWtotal_his.append(Sink1.W)
                lst_DWfruit_his.append(Sink1.Wf)
                lst_DWmature_his.append(Sink1.Wm)
                lst_Pg_his.append(dailyPg)
                lst_Rm_his.append(dailyRm)
                #2 升溫情境
                lst_datetime_Up.append(dateTime)
                lst_node_Up.append(MainStemNodeUp.node)
                lst_lai_Up.append(MainStemNodeUp.LAI)
                lst_DWtotal_Up.append(SinkUp.W)
                lst_DWfruit_Up.append(SinkUp.Wf)
                lst_DWmature_Up.append(SinkUp.Wm)
                lst_Pg_Up.append(dailyPg_up)
                lst_Rm_Up.append(dailyRm_up)
                #3 降溫情境
                lst_datetime_Dn.append(dateTime)
                lst_node_Dn.append(MainStemNodeDn.node)
                lst_lai_Dn.append(MainStemNodeDn.LAI)
                lst_DWtotal_Dn.append(SinkDn.W)
                lst_DWfruit_Dn.append(SinkDn.Wf)
                lst_DWmature_Dn.append(SinkDn.Wm)
                lst_Pg_Dn.append(dailyPg_dn)
                lst_Rm_Dn.append(dailyRm_dn)  
                # 完成所有的資料輸出，變數歸零
                # reinitialized variable into 0
                tempSum, tempDay, dailyPg,dailyRm,dailyGRnet, dNdday = (0,)*6
                tempSum_up,tempDay_up, dailyPg_up,dailyRm_up,dailyGRnet_up, dNdday_up = (0,)*6
                tempSum_dn,tempDay_dn, dailyPg_dn,dailyRm_dn,dailyGRnet_dn, dNdday_dn = (0,)*6

            # ---- end of running history wea


#%% 繪圖區1-各種指標
# ploting 
plt.rcParams['font.sans-serif'] = 'Microsoft JhengHei'
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=[16,9],dpi=150)
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
plt.show()                


## 碳平衡
# lst_date = lst_datetime + lst_datetime_his
# lst_Pg_all = lst_Pg + lst_Pg_his
# lst_Pg_allUp = lst_Pg + lst_Pg_Up
# lst_Rm_all = lst_Rm + lst_Rm_his
# plt.plot(lst_date, lst_Pg_all, label='總光合作用')
# plt.plot(lst_date, lst_Pg_allUp, label = '總光合作用(升溫)')
# plt.plot(lst_date, lst_Rm_all, label='呼吸作用')
# plt.legend()
# plt.title('碳平衡')
# plt.ylabel('速率(µmol m-2 s-1)')
# plt.show()                


#%% 繪圖區2-葉面積指數&每周鮮重
# 增加每周為單位的列表，以每七天為單位，目前的輸出是乾重，要乘上水分含量
# 才會得到鮮重的資料

deltaDay = 7 # weekly
counter = 0
wk_date = [] # list for weekly date
wk_DWmature = [] # list for weekly mature fruit weight
fruitDW0 = 0 # set the initial condition of fruit weight to 0
# 觀測日資料改為周生長
for d in range(len(lst_DWmature)):
    if counter%deltaDay == 0:
        wk_date.append( lst_datetime[d])
        fruitDW1 = lst_DWmature[d]
        deltaFruitDW = max(0,fruitDW1 - fruitDW0) # weekly accumulated
        deltaFruitFW = deltaFruitDW*20/1000 #假設水分含量95%，換算成kg/m2
        wk_DWmature.append(deltaFruitFW)
        fruitDW0 = fruitDW1 # pass到舊的fruitDW，作為下周的基礎
        
    counter += 1

# 初始化其他情境的list
#1. history
counter = 0
wk_date_his = []
wk_DWmature_his = []
fruitDW0_his = fruitDW0
#2 升溫
wk_date_his_up = []
wk_DWmature_his_up = []
fruitDW0_his_up = fruitDW0
#3 降溫
wk_date_his_down = []
wk_DWmature_his_down = []
fruitDW0_his_down = fruitDW0

# 歷史平均值
for d in range(len(lst_DWmature_his)):
    if counter%deltaDay == 0:
        wk_date_his.append( lst_datetime_his[d])
        fruitDW1_his = lst_DWmature_his[d]
        deltaFruitDW_his = max(0,fruitDW1_his - fruitDW0_his)
        deltaFruitFW_his = deltaFruitDW_his*20/1000
        wk_DWmature_his.append(deltaFruitFW_his)
        fruitDW0_his = fruitDW1_his               

        wk_date_his_up.append( lst_datetime_Up[d])
        fruitDW1_his_up = lst_DWmature_Up[d]
        deltaFruitDW_his_up = max(0,fruitDW1_his_up - fruitDW0_his_up)
        deltaFruitFW_his_up = deltaFruitDW_his_up*20/1000
        wk_DWmature_his_up.append(deltaFruitFW_his_up)
        fruitDW0_his_up = fruitDW1_his_up
        
# 歷史平均值降溫
        wk_date_his_down.append( lst_datetime_Dn[d])
        fruitDW1_his_down = lst_DWmature_Dn[d]
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
plt.figure(figsize=[10,7.5],dpi=150)

plt.subplot(211)
plt.plot(lst_datetime_his,lst_lai_his,label='history',color = "#C0C0C0")
plt.plot(lst_datetime,lst_lai,label='now',linewidth=3)
# plt.plot(lst_datetime_his_up,lst_lai_his_up,label='history_up',color = "#C08080")
# plt.plot(lst_datetime_his_down,lst_lai_his_down,label='history_down',color = "#408080")
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
plt.show()


plt.figure(figsize=[10,7.5],dpi=150)
plt.plot(wk_date_his, wk_DWmature_his,label='history',color = "#C0C0C0")
plt.plot(wk_date_his_up, wk_DWmature_his_up,label='history_up',color = "#FF0000",linestyle='--',alpha = 0.5)
plt.plot(wk_date_his_down, wk_DWmature_his_down,label='history_down',color = "#0000FF",linestyle='--',alpha = 0.5)
plt.fill_between(wk_date_his_up, y1 = wk_DWmature_his_up,y2 = wk_DWmature_his_down,color = "#FFFF00",alpha = 0.25)
plt.plot(wk_date, wk_DWmature,label='now',linewidth=3,marker='o')
plt.legend()
plt.ylabel('每周鮮重 (kg/m2)')
plt.title('每周產量')
plt.xlabel('\n※ 溫度幅度為正負 '+ str(Range_temperature)+' 度',loc='left')
plt.show()
