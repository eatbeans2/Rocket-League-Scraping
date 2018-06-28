import urllib2
import schedule
import time

from bs4 import BeautifulSoup

address = "https://www.rltprices.com/xbox"

priceTimeSeries = [["Parallax"],["Heatwave"],["Biomass"],["Torah"],["Hexed"],["Bubbly"]]

count = 1

def takeSample():

    global count
    global priceTimeSeries

    webAddress = urllib2.Request(address, headers={'User-Agent' : "Magic Browser"})

    page = urllib2.urlopen(webAddress)

    soup = BeautifulSoup(page, "html.parser")

    f = open("pricingIndex.csv", "w+")

#Finds a particular bmd
    for bmd in soup.find_all(string="Parallax"):
        priceTimeSeries[0].append(bmd.parent.parent.contents[5].string[:-3])
    for bmd in soup.find_all(string="Heatwave"):
        priceTimeSeries[1].append(bmd.parent.parent.contents[5].string[:-3])
    for bmd in soup.find_all(string="Biomass"):
        priceTimeSeries[2].append(bmd.parent.parent.contents[5].string[:-3])
    for bmd in soup.find_all(string="Tora"):
        priceTimeSeries[3].append(bmd.parent.parent.contents[5].string[:-3])
    for bmd in soup.find_all(string="Hexed"):
        priceTimeSeries[4].append(bmd.parent.parent.contents[5].string[:-3])
    for bmd in soup.find_all(string="Bubbly"):
        priceTimeSeries[5].append(bmd.parent.parent.contents[5].string[:-3])

    for i in xrange(len(priceTimeSeries)):
        f.write(priceTimeSeries[i][0].encode('utf-8'))
        for j in xrange(1, len(priceTimeSeries[i])):
            f.write(","+str(priceTimeSeries[i][j]))
        f.write("\n")
        
    f.close()
    count = count+1

schedule.every(30).minutes.do(takeSample)

while count < 120:
    schedule.run_pending()
    time.sleep(1)
