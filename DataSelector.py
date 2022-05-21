# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 19:39:45 2022

@author: dpira
"""

import math
import Auxil
import statistics
import Classes
from scipy import mean
from scipy.stats import sem

def GetOtherDataLabels(experiment):
    otherLabels = []
    for mouse in experiment.Mice:
        for measurement in mouse.OtherMeasurements:
            if not measurement.Label in otherLabels:
                otherLabels.append(measurement.Label)
    return otherLabels

def GetDataMeasurementsByGroup(experiment, dataLabel):
    rows = []
    
    timePoints, elapsed = GetDataTimepoints(experiment, dataLabel)
    
    header = ["Measurement Date", "Elapsed Time"]
    header = header + GetMouseNamesByGroup(experiment)    
    rows.append(header)

    for i in range(len(timePoints)):
        measurementRow = [str(timePoints[i]), elapsed[i]]
        hasValues = False
        for group in experiment.Groups:
            for mouse in group.Mice:
                for dataSet in mouse.OtherMeasurements:
                    if dataSet.Label == dataLabel:
                        measurement = GetDataMeasurementAtTimePoint(dataSet, timePoints[i])
                        measurementRow.append(measurement)
                        if measurement is not None:
                            hasValues = True
        if hasValues == True: #if any values were not None                
            rows.append(measurementRow)
    return rows

def GetDataMeasurementAtTimePoint(dataSet, timePoint):
    for tp in dataSet.TimePoints:
        if tp.Date == timePoint:
            return tp.Value
    return None

def GetDataTimepoints(experiment, dataLabel):
    timePoints = []
    elapsed = []
    for mouse in experiment.Mice:
        for otherData in mouse.OtherMeasurements:
            if  otherData.Label == dataLabel:
                for timePoint in otherData.TimePoints:
                    if not timePoint.Elapsed in elapsed:
                        timePoints.append(timePoint.Date)
                        elapsed.append(timePoint.Elapsed)
    return timePoints, elapsed

def GetDataSetAveragesByGroup(experiment, dataLabel, errorMode):
    rows = []
    
    timePoints, elapsed = GetDataTimepoints(experiment, dataLabel)
    
    header = ["Measurement Date", "Elapsed Time"]
    for group in experiment.Groups:
        header.append(group.Label)
    for group in experiment.Groups:
        header.append(errorMode + " " + str(group.Label))
    rows.append(header)
    
    for i in range(len(timePoints)):
        measurementRow = [str(timePoints[i]), elapsed[i]]
        errorRow = []
        timePointHasValues = False
        groupHasValues = False
        for group in experiment.Groups:
            currentMeasurements = []
            for mouse in group.Mice:
                for dataSet in mouse.OtherMeasurements:
                    if dataSet.Label == dataLabel:
                        measurement = GetDataMeasurementAtTimePoint(dataSet, timePoints[i])
                        if measurement is not None and not math.isnan(measurement):
                            currentMeasurements.append(measurement)
                            timePointHasValues = True
                            groupHasValues = True
            if groupHasValues:
                 measurementRow.append(mean(currentMeasurements))
                 if errorMode == "StDev":
                     errorRow.append(statistics.pstdev(currentMeasurements))
                 elif errorMode == "SEM":
                     errorRow.append(sem(currentMeasurements))
            else:
                measurementRow.append(None)
                errorRow.append(None)
        if timePointHasValues == True: #if any values were not None                
            rows.append(measurementRow + errorRow)
    return rows 

def GetSurvivalData(experiment):
    rows = []
    
    header = ["Measurement Date", "Elapsed Time"]
    for group in experiment.Groups:
        header.append(group.Label)
    rows.append(header)
    
    timePoints, elapsed = GetSurvivalTimePoints(experiment)

    for i in range(len(timePoints)):
      measurementRow = [str(timePoints[i]), elapsed[i]]
      for group in experiment.Groups:
          measurementRow.append(GetGroupSurvivalAtTimePoint(group, timePoints[i]))
      rows.append(measurementRow)
      
      if i < len(timePoints) - 1: #plot the "peek ahead" time point
          measurementRow = [str(timePoints[i]), elapsed[i]]
          for group in experiment.Groups:
              measurementRow.append(GetGroupSurvivalAtTimePoint(group, timePoints[i + 1]))
          rows.append(measurementRow)
      
    return rows

def GetSurvivalTimePoints(experiment):    
    timePoints = []
    elapsed = []
    
    for mouse in experiment.Mice:
        for timepoint in mouse.Survival:
            if timepoint.Date not in timePoints:
                timePoints.append(timepoint.Date)
                elapsed.append(timepoint.Elapsed)
    
    return timePoints, elapsed

def GetGroupSurvivalAtTimePoint(group, date):
    totalMice = 0
    liveMice = 0
    for mouse in group.Mice:
        for timePoint in mouse.Survival:
            if timePoint.Date == date:
                totalMice += 1
                if timePoint.Live:
                    liveMice += 1
    if totalMice > 0:
        return liveMice / totalMice
    else:
        return math.nan

def GetDataBounds(experiment, dataLabel):
    maxData = 0
    minData = 0
    firstData = True
    for mouse in experiment.Mice:
        for dataSet in mouse.OtherMeasurements:
            if dataSet.Label == dataLabel:
                for tp in dataSet.TimePoints:
                    if tp.Value is not None and tp.Value > maxData:
                        maxData = tp.Value
                    if firstData == True:
                        minData = tp.Value
                        firstData  = False
                    elif tp.Value < minData:
                        minData = tp.Value
    return minData, maxData  

def GetTumorLabels(experiment):
    tumorLabels = []
    for mouse in experiment.Mice:
        for tumor in mouse.Tumors:
            if not tumor.Label in tumorLabels:
                tumorLabels.append(tumor.Label)
    return tumorLabels

def GetTumorTimepoints(experiment, tumorLabel):
    timePoints = []
    elapsed = []
    for mouse in experiment.Mice:
        for tumor in mouse.Tumors:
            if  tumor.Label == tumorLabel:
                for timePoint in tumor.TimePoints:
                    if not timePoint.Elapsed in elapsed:
                        timePoints.append(timePoint.Date)
                        elapsed.append(timePoint.Elapsed)
    return timePoints, elapsed

def GetMouseNamesByGroup(experiment):
    names = []
    for group in experiment.Groups:
        for mouse in group.Mice:
            names.append(str(group.Label) + ": " + str(mouse.Label))
    return names

def GetTumorMeasurement(timePoint, tumorVolumeFormula):
    
    vol = 0
    foundValidMeasurement = False
    
    for node in timePoint.Nodes:
        ax1 = node.Axis1
        ax2 = node.Axis2
        
        if Auxil.IsNumeric(ax1) and Auxil.IsNumeric(ax2) and not math.isnan(ax1) and not math.isnan(ax2):
            foundValidMeasurement = True
            
            if tumorVolumeFormula == "(L x W^2) / 2":
                L = max(ax1, ax2)
                W = min(ax1, ax2)
                vol += math.pow(W, 2) * L * 0.5

    if foundValidMeasurement:
        return vol
    else:
        return None

def ComputeTumorVolumes(experiment, tumorVolumeFormula):
    for mouse in experiment.Mice:
        for tumor in mouse.Tumors:
            for timePoint in tumor.TimePoints:
                timePoint.Volume = GetTumorMeasurement(timePoint, tumorVolumeFormula)

def GetTumorMeasurementAtTimePoint(tumor, timePoint):
    for tp in tumor.TimePoints:
        if tp.Date == timePoint:
            return tp.Volume
    return None

def GetTumorMeasurementsByGroup(experiment, tumorLabel):
    rows = []
    
    timePoints, elapsed = GetTumorTimepoints(experiment, tumorLabel)
    
    header = ["Measurement Date", "Elapsed Time"]
    header = header + GetMouseNamesByGroup(experiment)    
    rows.append(header)

    for i in range(len(timePoints)):
        measurementRow = [str(timePoints[i]), elapsed[i]]
        hasValues = False
        for group in experiment.Groups:
            for mouse in group.Mice:
                for tumor in mouse.Tumors:
                    if tumor.Label == tumorLabel:
                        volume = GetTumorMeasurementAtTimePoint(tumor, timePoints[i])
                        measurementRow.append(volume)
                        if volume is not None:
                            hasValues = True
        if hasValues == True: #if any values were not None                
            rows.append(measurementRow)
    return rows

def GetMaxTumorMeasurement(experiment, tumorLabel):
    maxVol = 0
    for mouse in experiment.Mice:
        for tumor in mouse.Tumors:
            if tumor.Label == tumorLabel:
                for tp in tumor.TimePoints:
                    if tp.Volume is not None and tp.Volume > maxVol:
                        maxVol = tp.Volume
    return maxVol    

def GetTumorAveragesByGroup(experiment, tumorLabel, errorMode):
    rows = []
    
    timePoints, elapsed = GetTumorTimepoints(experiment, tumorLabel)
    
    header = ["Measurement Date", "Elapsed Time"]
    for group in experiment.Groups:
        header.append(group.Label)
    for group in experiment.Groups:
        header.append(errorMode + " " + str(group.Label))
    rows.append(header)
    
    for i in range(len(timePoints)):
        measurementRow = [str(timePoints[i]), elapsed[i]]
        errorRow = []
        timePointHasValues = False
        groupHasValues = False
        for group in experiment.Groups:
            currentMeasurements = []
            for mouse in group.Mice:
                for tumor in mouse.Tumors:
                    if tumor.Label == tumorLabel:
                        volume = GetTumorMeasurementAtTimePoint(tumor, timePoints[i])
                        if volume is not None:
                            currentMeasurements.append(volume)
                            timePointHasValues = True
                            groupHasValues = True
            if groupHasValues:
                 measurementRow.append(mean(currentMeasurements))
                 if errorMode == "StDev":
                     errorRow.append(statistics.pstdev(currentMeasurements))
                 elif errorMode == "SEM":
                     errorRow.append(sem(currentMeasurements))
            else:
                measurementRow.append(None)
                errorRow.append(None)
        if timePointHasValues == True: #if any values were not None                
            rows.append(measurementRow + errorRow)
    return rows 
    
def AsPercentageOfFirst(experiment):
    
    clonedExperiment = Auxil.CloneExperiment(experiment)
    
    for mouse in clonedExperiment.Mice:        
        for tumor in mouse.Tumors:
            normValueFound = False
            normValue = 1
            for timepoint in tumor.TimePoints:
                if not normValueFound and timepoint.Volume is not None and not math.isnan(timepoint.Volume):
                    normValue = timepoint.Volume
                    normValueFound = True
                if timepoint.Volume is not None and not math.isnan(timepoint.Volume):
                    if normValue != 0:
                        timepoint.Volume = (timepoint.Volume - normValue) / normValue * 100
                    else:
                        timepoint.Volume = math.nan
    
        for dataset in mouse.OtherMeasurements:
            normValueFound = False
            normValue = 1
            for timepoint in dataset.TimePoints:
                if not normValueFound and timepoint.Value is not None and not math.isnan(timepoint.Value):
                    normValue = timepoint.Value
                    normValueFound = True
                if timepoint.Value is not None and not math.isnan(timepoint.Value):
                    if normValue != 0:
                        timepoint.Value = (timepoint.Value - normValue) / normValue * 100
                    else:
                        timepoint.Volume = math.nan
    return clonedExperiment

def ComputeDeathDates(experiment):
    
    allDates = [] 
    
    #first collect all measurements and fill in allDates
    for mouse in experiment.Mice:
        for tumor in mouse.Tumors:
            for tp in tumor.TimePoints:
                hasData = False
                for node in tp.Nodes:
                    if Auxil.IsNumeric(node.Axis1) and Auxil.IsNumeric(node.Axis2) and not math.isnan(node.Axis1) and not math.isnan(node.Axis2):
                        hasData = True
                        break
                    
                if not tp.Date in allDates:
                    allDates.append(tp.Date)
                
                survivalTP, _ = GetOrCreateSurvivalTimepoint(mouse, tp.Date, experiment.StartDate)
                if hasData == True:
                    survivalTP.Live = True
                    
        for otherData in mouse.OtherMeasurements:
            for tp in otherData.TimePoints:
                hasData = False
                if not math.isnan(tp.Value):
                    hasData = True
                
                if not tp.Date in allDates:
                   allDates.append(tp.Date) 
                   
                survivalTP, _ = GetOrCreateSurvivalTimepoint(mouse, tp.Date, experiment.StartDate)
                if hasData == True:
                    survivalTP.Live = True
                    
    #add manual death date
    for mouse in experiment.Mice:
        if mouse.DeathDate is not None and not mouse.DeathDate in allDates:
            allDates.append(mouse.DeathDate)
             
    #fill in measurements if necessary
    for mouse in experiment.Mice:
        for index, date in enumerate(allDates):
            survivalPoint, isNew = GetOrCreateSurvivalTimepoint(mouse, date, experiment.StartDate)
            if isNew:
                survivalPoint.IsFillIn = True
                
    #sort dates
    allDates.sort()
    for mouse in experiment.Mice:
        mouse.Survival.sort(key = lambda x: x.Date)
        
    #for measurements that are filled in, set them to the previous value
    for mouse in experiment.Mice:
        for index, date in enumerate(allDates):
            survivalPoint, _ = GetOrCreateSurvivalTimepoint(mouse, date, experiment.StartDate)
            
            #if this is a new survival point, it is because a mouse died on an unscheduled measurement date. If the death date is not explicitly set, match the live value to the previous one
            if survivalPoint.IsFillIn and index == 0:
                survivalPoint.Live = True
            elif survivalPoint.IsFillIn:
                previousDate = allDates[index - 1]
                previousPoint, _ = GetOrCreateSurvivalTimepoint(mouse, previousDate, experiment.StartDate)
                survivalPoint.Live = previousPoint.Live
    
    #back fill live from last live date
    for mouse in experiment.Mice:
        isLive = False
        for survivalTP in reversed(mouse.Survival):
            if survivalTP.Live == True:
                isLive = True
            survivalTP.Live = isLive
    
    #if mouse has explicit death date, set that date to dead even if measurements were collected
    for mouse in experiment.Mice:
        if mouse.DeathDate is not None:
            deathTimePoint, _ = GetOrCreateSurvivalTimepoint(mouse, mouse.DeathDate, experiment.StartDate)
            deathTimePoint.Live = False
                

def GetOrCreateSurvivalTimepoint(mouse, date, startDate):
    for tp in mouse.Survival:
        if tp.Date == date:
            return tp, False
    newTP = Classes.Survival(date, startDate)
    mouse.Survival.append(newTP)
    return newTP, True
                    
                        
    