# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 13:58:36 2022

@author: dpira
"""

import glob, os

def LoadExcelFilesFromFolder(currentDir):
    os.chdir(currentDir)
    for file in glob.glob("*.xlsx"):
        print(file)