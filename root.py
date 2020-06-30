# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 07:05:43 2020

This program finds the smallest square to fit N points.
It was inspired by the ditanciation require due to covid-19.
This file creates the application and start the dialog.


@author: denis lachapelle
"""

import maxp as Maxp
import mydialog as MyDialog
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
import sys



    

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    md = MyDialog.MyDialog()
            
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    
    