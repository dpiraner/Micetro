# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 15:52:12 2022

@author: dpira
"""

import Classes

def GetSuperHeaderNames(df):
    prelim = list(df.columns)
    output = []
    for entry in prelim:
        output.append(entry.split('.')[0])
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
