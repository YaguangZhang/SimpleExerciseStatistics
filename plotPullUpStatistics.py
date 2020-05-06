"""
=======================================
Generate figures for pull up statistics
=======================================
Figures generated:

    1. One 3D bar chart for each day;
    2. Trend fit plots for first set & sum.

Developed and tested with Python 3.8.

Yaguang Zhang, 2020/04/29
"""
import os
import libs.exerciseStatistics as es
import matplotlib.pyplot as plt
# For setting font in the plot.
from pylab import mpl

pwd = os.path.dirname(__file__)
pathToCsvFile = os.path.join(pwd, './20200401_PullUps.csv')

(header, data) = es.loadStatisticsFromCsv(pathToCsvFile)
totalNumOfRows = len(data)
fieldsForSets  = [field for field in header
    if field.lower().startswith('set')]
totalNumOfSets = len(fieldsForSets)

# Set font size.
labelSize = 30
titleSize = 40
tickSize  = 30

# Set figure size.
figureSize = (9,16)
figureSizeWide = (16,9)
figureSizeSquare = (9,8)

# Set line width in the trend plot.
lineWidth = 5
lineWidthPre = 3

# Output folder.
outputFolderName = 'Output'
try:
    outputDir = os.path.join(pwd, outputFolderName)
    os.mkdir(outputDir)
except Exception:
    pass

# Loop through all days and all sets for the bar chart.
for idxRow in range(totalNumOfRows):
    for idxSet in range(totalNumOfSets):
        if idxRow==0:
            (fig, _) = es.plot3dBarChart(header, data, idxRow+1, idxSet+1,
                labelSize=labelSize, titleSize=titleSize, tickSize=tickSize,
                figureSize=figureSize, flagShowPlot=False)
        else:
            (fig, _) = es.plot3dBarChart(header, data, idxRow+1, idxSet+1,
                labelSize=labelSize, titleSize=titleSize, tickSize=tickSize,
                figureSize=figureSize, labelPad3D=30, extraLabelPadZ = 10,
                titleY=0.9, titleLoc='right', titleEndPad=5, zTickPad=3,
                camView=(10, -60), flagShowPlot=False)
        fig.savefig(
            os.path.join(outputDir,
            'bar_day_'+str(idxRow+1)+'_set_'+str(idxSet+1)+'.png'))
        plt.close(fig)

# Loop through (1) all days for the trend plots and (2) future days for the
# prediction trend plots.
for idxRow in range(1, 365):
    if idxRow<totalNumOfRows:
        lw = lineWidth
    else:
        lw = lineWidthPre
    (fig, _) = es.plotTrend(header, data,  idxRow+1,
        figureSize=figureSize, lineWidth=lw, labelSize=labelSize,
        titleSize=titleSize, tickSize=tickSize, flagShowPlot=False)
    fig.savefig(
        os.path.join(outputDir,
        'trend_day_'+str(idxRow+1)+'.png'))
    plt.close(fig)

# Loop through all days for square trend plots.
for idxRow in range(1, totalNumOfRows):
    (fig, _) = es.plotTrend(header, data,  idxRow+1,
        figureSize=figureSizeSquare, lineWidth=lineWidth, labelSize=labelSize,
        titleSize=titleSize, tickSize=tickSize, flagShowPlot=False,
        flagEndDateDataInTitle=True)
    fig.savefig(
        os.path.join(outputDir,
        'trend_square_day_'+str(idxRow+1)+'.png'))
    plt.close(fig)

    (fig, _) = es.plotDailyTimeSpent(header, data,  idxRow+1,
        figureSize=figureSizeSquare, lineWidth=lineWidth, labelSize=labelSize,
        titleSize=titleSize, tickSize=tickSize, flagShowPlot=False,
        flagEndDateDataInTitle=True)
    fig.savefig(
        os.path.join(outputDir,
        'time_square_day_'+str(idxRow+1)+'.png'))
    plt.close(fig)

# Loop through future days for wider prediction trend plots.
for idxRow in range(totalNumOfRows, 365):
    if idxRow<totalNumOfRows:
        lw = lineWidth
    else:
        lw = lineWidthPre
    (fig, _) = es.plotTrend(header, data,  idxRow+1,
        figureSize=figureSizeWide, lineWidth=lw, labelSize=labelSize,
        titleSize=titleSize, tickSize=tickSize, flagShowPlot=False)
    fig.savefig(
        os.path.join(outputDir,
        'trend_wide_day_'+str(idxRow+1)+'.png'))
    plt.close(fig)

# Wide version for the data available.
for idxRow in range(totalNumOfRows):
    if idxRow<totalNumOfRows:
        lw = lineWidth
    else:
        lw = lineWidthPre
    (fig, _) = es.plotTrend(header, data,  idxRow+1,
        figureSize=figureSizeWide, lineWidth=lw, labelSize=labelSize,
        titleSize=titleSize, tickSize=tickSize, flagShowPlot=False)
    fig.savefig(
        os.path.join(outputDir,
        'trend_available_wide_day_'+str(idxRow+1)+'.png'))
    plt.close(fig)