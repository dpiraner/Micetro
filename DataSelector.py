# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 19:39:45 2022

@author: dpira
"""

import math
import Auxil
import statistics
from scipy import mean
from scipy.stats import sem

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
        ax1 = node.Ax1s1
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
        measurementRow = [timePoints[i], elapsed[i]]
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
        if timePointHasValues == True: #if any values were not None                
            rows.append(measurementRow + errorRow)
    return rows 
    
    