# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 14:11:23 2022

@author: dpira
"""

class Tumor:
    def __init__(self, label):
        self.Label = label
        self.TimePoints = []
        
class TumorTimePoint:
            def __init__(self, date, startDate):
                self.Date = date
                self.Elapsed = date - startDate
                self.Axis1 = None
                self.Axis2 = None
                self.Volume = None

class OtherMeasurement:
    def __init__(self, label):
        self.Label = label
        self.TimePoints = []
        
class OtherMeasurementTimePoint:
            def __init__(self, date, startDate, value):
                self.Date = date
                self.Elapsed = date - startDate
                self.Value = value
        
class Mouse:
    def __init__(self, label, cage, group):
        self.Label = label
        self.Tumors = []
        self.OtherMeasurements = []
        self.Cage = cage
        self.Group = group
        self.DeathDate = None
        
class Group:
    def __init__(self, label):
        self.Label = label
        self.Mice = []
        
class Cage:
    def __init__(self, number, ID, origID):
        self.Number = number
        self.ID = id
        self.OrigID = origID
        self.Mice = []
        
class ExcelSheet:
    def __init__(self, path, date):
        self.Path = path
        self.Date = date
        self.DataFrame = None
        
class Experiment:
    def __init__(self):
        self.Mice = []
        self.Groups = []
        self.Cages = []
        self.ChallengeDate = None
        self.TreatmentDate = None
        self.StartFrom = "treatment"
        self.StartDate = None