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

#create settings
settings = {
    'initDir': ""
    }
settingsfile = 'settings.pk'   


def RunAnalysis():
    ExcelLoader.LoadExcelFilesFromFolder(currentDir)
    pass

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
                        text = "Load File", fg='white', bg='black',
                        command = loadFromLastDir)  

canvas1.create_window(50, 80, window=button_getFolder)

# Let the window wait for any events
window.mainloop()