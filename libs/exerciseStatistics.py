"""
Helper functions for visualizing exercise statistics.

Figures generated:

    1. One 3D bar chart for each set;
    2. Trend fit plots over days for first set & sum;
    3. Workout trend with current average.

Developed and tested with Python 3.8.

Yaguang Zhang, 2020/05/01
"""
# For loading data from a csv file.
import csv
# For date formatting.
import datetime
# For plotting.
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
# For setting font in the plot.
from pylab import mpl
from matplotlib.ticker import MaxNLocator

def loadStatisticsFromCsv(pathToCsvFile):
    """
    Load data from the input csv file.

    The data will be output in a list of dict, with each list element containing
    data from one row of the csv file.
    """
    with open(pathToCsvFile, mode='r') as csvFile:
        csvDictReader = csv.DictReader(csvFile)
        header = csvDictReader.fieldnames
        data = [row for row in csvDictReader]
        return (header, data)

def autoLabelBarChart(rects, ax, fontsize='large'):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        if height!=0:
            ax.text(rect.get_x() + rect.get_width()/2., 1.005*height,
                '%d' % int(height), weight='bold',
                ha='center', va='bottom', fontsize=fontsize)

# Color map to use (based on Matlab).
colorMap = (
    (0, 0.4470, 0.7410),
    (0.8500, 0.3250, 0.0980),
    (0.9290, 0.6940, 0.1250),
    (0.4940, 0.1840, 0.5560),
    (0.4660, 0.6740, 0.1880),
    (0.3010, 0.7450, 0.9330),
    (0.6350, 0.0780, 0.1840)
)

def getNumsOfRowsAndSets(header, data):
    totalNumOfRows = len(data)
    fieldsForSets  = [field for field in header
        if field.lower().startswith('set')]
    totalNumOfSets = len(fieldsForSets)
    return (totalNumOfRows, totalNumOfSets)

def constructTitleFromDate(data, idxRow):
    """
    Construct title string from date string (e.g. "4/1/2020").
    """
    dateStr = data[idxRow]['Date']
    (monthStr, dateStr, yearStr) = dateStr.split('/')
    return "第{}天（{}年{}月{}日）".format(
        idxRow+1, yearStr, monthStr, dateStr)

def plot3dBarChart(header, data,
    numOfRowsToShow=None, numOfSetsToShowForLastRow=None,
    fontInPlot='Microsoft YaHei', flagShowPlot=False, titleEndPad=0, zTickPad=0,
    figureSize=None, labelSize='large', titleSize='large', tickSize='large',
    labelPad3D = None, extraLabelPadZ=0,
    camView=(None, None), titleY=1, titleLoc='center'):
    """
    Plot the repetition number of each set of interest in a 3-dimensional bar
    chart plot. The plot will degenerate to a 2-dimensional one if there is only
    one day of data to show.
    """
    (totalNumOfRows, totalNumOfSets) = getNumsOfRowsAndSets(header, data)

    fieldsForSets  = [field for field in header
        if field.lower().startswith('set')]
    totalNumOfSets = len(fieldsForSets)

    # By default, plot all the data.
    if numOfRowsToShow is None:
        numOfRowsToShow = totalNumOfRows
    if numOfSetsToShowForLastRow is None:
        numOfSetsToShowForLastRow = totalNumOfSets

    # Set font to use in the plot.
    mpl.rcParams['font.sans-serif'] = [fontInPlot]
    # Just in case that the minus sign is not displayed correctly.
    mpl.rcParams['axes.unicode_minus'] = False

    # Set font size.
    mpl.rcParams.update({
        'axes.labelsize':  labelSize,
        'axes.titlesize':  titleSize,
        'xtick.labelsize': tickSize,
        'ytick.labelsize': tickSize
    })

    if figureSize is not None:
        mpl.rcParams.update({'figure.figsize': figureSize})

    # Parse date for file title construction.
    dateStrFormatted = constructTitleFromDate(
        data, numOfRowsToShow-1)

    # Store set values in a list, with each element being a list of all set
    # values for a day.
    histSetValues = [[0 for i in range(totalNumOfSets)]
        for i in range(numOfRowsToShow)]
    # Loop through all days/rows to show.
    for idxRow in range(numOfRowsToShow):
        if idxRow == numOfRowsToShow-1:
            curNumOfSetsToShowForLastRow = numOfSetsToShowForLastRow
        else:
            curNumOfSetsToShowForLastRow = totalNumOfSets

        # Obtain all data needed.
        for idxSet in range(curNumOfSetsToShowForLastRow):
            curSetValueStr = data[idxRow]['Set '+str(idxSet+1)]
            histSetValues[idxRow][idxSet] = int(curSetValueStr)

    # One plot per function call.
    fig = plt.figure()
    alpha = 0.8
    if numOfRowsToShow<1:
        raise ValueError("numOfRowsToShow should be at least 1!")
    elif numOfRowsToShow==1:
        # 2D plot.
        ax = fig.gca()
        color = colorMap[0]

        # Show at least 5 sets along the x axis.
        minNumSetsToShow = 5
        numOfSetsToShow = max(minNumSetsToShow, numOfSetsToShowForLastRow)

        xs = [v+1 for v in range(numOfSetsToShow)]
        ys = histSetValues[0][:numOfSetsToShow]
        barchart = ax.bar(xs, ys, color=color, alpha=alpha)
        autoLabelBarChart(barchart, ax, tickSize)

        # Better grid.
        ax.grid(True, which='major', color='b', linestyle='-' , alpha=0.5)
        ax.grid(True, which='minor', color='y', linestyle='--', alpha=0.5)
        ax.minorticks_on()
        # Labels.
        ax.set_xlabel('组数（组）')
        ax.set_ylabel('完成动作数（个）')
    else:
        # 3D plot.
        ax = fig.gca(projection='3d')
        # Labels.
        ax.set_xlabel('组数（组）', labelpad=labelPad3D)
        ax.set_ylabel('历史记录（天前）', labelpad=labelPad3D)
        if labelPad3D is not None:
            labelPadZ = labelPad3D + extraLabelPadZ
        else:
            labelPadZ = None
        ax.set_zlabel('完成动作数（个）', labelpad=labelPadZ)
        # Camera view angles.
        ax.view_init(elev=camView[0], azim=camView[1])

        # Plot data till the date and set of interest, with the plot for the
        # latest date show at front.
        for ir in range(numOfRowsToShow):
            color = colorMap[ir%len(colorMap)]
            xs = [v+1 for v in range(totalNumOfSets)]
            ys = histSetValues[ir]
            z = numOfRowsToShow-ir-1
            # We will gradually decrease alpha for history results.
            barAlphaMax = 1
            barAlphaMin = 0.3
            barAlphaStep = 0.1
            # The latest row is opaque.
            barAlpha = max(
                barAlphaMax-(numOfRowsToShow-1-ir)*barAlphaStep,
                barAlphaMin)
            ax.bar(xs, ys, zs=z, zdir='y',
                color=color, alpha=barAlpha)
            """
            # MatPlotLib has issues with 3D object visualization. Obstruction
            # may be rendered incorrectly (bar3d does not help).
            ```
            x = xs
            y = np.ones_like(ys)
            bottom = np.zeros_like(ys)
            width = depth = 1
            dz = ys
            ax.bar3d(x, y, bottom, width, depth, dz)
            ```
            """

        # Change Y range.
        plt.ylim(0, numOfRowsToShow-1)
        # We expect integer values.
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.zaxis.set_major_locator(MaxNLocator(integer=True))
        # Limit the number of y tick labels.
        maxNumOfYTickLs = 5
        curNumOfYTickLs = min(numOfRowsToShow, maxNumOfYTickLs)
        plt.locator_params(axis='y', nbins=curNumOfYTickLs)
        # Add values to the latest row.
        if ir==numOfRowsToShow-1:
            for x,y in zip(
                xs[:numOfSetsToShowForLastRow],
                ys[:numOfSetsToShowForLastRow]):
                ax.text(x, z, y, int(y), fontsize=tickSize, weight='bold',
                    horizontalalignment='center', verticalalignment='bottom')

    ax.set_title(dateStrFormatted+' '*titleEndPad, y=titleY, loc=titleLoc)
    plt.tight_layout()

    if numOfRowsToShow>1:
        # Move Z ticks away from the axis.
        fig.canvas.draw()
        labels = [item.get_text() for item in ax.get_zticklabels()]
        for idxL in range(len(labels)):
            labels[idxL] = ' '*zTickPad+labels[idxL]
        ax.set_zticklabels(labels)

    if flagShowPlot:
        plt.show()

    return (fig, ax)

def plotTrend(header, data, numOfRowsToShow=None,
    fontInPlot='Microsoft YaHei', flagShowPlot=False, lineWidth=5,
    figureSize=None, labelSize='large', titleSize='large', tickSize='large',
    flagEndDateDataInTitle=False):
    """
    Plot the trends over days of (1) the first-set repetition value and (2) the
    total repetition value of each day. If numOfRowsToShow is larger than
    available data, we will predict the values according to the history trends.
    """
    (totalNumOfRows, totalNumOfSets) = getNumsOfRowsAndSets(header, data)

    # By default, plot all the data.
    extraRowsToPredict = 0
    if numOfRowsToShow is None:
        numOfRowsToShow = totalNumOfRows
    elif numOfRowsToShow>totalNumOfRows:
        extraRowsToPredict = numOfRowsToShow-totalNumOfRows
        numOfRowsToShow = totalNumOfRows

    # Set font to use in the plot.
    mpl.rcParams['font.sans-serif'] = [fontInPlot]
    # Just in case that the minus sign is not displayed correctly.
    mpl.rcParams['axes.unicode_minus'] = False

    # Set font size.
    mpl.rcParams.update({
        'axes.labelsize':  labelSize,
        'axes.titlesize':  titleSize,
        'xtick.labelsize': tickSize,
        'ytick.labelsize': tickSize
    })

    if figureSize is not None:
        mpl.rcParams.update({'figure.figsize': figureSize})

    # Parse date for file title construction.
    dateStrFormatted = constructTitleFromDate(
        data, numOfRowsToShow-1)

    # Store history data in lists.
    firstSetReps = [0 for idx in range(numOfRowsToShow)]
    totalReps = [0 for idx in range(numOfRowsToShow)]
    # Loop through all days/rows to show.
    for idxRow in range(numOfRowsToShow):
        # Obtain all data needed.
        for idxSet in range(totalNumOfSets):
            curSetValue = int(data[idxRow]['Set '+str(idxSet+1)])
            totalReps[idxRow] += curSetValue
            if idxSet==0:
                firstSetReps[idxRow] = curSetValue

    xs = [r+1 for r in range(numOfRowsToShow)]
    # Plot the data we have.
    fig = plt.figure()
    ax = fig.gca()
    ax.plot(xs, totalReps, color=colorMap[0],
        linestyle='-', lineWidth=lineWidth)
    ax.plot(xs, firstSetReps, color=colorMap[1],
        linestyle='--', lineWidth=lineWidth)

    # We expect integer values.
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    # Limit the number of y tick labels.
    maxNumOfYTickLs = 5
    curNumOfYTickLs = min(numOfRowsToShow, maxNumOfYTickLs)
    plt.locator_params(axis='y', nbins=curNumOfYTickLs)

    # Plot the predictions.
    if extraRowsToPredict>0:
        (aFirstSet, bFirstSet) = np.polyfit(xs, firstSetReps, 1)
        (aTotal, bTotal) = np.polyfit(xs, totalReps, 1)

        xsPre = [1, numOfRowsToShow+extraRowsToPredict]
        firstSetRepsPre = [aFirstSet*x+bFirstSet for x in xsPre]
        totalRepsPre = [aTotal*x+bTotal for x in xsPre]

        ax.plot(xsPre, firstSetRepsPre, color=colorMap[1],
            linestyle=':', alpha=0.5, lineWidth=lineWidth)
        ax.plot(xsPre, totalRepsPre, color=colorMap[0],
            linestyle='-.', alpha=0.5, lineWidth=lineWidth)
        # Highlight the end predictions.
        ax.plot(xsPre[1], firstSetRepsPre[1], color=colorMap[1],
            Marker='o', alpha=0.5)
        ax.plot(xsPre[1], totalRepsPre[1], color=colorMap[1],
            Marker='s', alpha=0.5)
        ax.text(xsPre[1], firstSetRepsPre[1], str(int(firstSetRepsPre[1])),
            weight='bold', ha='right', va='center', fontsize=tickSize)
        ax.text(xsPre[1], totalRepsPre[1], str(int(totalRepsPre[1])),
            weight='bold', ha='right', va='center', fontsize=tickSize)

    ax.legend(["总计", "首组"], prop={'size': tickSize})
    if extraRowsToPredict>0:
        ax.set_title("第{}天".format(numOfRowsToShow+extraRowsToPredict))
    else:
        if flagEndDateDataInTitle:
            ax.set_title("第{}天".format(numOfRowsToShow) +
                " 总计{}个".format(totalReps[-1]))
        else:
            ax.set_title(dateStrFormatted)

    # Change X and Y ranges.
    plt.xlim(1, numOfRowsToShow+extraRowsToPredict)
    ax.set_ylim(bottom=0)
    # Better grid.
    ax.grid(True, which='major', color='b', linestyle='-' , alpha=0.5)
    ax.grid(True, which='minor', color='y', linestyle='--', alpha=0.5)
    ax.minorticks_on()
    # Labels.
    ax.set_xlabel('天数（天）')
    ax.set_ylabel('完成动作数（个）')

    plt.tight_layout()

    if flagShowPlot:
        plt.show()
    return (fig, ax)

def replaceLeadingZero(str, replacement=' '):
    newStr = str.lstrip('0')
    return replacement*(len(str)-len(newStr))+newStr

def getHumanReadableTimeStr(hStr, mStr, sStr):
    timeStr = ""
    if int(hStr)>0:
        timeStr += (replaceLeadingZero(hStr)+"小时")
    if int(mStr)>0:
        timeStr += (replaceLeadingZero(mStr)+"分")
    if int(sStr)>0:
        timeStr += (replaceLeadingZero(sStr)+"秒")
    return timeStr

def plotDailyTimeSpent(header, data, numOfRowsToShow=None,
    fontInPlot='Microsoft YaHei', flagShowPlot=False, lineWidth=5,
    figureSize=None, labelSize='large', titleSize='large', tickSize='large',
    flagEndDateDataInTitle=False):
    """
    Plot the trends over days of (1) the first-set repetition value and (2) the
    total repetition value of each day. If numOfRowsToShow is larger than
    available data, we will predict the values according to the history trends.
    """
    (totalNumOfRows, totalNumOfSets) = getNumsOfRowsAndSets(header, data)

    # Set font to use in the plot.
    mpl.rcParams['font.sans-serif'] = [fontInPlot]
    # Just in case that the minus sign is not displayed correctly.
    mpl.rcParams['axes.unicode_minus'] = False

    # Set font size.
    mpl.rcParams.update({
        'axes.labelsize':  labelSize,
        'axes.titlesize':  titleSize,
        'xtick.labelsize': tickSize,
        'ytick.labelsize': tickSize
    })

    if figureSize is not None:
        mpl.rcParams.update({'figure.figsize': figureSize})

    # Parse date for file title construction.
    dateStrFormatted = constructTitleFromDate(
        data, numOfRowsToShow-1)

    # Loop through rows of interest to get daily work out time records.
    workoutTimesInS = [0 for n in range(numOfRowsToShow)]
    for idxRow in range(numOfRowsToShow):
        workoutTimeStr = data[idxRow]['WorkoutTime']
        # Example time string: "0:04:10" for 0 hour 4 minutes 10 seconds.
        (hStr, mStr, sStr) = workoutTimeStr.split(':')
        workoutTimesInS[idxRow] = (int(hStr)*60+int(mStr))*60+int(sStr)

    # Average work out time.
    workoutTimeInSMean = sum(workoutTimesInS)/float(numOfRowsToShow)
    workoutTimeInMMean = workoutTimeInSMean/float(60)

    workoutTimeMeanStr = str(datetime.timedelta(seconds=int(workoutTimeInSMean)))
    (hStr, mStr, sStr) = workoutTimeMeanStr.split(':')
    workoutTimeMeanStr = "日均 "
    workoutTimeMeanStr += getHumanReadableTimeStr(hStr, mStr, sStr)

    xs = [r+1 for r in range(numOfRowsToShow)]
    # Plot.
    fig = plt.figure()
    ax = fig.gca()
    ax.plot(xs, [t/float(60) for t in workoutTimesInS], color=colorMap[0],
        linestyle='-', lineWidth=lineWidth)
    ax.plot([xs[0], xs[-1]], [workoutTimeInMMean]*2, color=colorMap[1],
        linestyle=':', lineWidth=lineWidth, alpha=0.75)
    ax.text(xs[-1], workoutTimeInMMean, workoutTimeMeanStr,
        weight='bold', ha='right', va='top', fontsize=tickSize)

    # We expect integer tick values.
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    # Limit the number of y tick labels.
    maxNumOfYTickLs = 5
    curNumOfYTickLs = min(numOfRowsToShow, maxNumOfYTickLs)
    plt.locator_params(axis='y', nbins=curNumOfYTickLs)

    ax.legend(["每日时长", "平均时长"], loc="lower right",
        prop={'size': tickSize})
    if flagEndDateDataInTitle:
        latestWorkoutTimeStr = str(datetime.timedelta(seconds=int(workoutTimesInS[-1])))
        (hStr, mStr, sStr) = latestWorkoutTimeStr.split(':')
        ax.set_title("第{}天 耗时".format(numOfRowsToShow) +
            getHumanReadableTimeStr(hStr, mStr, sStr))
    else:
        ax.set_title(dateStrFormatted)

    # Change X and Y ranges.
    plt.xlim(1, numOfRowsToShow)
    ax.set_ylim(bottom=0)
    # Better grid.
    ax.grid(True, which='major', color='b', linestyle='-' , alpha=0.5)
    ax.grid(True, which='minor', color='y', linestyle='--', alpha=0.5)
    ax.minorticks_on()
    # Labels.
    ax.set_xlabel('天数（天）')
    ax.set_ylabel('用时（分钟）')

    plt.tight_layout()

    if flagShowPlot:
        plt.show()
    return (fig, ax)

if __name__ == '__main__':
    # For testing
    import os
    pwd = os.path.dirname(__file__)
    pathToCsvFile = os.path.join(pwd, './../20200401_PullUps.csv')

    (header, data) = loadStatisticsFromCsv(pathToCsvFile)
    # Test 2D bar chart.
    plot3dBarChart(header, data, 1, 8, flagShowPlot=True)
    # Test 3D bar chart.
    plot3dBarChart(header, data, 5, 3, flagShowPlot=True)
    # Test trend plot with available data.
    plotTrend(header, data, numOfRowsToShow=5, flagShowPlot=True)
    # Test trend plot with prediction data.
    plotTrend(header, data, numOfRowsToShow=365, flagShowPlot=True)
    # Test workout time trend plot.
    plotDailyTimeSpent(header, data, numOfRowsToShow=25,
        flagEndDateDataInTitle=True, flagShowPlot=True)