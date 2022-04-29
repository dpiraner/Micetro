# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 15:52:12 2022

@author: dpira
"""

import datetime
import Classes
import os

def StringToDate(dateStr, sepChar):
    split = dateStr.split(sepChar)
    return StrArrayToDate(split)

def StrArrayToDate(arr):
    if len(arr) >=3:
            year = -1
            month = -1
            day = -1
            
            if (len(arr[0]) == 4) and (arr[0].isdigit() == True):
                year = int(arr[0])
                
            if (len(arr[1]) == 2) and (arr[1].isdigit() == True):
                month = int(arr[1])
            
            if (len(arr[2]) == 2) and (arr[2].isdigit() == True):
                day = int(arr[2])
              
            if (year >= 0 and month >= 0 and day >= 0):
                return datetime.datetime(year, month, day)
    return None        

def LoadExperimentInfo(experiment, currentDir):
    settingsPath = os.path.join(currentDir, "micetro.txt")
    if os.path.exists(settingsPath):
        print("Found Micetro settings file.")
        with open(settingsPath) as f:
            lines = f.readlines()
            for line in lines:
                split = line.split(':')
                stripped = list(map(str.strip, split))
                print(stripped)
                if len(stripped) == 2:
                    setting = stripped[0]
                    value = stripped[1]
                    
                    if setting == "tumor":
                        print ("setting = tumor")
                        experiment.ChallengeDate = StringToDate(value, ' ')
                    elif setting == "treatment":
                        print ("setting = treatment")
                        experiment.TreatmentDate = StringToDate(value, ' ')
                    elif setting == "start from":
                        print ("setting = start")
                        if value == 'tumor' or value == 'challenge':
                            experiment.StartFrom = "challenge"
                        else:
                            experiment.StartFrom = 'treatment'
                            
                            
    if experiment.StartFrom == "challenge" and experiment.ChallengeDate != None:
        experiment.StartDate = experiment.ChallengeDate
    elif experiment.StartFrom == "treatment" and experiment.TreatmentDate != None:
        experiment.StartDate = experiment.TreatmentDate
    return


def GetSuperHeaderNames(df):
    prelim = list(df.columns)
    output = []
    for entry in prelim:
        output.append(entry.split('.')[0]) #pandas appends .1, .2, etc to otherwise duplicate column headers
    return output

def IsNumeric(x):
    if isinstance(x, int):
        return True
    if isinstance(x, float):
        return True
    return False

def GetOrCreateCage(cages, number, ID, origID):    
    for cage in cages:
        if cage.Number == number:
            return cage
        
    newCage = Classes.Cage(number, ID, origID)
    cages.append(newCage)
    return newCage

def GetOrCreateGroup(groupName, experiment):
    for group in experiment.Groups:
        if group.Label == groupName:
            return group
    newGroup = Classes.Group(groupName)
    experiment.Groups.append(newGroup)
    return newGroup

def GetOrCreateMouse(label, cage, groupName, experiment):
    for mouse in cage.Mice:
        if mouse.Label == label:
            return mouse
    newMouse = Classes.Mouse(label, cage, groupName)
    cage.Mice.append(newMouse)
    currentGroup = GetOrCreateGroup(groupName, experiment)
    currentGroup.Mice.append(newMouse)
    experiment.Mice.append(newMouse)
    
    return newMouse
    
def GetOrCreateTumor(mouse, tumorName):
    for tumor in mouse.Tumors:
        if tumor.Label == tumorName:
            return tumor
    newTumor = Classes.Tumor(tumorName)
    mouse.Tumors.append(newTumor)
    return newTumor

def GetOrCreateOtherMeasurement(mouse, measurementName):
    for measurement in mouse.OtherMeasurements:
        if measurement.Label == measurementName:
            return measurement
    newMeasurement = Classes.OtherMeasurement(measurementName)
    mouse.OtherMeasurements.append(newMeasurement)
    return newMeasurement

def GetExperimentBoundDates(experiment, excelMeasurements):   
    if len(excelMeasurements) == 0:
        return
    
    startDate = excelMeasurements[0].Date
    endDate = excelMeasurements[0].Date
    for m in excelMeasurements:
        if m.Date < startDate:
            startDate = m.Date
        if m.Date > endDate:
            endDate = m.Date
    
    if experiment.StartDate == None:
        experiment.StartDate = startDate
    
    experiment.EndDate = endDate
    return