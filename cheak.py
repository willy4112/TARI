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
