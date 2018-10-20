# Functions for machine learning pattern recognition

import yaml
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np
import time
from functools import reduce


# Converts date to correct format for np.loadtxt on __main__

def convert_date(date_bytes):
    return mdates.strpdate2num('%m/%d/%Y %H:%M')(date_bytes.decode('ascii'))

# Returns percent change between two numbers

def percentChange(startPoint, currentPoint):

    try:
        x = ((float(currentPoint)-startPoint)/abs(startPoint))*100.00
        if x == 0.0:
            return 0.0000001
        else:
            return x
    except:
        return 0.0000001

# Stores all patterns in the data inside global array patternAr

def patternStorage(bid, ask, avgLine):
    
    patStartTime = time.time()

    x = len(avgLine) - 30
    y = 31
    n = 0

    while y < x:
        
        pattern = []
        
        for i in range(0,30):
            pattern.append(percentChange(avgLine[y-30], avgLine[y-(29-i)]))
 

        outcomeRange = avgLine[y+20:y+30]
        currentPoint = avgLine[y]

        try:
            avgOutcome = (reduce(lambda x,y: x+y, outcomeRange) / len(outcomeRange))
        
        except(Exception, e):
            print(str(e))
            avgOutcome = 0

        futureOutcome = percentChange(currentPoint, avgOutcome)

        
        patternAr.append(pattern)
        performanceAr.append(futureOutcome)

        y += 1
        n += 1

 

    patEndTime = time.time()

    print(len(patternAr))
    print(len(performanceAr))
    print("Time for pattern storage:", patEndTime-patStartTime, "seconds")

# Stores current pattern into patForRec array

def currentPattern(avgLine):

    startTime = time.time()

    for i in range (0,30):
        patForRec.append(percentChange(avgLine[-31], avgLine[-30+i]))

    endTime = time.time()

    print("Time for current pattern storage:", endTime-startTime, "seconds")
    print(patForRec)

def patternRecognition():

    startTime = time.time()
    patFound = 0
    plotPatAr = []
    predictedOutcomesAr = []

    for pattern in patternAr: 

        sim = []
        totalSim = 0

        for i in range(0,30):
            sim.append(100.00 - abs(percentChange(pattern[i], patForRec[i])))
            totalSim += sim[i]


        totalSim = totalSim/30.00

        if totalSim > 75:

            patternI = patternAr.index(pattern)
            
            patFound = 1


            xp = [i for i in range (1, 31)]
            
            plotPatAr.append(pattern)
    
    predArray = []

    if patFound == 1:

        #fig = plt.figure(figsize=(10,6))

        for eachPatt in plotPatAr:
            futurePoints = patternAr.index(eachPatt)

            if performanceAr[futurePoints] > patForRec[29]:
                pcolor = '#24bc00'
                predArray.append(1.000)
            else:
                pcolor = '#d40000'
                predArray.append(-1.000)

            predictedOutcomesAr.append(performanceAr[futurePoints])

            #plt.plot(xp, eachPatt)

            #plt.scatter(35, performanceAr[futurePoints], c=pcolor, alpha=.3)
        
        realOutcomeRange = allData[toWhat+20:toWhat+30]
        realAvgOutcome = reduce(lambda x, y: x+y, realOutcomeRange) / len(realOutcomeRange)
        realMovement = percentChange(allData[toWhat], realAvgOutcome) 
        predictedAvgOutcome = reduce(lambda x, y: x+y, predictedOutcomesAr) / len(predictedOutcomesAr)

        print(predArray)
        predictionAverage = reduce(lambda x, y: x+y, predArray) / len(predArray)

        print(predictionAverage)

        if predictionAverage < 0:
            print("Drop predicted")
            print(patForRec[29])
            print(realMovement)

            if realMovement < patForRec[29]:
                accuracyArray.append(100)
            else:
                accuracyArray.append(0)

        if predictionAverage > 0:
            print("Rise predicted")
            print(patForRec[29])
            print(realMovement)

            if realMovement > patForRec[29]:
                accuracyArray.append(100)
            else:
                accuracyArray.append(0)

        print(accuracyArray)

    endTime = time.time()

    print("Time for pattern Recognition:", endTime-startTime, "seconds")

        #plt.scatter(40, realMovement, c='#54fff7', s=25)
        #plt.scatter(40, predictedAvgOutcome, c='b', s=25)
        #plt.plot(xp, patForRec, '#54fff7', linewidth = 3)
        #plt.grid(True)
        #plt.title("Pattern Recognition")
        #plt.show()

# Creates a graph from data date, bid price, and ask price

def graphRawFX(conf, date, bid, ask):

    #midLine = midLineF(bid, ask)
    fig = plt.figure(figsize=(10,7))
    ax1 = plt.subplot2grid((40,40), (0,0), rowspan=40, colspan=40)

    ax1.plot(date, bid)
    ax1.plot(date, ask)
    #ax1.plot(date, midLine)
    
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
        
    ax1_2 = ax1.twinx()
    ax1_2.fill_between(date, 0, (ask-bid), facecolor='g', alpha=.3)
    
    plt.subplots_adjust(bottom=.23)

    plt.grid(True)
    plt.show()
    

startTime = time.time()

# Load conf file

stream = open("conf.yaml", "r")
conf = yaml.load(stream)

# Load data

date, bid, ask = np.loadtxt(conf['data_path'], unpack=True, 
                            delimiter=',', 
                            converters={0: convert_date}) 

dataLength = int(bid.shape[0])
print("Data length is", dataLength)
toWhat = 15000
allData = ((bid+ask)/2)
patternAr = []
performanceAr = []

accuracyArray = [100]
samps = 0
avgLine = allData[:toWhat]
patternStorage(bid, ask, avgLine)

while toWhat < dataLength:

    avgLine = allData[:toWhat]

    #Define arrays to store patterns and results
    #patternAr = []
    #performanceAr = []
    patForRec = [] 

    #graphRawFX(conf, date, bid, ask)
    #patternStorage(bid, ask, avgLine)
    currentPattern(avgLine)
    patternRecognition()

    samps += 1

    toWhat += 1
    accuracyAverage = reduce(lambda x, y: x+y, accuracyArray) / len(accuracyArray)
    print("Backtested Accuracy is", str(accuracyAverage)+"% after", samps, "samples")

    endTime = time.time()
    print("Time from start to end of loop:", endTime-startTime, "seconds")


    


