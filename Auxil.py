# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 15:52:12 2022

@author: dpira
"""

import datetime
import Classes
import os
from enum import Enum

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
    groupAliases = {}
    
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
                elif len(stripped) == 3 and stripped[0] == "GroupAlias":
                    groupAliases[stripped[1]] = stripped[2]
                
    if experiment.StartFrom == "challenge" and experiment.ChallengeDate != None:
        experiment.StartDate = experiment.ChallengeDate
    elif experiment.StartFrom == "treatment" and experiment.TreatmentDate != None:
        experiment.StartDate = experiment.TreatmentDate
    
    return groupAliases

def AliasGroupLabels(experiment, groupAliases):
    for group in experiment.Groups:
        origLabel = str(group.Label) 
        if origLabel in groupAliases:
            group.Label = groupAliases[origLabel]

    for mouse in experiment.Mice:
        origLabel = str(mouse.Group) 
        if origLabel in groupAliases:
            mouse.Group = groupAliases[origLabel]

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
    currentGroup = GetOrCreateGroup(groupName, experiment)
    newMouse = Classes.Mouse(label, cage, currentGroup)
    cage.Mice.append(newMouse)
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
        experiment.MeasurementDates.append(m.Date)
    
    if experiment.StartDate == None:
        experiment.StartDate = startDate
    
    experiment.EndDate = endDate
    
    experiment.MeasurementDates.sort()
    for date in experiment.MeasurementDates:
        elapsed = (date - experiment.StartDate).days
        experiment.MeasurementElapsedDays.append(elapsed)
    
    return

def CloneExperiment(experiment):
    clonedExperiment = Classes.Experiment()
    clonedExperiment.ChallengeDate = experiment.ChallengeDate
    clonedExperiment.EndDate = experiment.EndDate
    clonedExperiment.MeasurementDates = experiment.MeasurementDates
    clonedExperiment.MeasurementElapsedDays = experiment.MeasurementElapsedDays
    clonedExperiment.StartDate = experiment.StartDate
    clonedExperiment.StartFrom = experiment.StartFrom
    clonedExperiment.TreatmentDate = experiment.TreatmentDate

    for cage in experiment.Cages:
        for mouse in cage.Mice:
            sourceCage = GetOrCreateCage(clonedExperiment.Cages, mouse.Cage.Number, mouse.Cage.ID, mouse.Cage.OrigID)
            clonedMouse = GetOrCreateMouse(mouse.Label, sourceCage, mouse.Group.Label, clonedExperiment)
            
            for tumor in mouse.Tumors:
                clonedTumor = Classes.Tumor(tumor.Label)
                for timepoint in tumor.TimePoints:
                    clonedTimepointTumor = Classes.TumorTimePoint(timepoint.Date, experiment.StartDate)
                    clonedTimepointTumor.Volume = timepoint.Volume
                    for node in timepoint.Nodes:
                        clonedNode = Classes.TumorNode(node.Axis1, node.Axis2)
                        clonedTimepointTumor.Nodes.append(clonedNode)
                    clonedTumor.TimePoints.append(clonedTimepointTumor)
                clonedMouse.Tumors.append(clonedTumor)
            
            for dataSet in mouse.OtherMeasurements:
                clonedDataSet = Classes.OtherMeasurement(dataSet.Label)
                for timepoint in dataSet.TimePoints:
                    clonedTimepointData = Classes.OtherMeasurementTimePoint(timepoint.Date, experiment.StartDate, timepoint.Value)
                    clonedDataSet.TimePoints.append(clonedTimepointData)
                clonedMouse.OtherMeasurements.append(clonedDataSet)
                
            for group in clonedExperiment.Groups:
                UpdateGroupOrigID(group, experiment.Groups)
                 
    if GroupNamesAreNumeric(clonedExperiment, GroupLabelType.OrigLabel):
        clonedExperiment.Groups.sort(key = lambda x: x.OrigLabel)
    return clonedExperiment

def UpdateGroupOrigID(group, origGroups):
    for origGroup in origGroups:
        if group.Label == origGroup.Label:
            group.OrigLabel = origGroup.OrigLabel
            return
        
def GroupNamesAreNumeric(experiment, whichLabel):
    for group in experiment.Groups:
        if whichLabel == GroupLabelType.Label and not IsNumeric(group.Label):
            return False
        elif whichLabel == GroupLabelType.OrigLabel and not IsNumeric(group.OrigLabel):
            return False
    return True

class GroupLabelType(Enum):
    Label = 1
    OrigLabel = 2