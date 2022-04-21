# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 13:58:36 2022

@author: dpira
"""

import glob, os
import datetime
import pandas as pd
from Classes import ExcelSheet
from pathlib import Path

def LoadExcelFilesFromFolder(currentDir):
    os.chdir(currentDir)
    measurementFiles = []
    for file in glob.glob("*.xlsx"):
        fileName = Path(file).stem
        splitName = fileName.split(' ')
        if len(splitName) >=3:
            
            year = -1
            month = -1
            day = -1
            
            if (len(splitName[0]) == 4) and (splitName[0].isdigit() == True):
                year = int(splitName[0])
                
            if (len(splitName[1]) == 2) and (splitName[1].isdigit() == True):
                month = int(splitName[1])
            
            if (len(splitName[2]) == 2) and (splitName[2].isdigit() == True):
                day = int(splitName[2])
              
            if (year >= 0 and month >= 0 and day >= 0):
                measurementDate = datetime.datetime(year, month, day)
                measurementFile = ExcelSheet(file, measurementDate)
                measurementFile.DataFrame = pd.read_excel (file)
                measurementFiles.append(measurementFile)
    
    return measurementFiles