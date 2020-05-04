"""
Helper functions for visualizing exercise statistics.

Figures generated:

    1. One 3D bar chart for each set;
    2. Trend fit plots over days for first set & sum.

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
    totalNumOfRows = len(data)

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
    dateOfInterestStr = data[numOfRowsToShow-1]['Date']
    (monthStr, dateStr, yearStr) = dateOfInterestStr.split('/')
    dateStrFormatted = "第{}天（{}年{}月{}日）".format(
        numOfRowsToShow, yearStr, monthStr, dateStr)

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
