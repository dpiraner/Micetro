# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 13:44:50 2022

@author: dpira
"""

#https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/
  
# import all components
# from the tkinter library
import tkinter as tk
  
# import filedialog module
from tkinter import filedialog
  
import pandas as pd

import numpy as np

import scipy as sp

import math

import matplotlib.pyplot as plt

import pickle 

import os

from functools import partial

import ExcelLoader
import ExcelPlotter
import DataSelector
import Auxil
import Classes

#create settings
settings = {
    'initDir': "",
    'errorType': "SEM",
    'metricType': "Formula",
    'tumorVolumeFormula': "(L x W^2) / 2"
    }
settingsfile = 'micetro.pk'   


def RunAnalysis():
    experiment = Classes.Experiment()
    groupAliases, deathDates = Auxil.LoadExperimentInfo(experiment, currentDir)
    measurements = ExcelLoader.LoadExcelFilesFromFolder(currentDir)
    Auxil.GetExperimentBoundDates(experiment, measurements) 
    experiment = ExcelLoader.ParseExcelMeasurements(measurements, experiment)
    Auxil.RemoveEmptyMice(experiment)
    Auxil.SetExplicitDeathDates(experiment, deathDates) #should come before aliasing group labels
    Auxil.AliasGroupLabels(experiment, groupAliases)
    
    print("Loaded experiment with " + str(len(experiment.Mice))  + " mice distributed among " + str(len(experiment.Groups)) + " groups in " + str(len(experiment.Cages)) + " cages.")
    print("First measurement: " + str(measurements[0].Date))
    print("Starting measurements from " + str(experiment.StartDate) + " (Chosen from parameter: " + str(experiment.StartFrom) + ")")
    
    DataSelector.ComputeTumorVolumes(experiment, settings['tumorVolumeFormula'])
    DataSelector.ComputeDeathDates(experiment)
    ExcelPlotter.PlotExperiment(experiment, settings)
    print("Analyses complete!")
    
def chooseDir(initDir):
    chosenDir = filedialog.askdirectory(initialdir=initDir)
    
    global currentDir 
    currentDir = chosenDir
    
    RunAnalysis()

#on-close save settings
def exit():
    try:
        settings['initDir'] = os.path.dirname(currentDir)
        with open(settingsfile, "wb") as f:
            pickle.dump(settings, f, pickle.HIGHEST_PROTOCOL)

        window.destroy()
    except ValueError as e:
        print("Invalid value:", e)

#on-open load settings
try:
    with open(settingsfile, 'rb') as f:
        try:
            settings = pickle.load(f)
        except: 
            pass
except:
    pass

# Create the root window
window = tk.Tk()

canvas1 = tk.Canvas(window, width = 450, height = 200,  relief = 'raised', bg='white')
canvas1.pack()
  
# Set window title
window.title('File Explorer')
  
window.wm_title('Micetro')

loadFromLastDir = partial(chooseDir, settings['initDir']) 
button_getFolder = tk.Button(window,
                        text = "Select Directory", fg='white', bg='black',
                        command = loadFromLastDir)  

canvas1.create_window(50, 80, window=button_getFolder)

# Let the window wait for any events
window.mainloop()