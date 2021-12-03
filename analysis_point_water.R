# -*- coding: utf-8 -*-
library(stringr)

library(ggplot2)




# file='bcc-csm1-1'
file='bcc-csm1-1_changeH2Otime'
point='1032'
year = '2030'
# t = paste('新園', year,sep = "_")
t = paste('新園', year,'c',sep = "_")

path <- paste("L:\\climate change model\\to_run\\",file,"\\TN10-spring\\spring_",point,"_chishan_",year,sep = "")

simname <- paste("spring_",point,"_chishan",sep = "")



# function

get_sim <- function (simpath, yr){
  
  d1 = as.Date(paste("01/01/",yr), "%m/%d/%Y", tz="US")
  
  
  
  head<-c("DAY","JDAY","LAREAB","LAREAM","LAREAT","LSTEMH","NBRNCH","NFLRS","PODS","RSTAGE","VSTAGE",
          
          "SEEDP", "GSEEDWT",    "CLIMAT2","CLIMAT3","CLIMAT4","CLIMAT1","CLIMAT5","SHTWT",  
          
          "ROOTWT","PSIM","WSTRESS","LSTRESS","LEAFWT","PETWT","STEMWT","SEEDWT","PODWT",
          
          "NODWT","NRATIO","SCPOOL","RCPOOL","FIXCS","USEDCS","PLANTN","NODN")
  
  
  
  sim <- read.table(file=simpath,sep="")       #"," here, read separately with header
  
  colnames(sim)<-unlist(head)        # combine header and content
  
  
  
  Date <- sim$"JDAY"-1+d1      ## make Datetime vector
  
  sim <- cbind(Date, sim) ## combine the Datetime vector into the data frame
  
  return (sim)
  
}



# read g01 - sim

fname <- paste0(path,"\\",simname,".g01")

sim <- get_sim(fname,year)





# read table - stress

fname <- paste0(path,"\\",simname,".tab")

stress <- read.table(file=fname,skip=1,nrow = length(readLines(fname))-2)

colnames(stress) <- c("DAY","DOY","Rstage","morning","daytime","time")

stress$W <- str_count(stress$daytime,"W")

d1 = as.Date(paste("01/01/",year), "%m/%d/%Y", tz="US")

Date <- stress$DOY-1+d1        ## make Datetime vector

stress <- cbind(Date,stress)



# read irrigation - water

fname = paste0(path,"\\",simname,".dat")

water <- read.table(fname, skip=2)

colnames(water) <- c("Date","depth")

water$Date <- as.Date(water$Date,"%m/%d/%y")

water$wDate <- water$Date

water$depth <- round(water$depth * 2.54,0) # inch to cm



# merge precipitation, irrigation, water stress

merge <- merge(sim[,1:18],water,by="Date",all=TRUE)

merge <- merge(merge,stress,by="Date",all=TRUE)

merge <- merge[1:(nrow(merge)-1),]



#merge$wStress = NA
for(i in c(1:(nrow(merge)))){
  
  # growth stage
  
  if(floor(merge$RSTAGE[i]) < 1){
    
    merge$Stage[i] = "V"
    
  }else{
    
    merge$Stage[i] = paste0("R",floor(merge$RSTAGE[i]))
    
  }
  # 將無灌溉時期的depth改為0
  if(is.na(merge$depth[i])){
    merge$depth[i] = 0
  } 
}

merge$wStress = merge$Date

for(i in c(1:(nrow(merge)))){
  
  if(i == 1){
    
    merge$wStress[i] = NA
    
  }else if(merge$W[i] <6){
    
    merge$wStress[i] = NA
    
  }
  
  
  
  
  
}



# set factor of growth stage

merge$Stage <- factor(merge$Stage,levels=c("V","R1","R2","R3","R4","R5","R6","R7"))


#畫出水分收支圖

# ggplot(merge)+geom_line(aes(x=Date,y=CLIMAT4*2.54),size=1) + labs(x="Date",y="Precipitation (mm/day)",title=t)+theme_bw()+
#   
#   theme(plot.title=element_text(hjust = 0.5,face="bold",size=15))+
#   
#   geom_text(aes(x=wDate,label="↓",y=1.6),color="blue",size = 15)+  
#   
#   geom_area(aes(x=Date,y=-0.4,fill=Stage),size=0,linetype=0,alpha=0.7)+
#   
#   geom_col(aes(x=wStress,y=20),alpha=0.3

# leaf area
ggplot(merge)+geom_line(aes(x=Date, y=LAREAT))+labs(x='Date',y="Leaf area (cm/plant)",title=t)+theme_bw()+
  
  theme(plot.title=element_text(hjust = 0.5,face="bold",size=15))+
  
  geom_text(aes(x=wDate,label="↓",y=330),color="blue",size = 15)+  
  
  geom_area(aes(x=Date,y=-50,fill=Stage),size=0,linetype=0,alpha=0.7)+
  
  geom_col(aes(x=wStress,y=4000),alpha=0.3)+ylim(-50,4000)
