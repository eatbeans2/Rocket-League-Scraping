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

#Function for sampling values from the forums
def takeSample():

    global count
    global haveTimeSeries
    global wantTimeSeries

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
            haveFreq = []
            wantFreq = []
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
            haveTimeSeries.append(haveFreq)
            wantTimeSeries.append(wantFreq)

#Writes to the time series files
    f = open("haveOutput.csv", "w+")

    f.write("TradeID,ItemIn\n")
    for i in xrange(len(haveTimeSeries)):
        for j in xrange(len(haveTimeSeries[i])):
            for k in xrange(haveTimeSeries[i][j][1]):
                f.write(str(i)+",")
                f.write(haveTimeSeries[i][j][0].encode('utf-8'))
                f.write("\n")

    f.close()

    f = open("wantOutput.csv", "w+")

    f.write("TradeID,ItemIn\n")
    for i in xrange(len(wantTimeSeries)):
        for j in xrange(len(wantTimeSeries[i])):
            for k in xrange(wantTimeSeries[i][j][1]):
                f.write(str(i)+",")
                f.write(wantTimeSeries[i][j][0].encode('utf-8'))
                f.write("\n")
    f.close()
"""
    f = open("wantHaveOutput.csv", "w+")

    for i in xrange(len(wantHaveTimeSeries)):
        f.write(wantHaveTimeSeries[i][0].encode('utf-8'))
        for j in xrange(1, len(wantHaveTimeSeries[i])):
            f.write(","+str(wantHaveTimeSeries[i][j]))
        f.write("\n")

    f.close()
"""
#runs the actual timing
schedule.every().minute.do(takeSample)

while count < 120:
    schedule.run_pending()
    time.sleep(1)
