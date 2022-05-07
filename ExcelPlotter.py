# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 10:59:49 2022

@author: dpira
"""

import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell #https://xlsxwriter.readthedocs.io/working_with_cell_notation.html
from datetime import datetime
import DataSelector
import Auxil
import math

def PlotExperiment(experiment, settings):
    outputName = "Micetro Output " + datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + '.xlsx'
    tumorLabels = DataSelector.GetTumorLabels(experiment)
    workbook = xlsxwriter.Workbook(outputName)

    debug = PlotTumors(experiment, workbook, settings['errorType'])
    
    workbook.close()
    return debug

def PlotTumors(experiment, workbook, errorMode):  
    
    #Preprocessing
    groupNames = GetGroupNames(experiment.Groups)
    numGroups = len(groupNames)
    micePerGroup = GetCategoryLengths(experiment.Groups)
    
    #normalize data 
    normalizedExperiment = DataSelector.AsPercentageOfFirst(experiment)
    
    #plot tumors
    tumorLabels = DataSelector.GetTumorLabels(experiment)
    #iterate through tumors
    for tumorLabel in tumorLabels:
        #set up worksheet for current tumor name
        worksheet = workbook.add_worksheet(tumorLabel)
        sheetRow = 0
        sheetColumn = 0
        
        #get and record tumor volumes
        rawMeasurements = DataSelector.GetTumorMeasurementsByGroup(experiment, tumorLabel)
        sheetRow, sheetColumn = WriteDataToSheet(rawMeasurements, worksheet, sheetRow, sheetColumn)
        
        #plot spider charts
        maxX = (experiment.EndDate - experiment.StartDate).days
        maxY = DataSelector.GetMaxTumorMeasurement(experiment, tumorLabel)
        PlotChartsFromRawData(workbook, worksheet, 0, 1, sheetRow - 1, 1, 2, sheetColumn - 1, micePerGroup, groupNames, 'scatter', "Day", "Tumor volume (mm3)", "Group ", 0, maxX, 0, maxY)
    
        #skip some cells to make room for charts
        sheetRow += 16
    
        #get and plot tumor averages
        averagesHeaderRowIndex = sheetRow
        averagesAndErrors = DataSelector.GetTumorAveragesByGroup(experiment, tumorLabel, errorMode)
        sheetRow, sheetColumn = WriteDataToSheet(averagesAndErrors, worksheet, sheetRow, 0)
        
        #plot averages with error bars
        PlotAveragesAndErrors(workbook, worksheet, averagesHeaderRowIndex, averagesHeaderRowIndex + 1, sheetRow - 1, 1, 2, numGroups + 1, groupNames, 'scatter', 'Day', 'Tumor volume (mm3)', 'Tumor Growth', 0, maxX, 0, maxY, 0)
        
        
        
        
        #plot normalized spider plots
        sheetRow += round(numGroups * 2.2)
        normalizedHeaderIndex = sheetRow
        sheetColumn = 0
        
        #get and record tumor volumes
        rawMeasurements = DataSelector.GetTumorMeasurementsByGroup(normalizedExperiment, tumorLabel)
        sheetRow, sheetColumn = WriteDataToSheet(rawMeasurements, worksheet, sheetRow, sheetColumn)
        
        #plot spider charts
        maxX = (experiment.EndDate - experiment.StartDate).days
        maxY = DataSelector.GetMaxTumorMeasurement(normalizedExperiment, tumorLabel)
        PlotChartsFromRawData(workbook, worksheet, normalizedHeaderIndex, normalizedHeaderIndex + 1, sheetRow - 1, 1, 2, sheetColumn - 1, micePerGroup, groupNames, 'scatter', "Day", "% Tumor Growth", "Group ", 0, maxX, 0, maxY)

        #skip some cells to make room for charts
        sheetRow += 16
    
        #get and plot tumor averages
        averagesHeaderRowIndex = sheetRow
        averagesAndErrors = DataSelector.GetTumorAveragesByGroup(normalizedExperiment, tumorLabel, errorMode)
        sheetRow, sheetColumn = WriteDataToSheet(averagesAndErrors, worksheet, sheetRow, 0)
        
        #plot averages with error bars
        PlotAveragesAndErrors(workbook, worksheet, averagesHeaderRowIndex, averagesHeaderRowIndex + 1, sheetRow - 1, 1, 2, numGroups + 1, groupNames, 'scatter', 'Day', '% Tumor Growth', '% Tumor Growth', 0, maxX, 0, maxY, 0)
        
    #plot other data
    otherDataLabels = DataSelector.GetOtherDataLabels(experiment)
    #iterate through other measurements
    for dataLabel in otherDataLabels:
        #set up worksheet for current data set
        worksheet = workbook.add_worksheet(dataLabel)
        sheetRow = 0
        sheetColumn = 0
        
        #get and record data
        rawMeasurements = DataSelector.GetDataMeasurementsByGroup(experiment, dataLabel)
        sheetRow, sheetColumn = WriteDataToSheet(rawMeasurements, worksheet, sheetRow, sheetColumn)
        
        #plot spider charts
        maxX = (experiment.EndDate - experiment.StartDate).days
        minY, maxY = DataSelector.GetDataBounds(experiment, dataLabel)
        minY = RoundOrdinateAxisMin(minY)
        PlotChartsFromRawData(workbook, worksheet, 0, 1, sheetRow - 1, 1, 2, sheetColumn - 1, micePerGroup, groupNames, 'scatter', "Day", dataLabel, "Group ", 0, maxX, minY, maxY)
    
        #skip some cells to make room for charts
        sheetRow += 16
    
        #get and plot tumor averages
        averagesHeaderRowIndex = sheetRow
        averagesAndErrors = DataSelector.GetDataSetAveragesByGroup(experiment, dataLabel, errorMode)
        sheetRow, sheetColumn = WriteDataToSheet(averagesAndErrors, worksheet, sheetRow, 0)
        
        #plot averages with error bars
        PlotAveragesAndErrors(workbook, worksheet, averagesHeaderRowIndex, averagesHeaderRowIndex + 1, sheetRow - 1, 1, 2, numGroups + 1, groupNames, 'scatter', 'Day', dataLabel, dataLabel, 0, maxX, 0, maxY, 0)
        
        
        
        
        
        #plot normalized spider plots
        sheetRow += round(numGroups * 2.2)
        normalizedHeaderIndex = sheetRow
        sheetColumn = 0
        
        #get and record data
        rawMeasurements = DataSelector.GetDataMeasurementsByGroup(normalizedExperiment, dataLabel)
        sheetRow, sheetColumn = WriteDataToSheet(rawMeasurements, worksheet, sheetRow, sheetColumn)
        
        #plot spider charts
        maxX = (experiment.EndDate - experiment.StartDate).days
        minY, maxY = DataSelector.GetDataBounds(normalizedExperiment, dataLabel)
        minY = RoundOrdinateAxisMin(minY)
        PlotChartsFromRawData(workbook, worksheet, normalizedHeaderIndex, normalizedHeaderIndex + 1, sheetRow - 1, 1, 2, sheetColumn - 1, micePerGroup, groupNames, 'scatter', "Day", dataLabel + " (% Change)", "Group ", 0, maxX, minY, maxY)
    
        #skip some cells to make room for charts
        sheetRow += 16
    
        #get and plot tumor averages
        averagesHeaderRowIndex = sheetRow
        averagesAndErrors = DataSelector.GetDataSetAveragesByGroup(normalizedExperiment, dataLabel, errorMode)
        sheetRow, sheetColumn = WriteDataToSheet(averagesAndErrors, worksheet, sheetRow, 0)
        
        #plot averages with error bars
        PlotAveragesAndErrors(workbook, worksheet, averagesHeaderRowIndex, averagesHeaderRowIndex + 1, sheetRow - 1, 1, 2, numGroups + 1, groupNames, 'scatter', 'Day', dataLabel + " (% Change)", dataLabel + " (% Change)", 0, maxX, minY, maxY, 0)
        
        
    return rawMeasurements

def WriteDataToSheet(data, worksheet, startRow, startColumn):
    
    xlRow = startRow
    xlColumn = startColumn
    columnMax = 0
    
    for line in data:
        xlColumn = startColumn
        for value in line:
            if Auxil.IsNumeric(value) and math.isnan(value):
                value = None
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


#def RoundOrdinateAxisMax(x):
#    if x <= 100:
#        return int(math.ceil(x / 10.0)) * 10
#    elif x <= 1000:
#        return int(math.ceil(x / 100.0)) * 100
#    else:
#        return int(math.ceil(x / 1000.0)) * 1000
    
def RoundOrdinateAxisMax(x):
    i = 0
    while True:
        ceilDecade = math.pow(10, i)
        if x < ceilDecade:
            ceilDecade = math.pow(10, i - 1)
            return int(math.ceil(x / ceilDecade)) * ceilDecade
        i += 1

def RoundOrdinateAxisMin(x):
    i = 1
    scalar = 1
    if x < 0:
        scalar = -1
        x = abs(x)
    
    while True:
        floorDecade = math.pow(10, i)
        if x > floorDecade:
            if i == 1 and scalar == 1: 
                return 0
            elif i == 1 and scalar == -1:
                return -1 * RoundOrdinateAxisMax(x) 
            else:                
                floorDecade = math.pow(10, i - 1)
                return int(math.floor(x / floorDecade)) * floorDecade * scalar
        i += 1    
        
def PlotAveragesAndErrors(workbook, worksheet, headerRow, dataStartRow, dataEndRow, abscissaColumn, dataStartColumn, dataEndColumn, categoryNames, chartType, xName, yName, title, minX, maxX, minY, maxY, gapColumnsBeforeErrors):
    currentColumn = dataStartColumn
    currentErrorColumn = dataEndColumn + 1 + gapColumnsBeforeErrors
    abscissaStart = [dataStartRow, abscissaColumn]
    abscissaEnd = [dataEndRow, abscissaColumn]
    
    chart = workbook.add_chart({
            'type': chartType, 
            'subtype': 'straight_with_markers'
            })
    FormatStandardChart(chart, title, xName, yName, minX, maxX, minY, maxY)
    chartWidth =  63.8 * len(categoryNames)
    chartHeight = chartWidth / 6 * 4
    chart.set_size({'width':chartWidth, 'height': chartHeight})
    
    #add series for each mouse in group or cage
    for name in categoryNames:
        dataStart = [dataStartRow, currentColumn]
        dataEnd = [dataEndRow, currentColumn]
        errorStart = [dataStartRow, currentErrorColumn]
        errorEnd = [dataEndRow, currentErrorColumn]
    
        errorStartStr = xl_rowcol_to_cell(dataStartRow, currentErrorColumn, row_abs=True, col_abs=True)
        errorEndStr = xl_rowcol_to_cell(dataEndRow, currentErrorColumn, row_abs=True, col_abs=True)
        errorLocStr = "='" + worksheet.name + "'!" + errorStartStr  + ':' + errorEndStr
    
        chart.add_series({
            'categories': [worksheet.name] + abscissaStart + abscissaEnd,
            'values': [worksheet.name] + dataStart + dataEnd,
            'name': [worksheet.name] + [headerRow, currentColumn],
            'marker': {'type': 'circle'},
            'name_font': {'name': 'arial', 'size': 11},
            'y_error_bars': {
                'type': 'custom',
                'plus_values': errorLocStr,
                'minus_values': errorLocStr
                }
        })
        currentColumn += 1
        currentErrorColumn += 1
    
    #add chart to worksheet
    worksheet.insert_chart(dataEndRow + 1, abscissaColumn + 1, chart)

def PlotChartsFromRawData(workbook, worksheet, headerRow, dataStartRow, dataEndRow, abscissaColumn, dataStartColumn, dataEndColumn, categoryLengths, categoryNames, chartType, xName, yName, titlePrefix, minX, maxX, minY, maxY): # designed to be arbitrary between groups and cages. categoryLengths = number of mice in each group or cage
    
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
        
        FormatStandardChart(chart, titlePrefix + category, xName, yName, minX, maxX, minY, maxY)
        
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



def FormatStandardChart(chart, title, xName, yName, minX, maxX, minY, maxY):
    chart.set_title({
        'name': title,
        'name_font': {'name': 'arial', 'size': 14, 'bold': False}
        })
        
    chart.set_x_axis({
            'name': xName, 
            'name_font': {'name': 'arial', 'size': 11, 'bold': False}, 
            'num_font': {'name': 'arial', 'size': 11},
            'min': minX,
            'max': maxX
            })
    
    if maxY is not None:
        chart.set_y_axis({
            'name': yName, 
            'name_font': {'name': 'arial', 'size': 11, 'bold': False}, 
            'num_font': {'name': 'arial', 'size': 11},
            'major_gridlines': {'visible': False}, 
            'min': minY, 
            'max': RoundOrdinateAxisMax(maxY)
            })
    else:
        chart.set_y_axis({
            'name': yName, 
            'name_font': {'name': 'arial', 'size': 11, 'bold': False}, 
            'num_font': {'name': 'arial', 'size': 11},
            'major_gridlines': {'visible': False}, 
            'min': minY
            })
    return
        
        