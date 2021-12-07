import os
import re
import csv


def getTraceInfos(tracePath):
    sizeList = []
    with open(tracePath, "r") as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            sizeList.append(line[-1])

    return sizeList


def getProcessedResult(path, tracePath):
    sizeList = getTraceInfos(tracePath)

    processedPath = ""
    if "repeat" in path:
        processedPath = "processed-" + os.path.basename(path).split(".log")[0] + os.path.basename(path).split(".log")[
            1] + ".csv"
    else:
        processedPath = "processed-" + os.path.basename(path).split(".log")[0] + ".csv"
    print(processedPath)

    processedPath = os.path.join(os.path.dirname(path), processedPath)
    presults = []
    file = open(path, "r")
    reader = file.readlines()

    for line in reader:
        if "Request " in line and "type" in line:
            latency = re.findall(r"\d+\.?\d*", line)[-1]
            typee = line.strip("type ")[0].strip()
            presults.append([latency, typee])

    with open(processedPath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        requestNum = len(sizeList)
        for i in range(requestNum):
            writer.writerow(presults[i] + [sizeList[i]])


def getBatchResultsProcessed(rootdir, tracePath):
    fileList = os.listdir(rootdir)

    for file in fileList:
        if ".log" in file and "ibm" in file:
            print("Processing", file)
            getProcessedResult(os.path.join(rootdir, file), tracePath)


def getFileProcessedAnalysised(path, lowwerBound, upperBound):
    infoList = []

    with open(path, "r") as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            objectSize = int(line[-1])

            if (objectSize <= upperBound and objectSize >= lowwerBound):
                infoList.append(line)

    return infoList


def getResultsProcessedAnalysised(rootdir, suffient, lowwerBound, upperBound):
    fileList = os.listdir(rootdir)
    schemesList = ["64kpipe", "eccache", "monEC"]
    schemesMapper = {}

    for file in fileList:
        if ".csv" in file and "processed-degrade.ibm" in file and suffient in file:
            print("Processing", file)

            for sche in schemesList:
                if sche in file:
                    schemesMapper[sche] = getFileProcessedAnalysised(os.path.join(rootdir, file), lowwerBound,
                                                                     upperBound)

    baseList=schemesMapper["64kpipe"]
    for record in baseList:
        record=record.reverse()
    # print(baseList)

    for sche in schemesList:
        if sche == "64kpipe":
            continue

        for i in range(len(schemesMapper[sche])):
            baseList[i].append(schemesMapper[sche][i][0])

    for record in baseList:
        print(record)


if __name__ == "__main__":
    resultRoot = r"./latencies"
    tracePath = r"./results/mod16k_filter-0706subDal09_6h.csv"
    getBatchResultsProcessed(resultRoot, tracePath)

    # getResultsProcessedAnalysised(resultRoot, "repeat0", 16*1024, 256*1024)


