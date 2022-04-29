# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 13:58:36 2022

@author: dpira
"""

import glob, os
import pandas as pd
from Classes import ExcelSheet, Experiment, TumorTimePoint, TumorNode, OtherMeasurementTimePoint
import Auxil
from pathlib import Path
import math

def LoadExcelFilesFromFolder(currentDir):
    os.chdir(currentDir)
    measurementFiles = []
    for file in glob.glob("*.xlsx"):
        fileName = Path(file).stem
        splitName = fileName.split(' ')
        fileDate = Auxil.StrArrayToDate(splitName)
        if fileDate != None:
                measurementFile = ExcelSheet(file, fileDate)
                measurementFile.DataFrame = pd.read_excel (file)
                measurementFiles.append(measurementFile)
    
    measurementFiles.sort(key = lambda x: x.Date)
    return measurementFiles


class TumorMeasurementLocation:
    def __init__(self, name):
        self.NodeColumns = []
        self.Name = name
        
class NodeColumnPair:
    def __init__(self, col_Ax1, col_Ax2):
        self.Col_Ax1 = col_Ax1
        self.Col_Ax2 = col_Ax2
        
class OtherDataLocation:
    def __init__(self, name, column):
        self.Name = name
        self.Column = column
        
def GetTumorMeasurementLocation(tumorLabel, cols_Tumors):
    for tumorMeasurementLocation in cols_Tumors:
        if tumorMeasurementLocation.Name == tumorLabel:
            return tumorMeasurementLocation
    
    newTML = TumorMeasurementLocation(tumorLabel)
    cols_Tumors.append(newTML)
    return newTML

def IsAxis(string, num):
    validStrs = [
        'Axis' + str(num),
        'axis' + str(num),
        '+ Axis' + str(num),
        '+ axis' + str(num),
        'Additional Axis' + str(num),
        'additional axis' + str(num),
        'Extra Axis' + str(num),
        'extra axis' + str(num),
        
        'Axis' + ' ' + str(num),
        'axis' + ' ' + str(num),
        '+ Axis' + ' ' + str(num),
        '+ axis' + ' ' + str(num),
        'Additional Axis' + ' ' + str(num),
        'additional axis' + ' ' + str(num),
        'Extra Axis' + ' ' + str(num),
        'extra axis' + ' ' + str(num)
        ]
    
    if string.strip() in validStrs:
        return True
    else:
        return False

def ParseExcelMeasurements(measurements, experiment):
    for measurementSession in measurements:
        print("Parsing measurements from " + str(measurementSession.Date))
        df = measurementSession.DataFrame
        superHeaders = Auxil.GetSuperHeaderNames(df)
        columnHeaders = df.iloc[0,:].values
        
        col_CageNum = -1
        col_OrigCageID = -1
        col_CageID = -1
        col_GroupID = -1
        col_AnimalID = -1
        cols_Tumors = []
        cols_Others = []
        
        colNum = -1
        for header in columnHeaders:
            colNum += 1
            if not isinstance(header, str) or header.startswith("*") or header.startswith("Axis 2"):
                continue
            elif header.startswith("Cage #"):
                col_CageNum = colNum
            elif header.startswith("Original Cage"):
                col_OrigCageID = colNum
            elif header.startswith("Cage ID"):
                col_CageID = colNum
            elif header.startswith("Group"):
                col_GroupID = colNum
            elif header.startswith("Animal"):
                col_AnimalID = colNum
            elif IsAxis(header, 1) and IsAxis(columnHeaders[colNum + 1], 2):
                tumorLoc = GetTumorMeasurementLocation(superHeaders[colNum], cols_Tumors)
                tumorLoc.NodeColumns.append(NodeColumnPair(colNum, colNum + 1))
            else:
                otherData = OtherDataLocation(header, colNum)
                cols_Others.append(otherData)
        
        for index, row in df.iterrows():
            if index == 0:
                continue
            
            cageNum = row[col_CageNum]
            if cageNum == "nan" or (Auxil.IsNumeric(cageNum) and math.isnan(cageNum)):
                continue
            
            groupID = row[col_GroupID]
            if groupID == "nan" or (Auxil.IsNumeric(groupID) and math.isnan(groupID)):
                continue
            
            animalID = row[col_AnimalID]
            if animalID == "nan" or (Auxil.IsNumeric(animalID) and math.isnan(animalID)):
                continue
            
            cage = Auxil.GetOrCreateCage(experiment.Cages, cageNum, row[col_CageID], row[col_OrigCageID])
            
            mouse = Auxil.GetOrCreateMouse(animalID, cage, groupID, experiment)
                
            for tumorData in cols_Tumors:
                tumor = Auxil.GetOrCreateTumor(mouse, tumorData.Name)
                timepoint = TumorTimePoint(measurementSession.Date, experiment.StartDate)
                for nodeColumnPair in tumorData.NodeColumns:
                    newNode = TumorNode(row[nodeColumnPair.Col_Ax1], row[nodeColumnPair.Col_Ax2])
                    timepoint.Nodes.append(newNode)
                tumor.TimePoints.append(timepoint)
            
            for otherData in cols_Others:
                otherMeasurement = Auxil.GetOrCreateOtherMeasurement(mouse, otherData.Name)
                timepoint = OtherMeasurementTimePoint(measurementSession.Date, experiment.StartDate, row[otherData.Column])
                otherMeasurement.TimePoints.append(timepoint)
                
    return experiment