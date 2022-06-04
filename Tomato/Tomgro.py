
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 16:45:32 2021
@author: ccchen
"""
# Jones(1991) "A dynamix tomato growth and yield model(TOMGRO)"
# Jones(1999) "Reduced state-variable tomato growth model"
# Heuvelink(1994) "Dry-matter partitioning in a tomato crop:Comparison of two simulation models"

import numpy as np
import math
import random
random.seed( 2021 )
# global variable 
density = 2.79 # plant density(plant/m2)


class Node:
    # should be called hourly
    LARmax = 0.5
    Tbase = 8
    Topt = 32.1
    Tceil = 43.7
    LAI_up = 1.5
    LAI_cut = 0.3
    
    def __init__(self):
        self.node = 2
        self.dNdt = 0
        self.LAI = 0.002 # (m2/m2), 
        self.LDW_cut = 0
        
    def update(self,t_hour):
        self.dNdt = self.beta_fn(t_hour,self.LARmax,self.Topt,self.Tceil)/24 
        self.node += self.dNdt
        if self.node > 50:
            self.node = 50
        self.LAI += self.dLAIdt()
        # adding 
        if self.LAI > self.LAI_up:
            self.LAI_cut = float('{:.2f}'.format(random.uniform(0.2, 0.4))) # set cut random
            self.LAI = self.LAI-self.LAI_cut
        self.LDW_cut += self.LAI_cut*density/130 # SLA
        
    def beta_fn(self,t, Rmax, t_o, t_c):
        t_b = 0
        beta = 1
        if (t <= t_b or t > t_c):
            return 0
        f = (t - t_b) / (t_o - t_b)
        g = (t_c - t) / (t_c - t_o)
        alpha = beta*(t_o - t_b) / (t_c - t_o)
    
        return Rmax*pow(f, alpha)*pow(g, beta)
    # The rate of LAI(Leaf Area Index) development
    def dLAIdt(self):
        sigma = 0.021 # plant parameter
        betaLai = 0.3 # plant parameter
        
        Nb = 6 # plant parameter
        a = math.exp(betaLai*(self.node-Nb))
        rate = density*sigma*a/(1+a)*self.dNdt
        return rate

# LARmax - maximum leaf appearance rate        
# node - main stem node number
# Tbase - base temperature for leaf development
# Topt - optimum temperature for leaf development
# Tceil - ceiling temperature for leaf development
# dLAIdt - leaf area expansion rate  

class Source:
    # this function should be calculated in hourly timestep
    def __init__(self,CO2,class_node):
        self.LFmax = 0.0693*CO2 # tau (CO2 use efficiency = 0.0693)
        self.lai = class_node.LAI
        self.Pg = 0
        self.Rm = 0
        self.GRnet = 0
    
    def update(self,temp,ppfd,class_node,class_sink):
        self.lai = class_node.LAI
        self.pruningLW = class_node.LDW_cut
        self.Pg = self.grossPhotosyn(temp,ppfd)/24 #hourly
        self.Rm = self.respiration(temp,class_sink)/24
        self.GRnet = self.netAssimilate(class_sink)
        
        

    def grossPhotosyn(self,T, PPFD):
        # Jones (1991)
        # temperature function
        if(T > 0 and T <= 12):
            PGRED =  1.0 / 12.0 * T
        elif(T > 12 and T < 35):
            PGRED =  1.0
        else:
            PGRED = 0
        # the D value is daily 
        D = 2.593   #P coefficient to convert Pg from CO2 to CH2O; Jones(1991) 
                    # convert CO2 to CH2O molecular basis: 30/44 = 0.682
                    # convert unit from umol/ms/s to g/m2/day
                    # 44/100000 (g/umol) * 3600 (s/hour) * 24(hour/day)*0.682 (CH2O/CO2)= 2.593
        K = 0.58 #P light extinction coefficient; Jones(1991)
        m = 0.1 #P leaf light transmission coefficient; Jones(1991)
        Qe = 0.0645 #P leaf quantum efficiency; Jones(1991)
        LFmax = self.LFmax
        LAI = self.lai

        a = D * LFmax * PGRED / K
        b = np.log(((1-m) * LFmax + Qe * K * PPFD) / 
                   ((1-m) * LFmax + Qe * K * PPFD * np.exp(-1 * K * LAI)))
        return  a * b

    def respiration(self,T,class_sink):
        #Jones(1999)
        #Hourly Data!
        Q10 = 1.4 #P Jones(1991)
        rm = 0.010 #P Jones(1999)
        W = class_sink.W
        Wm = class_sink.Wm
        return pow(Q10,(T-20)/10) * rm * (W-Wm-self.pruningLW) # end of function
    
    def netAssimilate(self,class_sink):
        E = 0.717 #P convert efficiency; Dimokas(2009)
        fR = class_sink.fR
        return max(0, E * (self.Pg - self.Rm) * (1 - fR))


# Pg - gross photosynthesis, computed hourly
# Rm - respiration, computed hourly by Q10 function
# GRnet - net assimilate
# W - aboveground dry weight (g/m2)
# Wm - mature druit dry weight (g/m2)
# rm - maintenance respiration coefficience g[CH2O]/m2/day
# temp - hourly temperature
'''
Jones(1999) "Reduced state-variable tomato growth model"

Pg      Gross photosynthesis, integrated over a day  (g[CH2O]/m2/day)
Rm      Daily maintenance respiration                (g[CH2O]/m2/day)
GRnet   Net aboveground growth rate                  (g[d.w.]/m2/day)
W       Aboveground dry weight                       (g[d.w.]/m2)
WM      Mature fruit dry weight                      (g[d.w.]/m2)
rm      Maintenance respiration coefficient          (g[CH2O]/g[d.w.]/day)
T       Hourly temperature                           (°C)

'''

class Sink:
    # daily time step
    # the input of source should be daily basis
    # sending the daily Td, Tdaytime,Pg, Rm, and GRnet from main,
    # should make another class for daily calculation
    
    #NFF = 22.0 # Nodes per plant when first fruit appears; Jones(1999)
    NFF = 15 # green house experiment
    def __init__(self,cls_node):
        self.lai = cls_node.LAI
        self.W = 0 # above ground DW
        self.Wf = 0 #  total fruit DW
        self.Wm = 0 # mature fruit DW
        self.fR = 0.2034 # partition of assimilate to root
        self.WRate = 0
        self.WfRate = 0
    
    def update(self,Td,Tdaytime,cls_node,dNdday, dailyGRnet):
        self.nodeNum = cls_node.node
        self.lai = cls_node.LAI
        self.WRate = self.dWdt(dNdday,dailyGRnet)
        self.WfRate = self.dWfdt(Td,Tdaytime,dailyGRnet)
        self.WmRate = self.dWmdt(Tdaytime)
        self.fR = self.rootFraction()
        self.W += self.WRate
        self.Wf += self.WfRate
        self.Wm += self.WmRate
     
    
    def dWdt(self,dNdday,dailyGRnet):  # above ground dry weight 
        # using the equation from (Jones, 1999)
        LAImax = 4.0 #P Jones(1999)
        # the LAImax should be changed into lower or using 
        # pruning module to modify LAI in Node class
        if(self.lai >= LAImax):
            p1 = 2.0 #P Jones(1999)
        else:
            p1 = 0

        Vmax = 8.0 #P Jones(1999)
        a = dailyGRnet - p1 * density * dNdday # equation 9
        b = self.WfRate + (Vmax - p1) * density * dNdday #equation 10
        # assuming maximum rate of vegetative growth restricted the limit of fruit

        return max(0,min(a, b)) # end of the function

    def rootFraction(self):
        #root phenology-dependent fraction; Jones(1991)
        if(self.nodeNum >= 30):# leaf number 
            return 0.07
        return -0.0046 * self.nodeNum + 0.2034

    def dWfdt(self,Td,Tdaytime,dailyGRnet): #  fruit weight growth rate
        # equaiton 7 (Jones, 1999)
        alphaF = 0.80 # Maximum partitioning of new growth to fruit; Jones(1999)
        #v = 0.200 # Transition coefficient between vegetative and full fruit growth (table 4)
        v = 1
        
        # temperature function 1 - fF(Td):using Td (average daily temperature)
        # effect of cool average daily temperature on partitioning of vegetative 
        # and reprotductive growth
        fF = 0.5 #P ORIGINAL
        if Td > 8 and Td <= 28:
            fF = 0.0017 * Td - 0.0147
        elif Td > 28:
            fF = 0.032
        else: 
            fF = 0.5
        fF = 1
  
        # temperature function 2 - gT : using Tdaytime
        T_crit = 24.4 # mean daytime temperature above which fruit abortion start (Jones, 1999)
        if Tdaytime < T_crit :
            gT = 0
        else:
            gT = 1.0 - 0.154 *(Tdaytime - T_crit)
        gT = 1    
        # equation 7
        if self.nodeNum <= self.NFF:
            WfRate = 0
        else:
            WfRate = dailyGRnet* alphaF * fF * (1- math.exp(v*(self.NFF-self.nodeNum))) * gT

        return WfRate # end of the function 


    def dWmdt(self,Tdaytime): 

        #kappaF = 5.0 #P Jones(1999) 
        kappaF = 3
        # temperature function Df - fruit agint using hourly temperature
        if Tdaytime > 9 and Tdaytime <= 28:
            Df = 0.0017 * Tdaytime - 0.015
        elif Tdaytime >28 and Tdaytime <= 35:
            Df = 0.032
        else:
            Df = 0
        
        # node addition rate to scaling fruit mature
        if self.nodeNum <= self.NFF + kappaF:
            WmRate = 0
        else:
            WmRate = Df * (self.Wf- self.Wm)
        
        return WmRate 

# W- above ground dry weight (g/m2)
# Wf - total fruit dry weight  (g/m2)
# Wm - mature fruit dry weight (g/m2)
# Tdaytime - average temperature during daytime hour (degree C)
# Td - average daily temperature (degree C)
# alphaF - maximum partitioning of new growth of fruit
# kappaF - developmetn time from frist fruit to first ripe fruit (node)
'''
Jones(1999) "Reduced state-variable tomato growth model"

W           Aboveground dry weight                                   (g[d.w.]/m2)
WF          Total fruit dry weight                                   (g[d.w.]/m2)
WM          Mature fruit dry weight                                  (g[d.w.]/m2)
Tdaytime    Average temperature during daytime hours                 (°C)
Td          Average daily temperature                                (°C)
αF          Maximum partitioning of new growth to fruit              ([fraction]/day)
κF          Development time from first fruit to first ripe fruit    (node)

'''

