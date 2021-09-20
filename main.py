import argparse
import csv
import datetime
import re
import urllib
from io import StringIO


def downloadData(url):
    content = urllib.request.urlopen(url).read().decode("ascii", "ignore")
    return content


def processData(file):
    data = StringIO(file)
    csv_reader = csv.reader(data, delimiter=',')
    next(csv_reader)
    dataList = []
    for line in csv_reader:
        dataList.append(line)
    return dataList


imageBrowserList = []


def imageHits(dataList):

    count = 0
    imageCount = 0
    for line in dataList:
        extensionList = re.findall('([^\s]+(\.(?i)(jpg|png|gif))$)', line[0])
        if len(extensionList) > 0:
            imageCount += 1
            imageBrowserList.append(line)
        count += 1
    imagePercentage = (imageCount / count) * 100
    imagePercentage = round(imagePercentage, 1)
    print("Image request acount for {} % of all requests".format(imagePercentage))


def browserType(imageBrowserList=None, browserTup=None):
    if imageBrowserList is None:
        imageBrowserList = imageBrowserList
    browserCount = {}
    browserList = []
    for line in imageBrowserList:
        browserType = re.findall("(?i)(firefox|msie|chrome|safari)[/\s]([\d.]+)", line[2])
        browserList.append(browserType)
    for browsers in browserList:
        if browsers[0][0] not in browserCount:
            browserCount[browsers[0][0]] = 1
        else:
            browserCount[browsers[0][0]] += 1
    browserTup.sort(reverse=True)
    print("The most used browser in {} with {} hits".format(browserTup[0][1], browserTup[0][0]))

def hourHits(dataList, histDict=None):
    hitsDict = {}
    for data in dataList:
        hours = datetime.datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S').hour
        if hours not in hitsDict:
            hitsDict[hours] = 1
        else:
            hitsDict[hours] += 1
        hitsTup = list()
        for key, value in list(histDict.items()):
            hitsTup.append((value, key))
        hitsTup.sort(reverse=True)
        for i, value in hitsTup:
            print("Hour {} has {} hits".format(value, i))


def main():
    commandParser = argparse.ArgumentParser(description="Send a --url parameter to the script")
    commandParser.add_argument("--url", type=str, help="Link to the csv file")
    args = commandParser.parse_args()
    if not args.url:
        exit()

    try:
        csvData = downloadData(args.url)
    except:
        print("An error has occurred. Please try again")
        exit()
    browserData = processData(csvData)
    image = imageHits(browserData)
    browserType()
    hourHits(browserData)

if __name__ == "__main__":
    main()