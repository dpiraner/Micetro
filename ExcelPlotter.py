# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 10:59:49 2022

@author: dpira
"""

import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
from datetime import datetime
import DataSelector
import math

def PlotExperiment(experiment, settings):
    outputName = "Micetro Output " + datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + '.xlsx'
    tumorLabels = DataSelector.GetTumorLabels(experiment)
    workbook = xlsxwriter.Workbook(outputName)

    debug = PlotTumors(experiment, workbook, settings['errorType'])
    
    workbook.close()
    return debug

def PlotTumors(experiment, workbook, errorMode):
        tumorLabels = DataSelector.GetTumorLabels(experiment)
        #iterate through tumors
        for tumorLabel in tumorLabels:
            #set up worksheet for current tumor name
            worksheet = workbook.add_worksheet(tumorLabel)
            sheetRow = 0
            sheetColumn = 0
            
            #get and plot tumor volumes
            rawMeasurements = DataSelector.GetTumorMeasurementsByGroup(experiment, tumorLabel)
            sheetRow, sheetColumn = WriteDataToSheet(rawMeasurements, worksheet, sheetRow, sheetColumn)
            
            #plot spider charts
            maxX = (experiment.EndDate - experiment.StartDate).days
            maxY = DataSelector.GetMaxTumorMeasurement(experiment, tumorLabel)
            PlotChartsFromRawData(workbook, worksheet, 0, 1, sheetRow - 1, 1, 2, sheetColumn - 1, GetCategoryLengths(experiment.Groups), GetGroupNames(experiment.Groups), 'scatter', "Day", "Tumor volume (mm3)", "Group ", maxX, maxY)
        
            #get and plot tumor averages
            averagesAndErrors = DataSelector.GetTumorAveragesByGroup(experiment, tumorLabel, errorMode)
            dbg = True
        
        return rawMeasurements


def WriteDataToSheet(data, worksheet, startRow, startColumn):
    
    xlRow = startRow
    xlColumn = startColumn
    columnMax = 0
    
    for line in data:
        xlColumn = startColumn
        for value in line:
            worksheet.write(xlRow, xlColumn, value)
            xlColumn += 1
            if xlColumn > columnMax:
                columnMax = xlColumn
        xlRow += 1
    return xlRow, columnMax

def GetCategoryLengths(mouseCollections):
    lengths = []
    for collection in mouseCollections:
        lengths.append(len(collection.Mice))
    return lengths

def GetGroupNames(groups):
    names = []
    for group in groups:
        names.append(str(group.Label))
    return names

def RoundOrdinateAxisMax(x):
    if x <= 1000:
        return int(math.ceil(x / 100.0)) * 100
    else:
        return int(math.ceil(x / 1000.0)) * 1000
        
def WriteAveragesAndErrorsByValue(workbook, worksheet, experiment, headerRow, startRow, startColumn, abscissaColumn, dataStartColumn, dataEndColumn, categoryLengths, categoryNames):
    xlRow = startRow
    xlColumn = startColumn
    rowMax = startRow
    colMax = startColumn
    
    

def PlotChartsFromRawData(workbook, worksheet, headerRow, dataStartRow, dataEndRow, abscissaColumn, dataStartColumn, dataEndColumn, categoryLengths, categoryNames, chartType, xName, yName, titlePrefix, maxX, maxY): # designed to be arbitrary between groups and cages. categoryLengths = number of mice in each group or cage
    
    currentColumn = dataStartColumn
    
    abscissaStart = [dataStartRow, abscissaColumn]
    abscissaEnd = [dataEndRow, abscissaColumn]
    
    for i in range(len(categoryNames)): #iterate through categories (groups or cages)
        categoryStartColumn = currentColumn
        #create new chart for new group or cage
        category = categoryNames[i]
        numSeries = categoryLengths[i]
        
        chartWidth = 63.8 * categoryLengths[i] # https://xlsxwriter.readthedocs.io/worksheet.html  The default width is 8.43 in the default font of Calibri 11
        
        chart = workbook.add_chart({
                'type': chartType, 
                'subtype': 'straight_with_markers'
                })
        
        chart.set_size({'width': chartWidth})
        
        FormatStandardChart(chart, titlePrefix + category, xName, yName, maxX, maxY)
        
        #add series for each mouse in group or cage
        for j in range(categoryLengths[i]):
            
            dataStart = [dataStartRow, currentColumn]
            dataEnd = [dataEndRow, currentColumn]
            
            chart.add_series({
                'categories': [worksheet.name] + abscissaStart + abscissaEnd,
                'values': [worksheet.name] + dataStart + dataEnd,
                'name': [worksheet.name] + [headerRow, currentColumn],
                'marker': {'type': 'circle'},
                'name_font': {'name': 'arial', 'size': 11}
            })
            currentColumn += 1
        
        #add chart to worksheet
        worksheet.insert_chart(dataEndRow + 1, categoryStartColumn, chart)
    return



def FormatStandardChart(chart, title, xName, yName, maxX, maxY):
    chart.set_title({
        'name': title,
        'name_font': {'name': 'arial', 'size': 14, 'bold': False}
        })
        
    chart.set_x_axis({
            'name': xName, 
            'name_font': {'name': 'arial', 'size': 11, 'bold': False}, 
            'num_font': {'name': 'arial', 'size': 11},
            'min': 0,
            'max': maxX
            })
    
    if maxY is not None:
        chart.set_y_axis({
            'name': yName, 
            'name_font': {'name': 'arial', 'size': 11, 'bold': False}, 
            'num_font': {'name': 'arial', 'size': 11},
            'major_gridlines': {'visible': False}, 
            'min': 0, 
            'max': RoundOrdinateAxisMax(maxY)
            })
    else:
        chart.set_y_axis({
            'name': yName, 
            'name_font': {'name': 'arial', 'size': 11, 'bold': False}, 
            'num_font': {'name': 'arial', 'size': 11},
            'major_gridlines': {'visible': False}, 
            'min': 0
            })
    return
        
        