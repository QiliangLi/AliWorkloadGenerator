import os
import re
import csv


def getTraceInfos(tracePath):
    sizeList=[]
    with open(tracePath, "r") as csvfile:
        reader=csv.reader(csvfile)
        for line in reader:
            sizeList.append(line[-1])

    return sizeList


def getProcessedResult(path, tracePath):
    sizeList=getTraceInfos(tracePath)

    processedPath = "processed-" + os.path.basename(path).split(".log")[0] +".csv"
    processedPath = os.path.join(os.path.dirname(path), processedPath)
    presults=[]
    file = open(path, "r")
    reader = file.readlines()

    for line in reader:
        if "Request " in line and "type" in line:
            latency=re.findall(r"\d+\.?\d*", line)[-1]
            typee=line.strip("type ")[0].strip()
            presults.append([latency, typee])

    with open(processedPath, "w", newline="") as csvfile:
        writer=csv.writer(csvfile)

        requestNum=len(sizeList)
        for i in range(requestNum):
            writer.writerow(presults[i]+[sizeList[i]])


def getBatchResultsProcessed(rootdir, tracePath):
    fileList=os.listdir(rootdir)

    for file in fileList:
        if ".log" in file and "ibm" in file:
            print("Processing", file)
            getProcessedResult(os.path.join(rootdir,file), tracePath)


if __name__=="__main__":
    resultRoot=r"./latencies"
    tracePath=r"./results/mod16k_filter-0706subDal09_6h.csv"
    getBatchResultsProcessed(resultRoot, tracePath)
