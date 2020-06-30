# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 21:19:11 2020

This program is the dialog for exercising the maxp,py program.
It provide the controls and the visual final results and search trajectory.

@author: denis lachapelle
"""
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from PyQt5 import QtWidgets
import sys
import numpy as np
import maxp as Maxp
from PyQt5.QtCore import QTimer

class MyDialog(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        
        self.LeftPlotEnableCB = QtWidgets.QCheckBox("Cummulative", self)
        self.SquareCB = QtWidgets.QCheckBox("Square", self)
        self.CircleCB = QtWidgets.QCheckBox("Circle", self)
        
        #define the dialog layouts.
        TopLayout=QtWidgets.QGridLayout(self)
        
        ButtonLayout=QtWidgets.QVBoxLayout()
        GraphLayout=QtWidgets.QHBoxLayout()
        ParametersLayout=QtWidgets.QFormLayout()
        ResultsLayout=QtWidgets.QFormLayout()
        
        TopLayout.addLayout(ParametersLayout, 7, 2, 1, 2)
        TopLayout.addLayout(ResultsLayout, 7, 5, 1, 2)
        TopLayout.addLayout(ButtonLayout, 1, 1, 4, 1)
        TopLayout.addLayout(GraphLayout, 1, 2, 6, 6)
       
        
        #define the buttons.
        ResetButton = QtWidgets.QPushButton("Reset", self)
        ResetButton.clicked.connect(self.Reset)
        StartButton = QtWidgets.QPushButton("start", self)
        StartButton.clicked.connect(self.StartOpt)
        StopButton = QtWidgets.QPushButton("stop", self)
        LoadFileButton = QtWidgets.QPushButton("Load", self)
        StopButton.clicked.connect(self.StopOpt)
        
        SaveFileButton = QtWidgets.QPushButton("Save", self)


        #add buttons ton button layout.
        ButtonLayout.addWidget(ResetButton)
        ButtonLayout.addWidget(StartButton)
        ButtonLayout.addWidget(StopButton)
        ButtonLayout.addWidget(LoadFileButton)
        ButtonLayout.addWidget(SaveFileButton)
        ButtonLayout.addWidget(self.LeftPlotEnableCB)
        ButtonLayout.addWidget(self.SquareCB)
        ButtonLayout.addWidget(self.CircleCB)
       
        
        
        
      
        fig1 = Figure(figsize=(5, 5), dpi=100)
        self.axes1 = fig1.add_subplot(111)
        self.figCanvas1=FigureCanvas(fig1)
        self.figCanvas1.setParent(self)
        GraphLayout.addWidget(self.figCanvas1)

        fig2 = Figure(figsize=(5, 5), dpi=100)
        self.axes2 = fig2.add_subplot(111)
        self.figCanvas2=FigureCanvas(fig2)
        self.figCanvas2.setParent(self)
        GraphLayout.addWidget(self.figCanvas2)

       
        StepSizeLabel=QtWidgets.QLabel("StepSize")
        self.StepSizeText=QtWidgets.QLineEdit("0.1")
        self.StepSizeText.textChanged.connect(self.UpdateParameters)
        ParametersLayout.addRow(StepSizeLabel, self.StepSizeText)
        
        NumberOfPointsLabel=QtWidgets.QLabel("Numder of points")
        self.NumberOfPointsText=QtWidgets.QLineEdit("65")
        self.NumberOfPointsText.textChanged.connect(self.UpdateNumberOfPoints)
        ParametersLayout.addRow(NumberOfPointsLabel, self.NumberOfPointsText)
        
        MaxLoopCountLabel=QtWidgets.QLabel("Maximum Trials")
        self.MaxLoopCountText=QtWidgets.QLineEdit("100000")
        self.MaxLoopCountText.textChanged.connect(self.UpdateParameters)
        ParametersLayout.addRow(MaxLoopCountLabel, self.MaxLoopCountText)
        
        TestFieldLabel=QtWidgets.QLabel("Test Field")
        self.TestFieldText=QtWidgets.QLineEdit("ux")
        ResultsLayout.addRow(TestFieldLabel, self.TestFieldText)
        
        QualityLabel=QtWidgets.QLabel("Quality")
        self.QualityText=QtWidgets.QLineEdit("???")
        ResultsLayout.addRow(QualityLabel, self.QualityText)                  
    
        self.mp = Maxp.Maxp()
        self.Reset()
        
    
        self.Timer=QTimer(self)
        self.Timer.setInterval(0)
        self.Timer.timeout.connect(self.TimerProcess)
#        self.Timer.start() 

        
        self.show()
        self.testcounter=0
        

        
    def GetNumberOfPoints(self):
        return int(self.NumberOfPointsText.text())
    
    def GetMaxLoopCount(self):
        return int(self.MaxLoopCountText.text())

    def GetStepSize(self):
        return float(self.StepSizeText.text()) 
    
    def UpdateParameters(self):
        self.mp.SetStepSize(float(self.StepSizeText.text()))
        self.mp.SetNumberOfPoints(int(self.NumberOfPointsText.text()))
        self.mp.SetMaxLoopCount(int(self.MaxLoopCountText.text()))

    def UpdateNumberOfPoints(self):
        self.mp.SetNumberOfPoints(int(self.NumberOfPointsText.text()))
        self.Reset()
        

    def PlotLeft(self, array):
        self.axes1.clear()
        self.axes1.plot(array[0], array[1], 'r+' )
        self.figCanvas1.draw()
        
    def PlotRight(self, array):
        self.axes2.plot(array[0], array[1], 'r.' )
        self.figCanvas2.draw()
        
    def StartOpt(self):
        self.NumberOfPointsText.setReadOnly(True)
        self.Timer.start() 
        
    def StopOpt(self):
        self.NumberOfPointsText.setReadOnly(False)
        self.Timer.stop() 
        
    def Reset(self):
        self.mp.SetStepSize(float(self.StepSizeText.text()))
        self.mp.SetMaxLoopCount(int(self.MaxLoopCountText.text()))
        self.mp.SetNumberOfPoints(int(self.NumberOfPointsText.text()))
        self.mp.InitMaxp()
         
    def TimerProcess(self):
        if self.SquareCB.isChecked()==True:
            self.mp.SetShape("Square")
        elif self.CircleCB.isChecked()==True:
             self.mp.SetShape("Circle")
             
        self.testcounter=self.testcounter+1
        self.TestFieldText.setText(str(self.testcounter))
        self.PlotLeft(self.mp.GetArrayOfPoints())
        if self.LeftPlotEnableCB.isChecked() == True:
            self.PlotRight(self.mp.GetArrayOfPoints())
         
        if self.mp.Search() >= self.GetMaxLoopCount():
            self.Timer.stop()
            
        self.QualityText.setText(str(self.mp.GetQuality()))

        
