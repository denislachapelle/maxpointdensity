# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 21:18:12 2020

@author: denis
"""

import numpy as np

#simple change

class Maxp():
####
    def InitMaxp(self):
      
        self.ArrayOfPoints=np.zeros((2, 2, self.NumberOfPoints))
        self.CurrentArray=0 #either 0 or 1.
        self.PreviousQuality=float('-inf') 
        self.NewQuality=0
        self.LoopCount=0
        self.BetterCount=0
        self.LastLoopCount=0
        self.Shape="Circle"
        
    def Quality(self, Points, NumberOfPoints):
        #compute the sum of distance quality.
        Sum=0
        for i in range(0, NumberOfPoints-1):
            for j in range(i+1, NumberOfPoints):
                ds=np.power(Points[0, i]-Points[0, j], 2) + np.power(Points[1, i]-Points[1, j], 2) 
                if(ds<1):
                    Sum=Sum+np.log(ds)
                else:
                     Sum=Sum+np.log(1)
    
        #Find the minimum square.
        Minx=np.amin(Points[0])
        Maxx=np.amax(Points[0])
        Miny=np.amin(Points[1])
        Maxy=np.amax(Points[1])
      
        if self.Shape=="Square":
            Area=np.amax([np.power(Maxx-Minx, 2), np.power(Maxy-Miny, 2)])        
            RetVal=Sum-np.log(Area)#/NumberOfPoints     
        elif self.Shape=="Circle":    #circle
            Area=np.amax(np.power(Points[0], 2) + np.power(Points[1], 2))  
            RetVal=Sum-np.log(Area) #/NumberOfPoints 
        else:
            print( "Square or Circle")
       
        return RetVal
        

    def Search(self):
        
        self.LoopCount=self.LoopCount+1
        Delta=self.StepSize*(np.random.rand(2, self.NumberOfPoints)*2.0-1.0)
        Delta[0,0]=0
        Delta[1,0]=0
        self.ArrayOfPoints[(self.CurrentArray+1)%2]=self.ArrayOfPoints[self.CurrentArray]+Delta
        self.NewQuality= self.Quality(self.ArrayOfPoints[(self.CurrentArray+1)%2], self.NumberOfPoints)
        if(self.NewQuality>self.PreviousQuality):
            self.BetterCount=self.BetterCount+1
#            LastLoopCount=self.LoopCount
            self.CurrentArray=(self.CurrentArray+1)%2
            self.PreviousQuality=self.NewQuality
#            print("A better set",self.BetterCount, LastLoopCount, PreviousQuality)
        return self.LoopCount
#        ax1.plot(ArrayOfPoints[CurrentArray, 0], ArrayOfPoints[CurrentArray, 1], 'r+')
#        ax1.draw()

        
#        print("Last set", self.BetterCount, LastLoopCount, PreviousQuality)

#ax2.plot(ArrayOfPoints[CurrentArray, 0], ArrayOfPoints[CurrentArray, 1], 'r+')

#plt.show()
        
    def SetStepSize(self, StepSize):
        self.StepSize=StepSize
    def SetMaxLoopCount(self, MaxLoopCount):
        self.MaxLoopCount=MaxLoopCount
    def SetNumberOfPoints(self, NumberOfPoints):
        self.NumberOfPoints=NumberOfPoints
    def SetShape(self, Shape):
        self.Shape=Shape
        
        
    def GetArrayOfPoints(self):
        return(self.ArrayOfPoints[self.CurrentArray])
        
    def GetQuality(self):
        return(self.PreviousQuality)
