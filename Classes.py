# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 14:11:23 2022

@author: dpira
"""

class Tumor:
    def __init__(self):
        self.Axis1 = ''
        self.Axis2 = ''
        
class Attribute:
    def __init__(self):
        self.Name = ''
        self.Value = ''
        
class TimePoint:
    def __init__(self):
        self.Date = ''
        self.Elapsed = 0
        self.Tumor = None
        self.Attributes = []

class Mouse:
    def __init__(self):
        self.Label = ''
        self.Timepoints = []
        
class Group:
    def __init__(self):
        self.Label = ''
        self.Mice = []
        
class Cage:
    def __init__(self):
        self.ID = ''
        self.Mice = []
        
class ExcelSheet:
    def __init__(self, path, date):
        self.Path = path
        self.Date = date
        self.DataFrame = None