import urllib2
import schedule
import time
import csv

from bs4 import BeautifulSoup

#Counts the loops which have occurred
count = 1

#Address for reference. We attach a page number to this
rawAddress = "https://rocket-league.com/trading?filterItem=0&\
filterCertification=0&filterPaint=0&filterPlatform=3&filterSearchType=1"

#Stores time series data for have, want, and ratios
haveTimeSeries = []
wantTimeSeries = []
wantHaveTimeSeries = []

#Function for sampling values from the forums
def takeSample():

    global count
    global haveTimeSeries
    global wantTimeSeries
    global wantHaveTimeSeries

    haveFreq = []
    wantFreq = []

    wantHaveRatio = []

    count = count+1

#This loop starts at page 20 and works backwards
#If you wanna apply filters or anything, do it in this link
    for pageNumber in reversed(xrange(1, 20)):
        webAddress = urllib2.Request("https://rocket-league.com/trading?filterItem=0&filterCertification=0&filterPaint=0&filterPlatform=3&filterSearchType=1&p="+str(pageNumber), headers={'User-Agent' : "Magic Browser"})

        page = urllib2.urlopen(webAddress)

        soup = BeautifulSoup(page, "html.parser")
#Finds the trade container
        for tradeNum in soup.find_all(class_="rlg-trade-display-container"):
#Looks through offered items
            for trade in tradeNum.find_all(id="rlg-youritems"):
#Finds all the listed items, scrapes the image alt text, color, and quantity
                for listing in trade.find_all('a'):
                    nextItem = ''
                    for item in listing.find_all('img'):
                        nextItem =  item.get('alt')
                        for color in listing.find_all(class_='rlg-trade-display-item-paint'):
                            nextItem = nextItem + " " + color.get('data-name')
                    isNew=1
                    for i in xrange(0,len(haveFreq)):
                        if(nextItem == haveFreq[i][0]):
                            haveFreq[i][1]=haveFreq[i][1]+1
                            isNew=0
                    if(isNew==1):
                        haveFreq.append([nextItem,1])
                    for quantity in listing.find_all("div", "rlg-trade-display-item__amount"):
                        for i in xrange(0,len(haveFreq)):
                                if(nextItem == haveFreq[i][0]):
                                    haveFreq[i][1]=haveFreq[i][1]+int(quantity.get_text().lstrip())-1
#Looks through wanted items
            for trade in tradeNum.find_all(id="rlg-theiritems"):
                for listing in trade.find_all('a'):
                    nextItem = ''
                    for item in listing.find_all('img'):
                        nextItem = item.get('alt')
                        for color in listing.find_all('data_name:'):
                            nextItem = nextItem + " " + color.get('data-name')
                    isNew=1
                    for i in xrange(0,len(wantFreq)):
                        if(nextItem == wantFreq[i][0]):
                            wantFreq[i][1]=wantFreq[i][1]+1
                            isNew=0
                    if(isNew==1):
                        wantFreq.append([nextItem,1])
                for quantity in listing.find_all("div", "rlg-trade-display-item__amount"):
                    for i in xrange(0,len(wantFreq)):
                        if(nextItem == wantFreq[i][0]):
                            wantFreq[i][1]=wantFreq[i][1]+int(quantity.get_text().lstrip())-1

#Calculates want/have ratio, adds missing titles to wantFreq
    for i in xrange(len(haveFreq)):
        foundMatch = 0
        for j in xrange(len(wantFreq)):
            if(haveFreq[i][0]==wantFreq[j][0]):
                wantHaveRatio.append([wantFreq[j][0], float(wantFreq[j][1])/float(haveFreq[i][1])])
                foundMatch = 1
        if (foundMatch == 0):
            wantFreq.append([haveFreq[i][0],0])
            wantHaveRatio.append([haveFreq[i][0],0])

#Adds missing titles to wantFreq, wantHaveRatio
    for i in xrange(len(wantFreq)):
        foundMatch = 0
        for j in xrange(len(haveFreq)):
            if(haveFreq[j][0]==wantFreq[i][0]):
                foundMatch = 1
        if (foundMatch == 0):
            haveFreq.append([wantFreq[i][0],0])
            wantHaveRatio.append([wantFreq[i][0],0])

#Updates the time series
    isNew = 1
    for i in xrange(0, len(haveFreq)):
            for item in haveTimeSeries:
                if(haveFreq[i][0]==item[0]):
                    isNew=0
                    item.append(haveFreq[i][1])
                    break
            if(isNew==1):
                haveTimeSeries.append([haveFreq[i][0]])
                haveTimeSeries[len(haveTimeSeries)-1].append(haveFreq[i][1])
    for i in xrange(0, len(haveTimeSeries)):
        if(len(haveTimeSeries[i])<count):
            haveTimeSeries[i].append(0)
#Updates the time series
    isNew = 1
    for i in xrange(0, len(wantFreq)):
            for item in wantTimeSeries:
                if(wantFreq[i][0]==item[0]):
                    isNew=0
                    item.append(wantFreq[i][1])
                    break
            if(isNew==1):
                wantTimeSeries.append([wantFreq[i][0]])
                wantTimeSeries[len(wantTimeSeries)-1].append(wantFreq[i][1])
    for i in xrange(0, len(wantTimeSeries)):
        if(len(wantTimeSeries[i])<count):
            wantTimeSeries[i].append(0)
#Updates the time series
    isNew = 1
    for i in xrange(0, len(wantHaveRatio)):
            for item in wantHaveTimeSeries:
                if(wantHaveRatio[i][0]==item[0]):
                    isNew=0
                    item.append(wantHaveRatio[i][1])
                    break
            if(isNew==1):
                wantHaveTimeSeries.append([wantHaveRatio[i][0]])
                wantHaveTimeSeries[len(wantHaveTimeSeries)-1].append(wantHaveRatio[i][1])
    for i in xrange(0, len(wantHaveTimeSeries)):
        if(len(wantHaveTimeSeries[i])<count):
            wantHaveTimeSeries[i].append(0)

    FinalData=[]
#Creates a nice snapshot of the data at that exact time
    for i in xrange(len(haveFreq)):
        FinalData.append([haveFreq[i][0],haveFreq[i][1],0,0.0])
    for i in xrange(len(wantFreq)):
        isNew=1
        for j in xrange(len(FinalData)):
            if(wantFreq[i][0]==FinalData[j][0]):
                FinalData[j][2]=wantFreq[i][1]
                isNew=0
        if(isNew==1):
            FinalData.append([wantFreq[i][0],0,wantFreq[i][1],0.0])
    for i in xrange(len(wantHaveRatio)):
        isNew=1
        for j in xrange(len(FinalData)):
            if(wantHaveRatio[i][0]==FinalData[j][0]):
                FinalData[j][3]=wantHaveRatio[i][1]
                isNew=0
        if(isNew==1):
            FinalData.append([wantHaveRatio[i][0],0,0,wantHaveRatio[i][1]])

#Writes to the time series files
    f = open("haveOutput.csv", "w+")

    for i in xrange(len(haveTimeSeries)):
        f.write(haveTimeSeries[i][0].encode('utf-8'))
        for j in xrange(1, len(haveTimeSeries[i])):
            f.write(","+str(haveTimeSeries[i][j]))
        f.write("\n")

    f.close()

    f = open("wantOutput.csv", "w+")

    for i in xrange(len(wantTimeSeries)):
        f.write(wantTimeSeries[i][0].encode('utf-8'))
        for j in xrange(1, len(wantTimeSeries[i])):
            f.write(","+str(wantTimeSeries[i][j]))
        f.write("\n")

    f.close()

    f = open("wantHaveOutput.csv", "w+")

    for i in xrange(len(wantHaveTimeSeries)):
        f.write(wantHaveTimeSeries[i][0].encode('utf-8'))
        for j in xrange(1, len(wantHaveTimeSeries[i])):
            f.write(","+str(wantHaveTimeSeries[i][j]))
        f.write("\n")

    f.close()

#runs the actual timing
schedule.every(30).minutes.do(takeSample)

while count < 120:
    schedule.run_pending()
    time.sleep(1)
