# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 19:39:45 2022

@author: dpira
"""

import math
import Auxil

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

def GetTumorMeasurement(ax1, ax2, tumorVolumeFormula):
    
    if not Auxil.IsNumeric(ax1) or not Auxil.IsNumeric(ax2) or math.isnan(ax1) or math.isnan(ax2):
        return None
    
    vol = 0
    if tumorVolumeFormula == "(L x W^2) / 2":
        L = max(ax1, ax2)
        W = min(ax1, ax2)
        vol = math.pow(W, 2) * L * 0.5
    return vol

def ComputeTumorVolumes(experiment, tumorVolumeFormula):
    for mouse in experiment.Mice:
        for tumor in mouse.Tumors:
            for timePoint in tumor.TimePoints:
                timePoint.Volume = GetTumorMeasurement(timePoint.Axis1, timePoint.Axis2, tumorVolumeFormula)

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
                        