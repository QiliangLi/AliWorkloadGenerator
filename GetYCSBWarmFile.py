import os
import re
import csv


def getYCSBWarmFile(path):
    putNames = set()
    warmNames =set()

    warmPath = "warm-" + os.path.basename(path)
    warmPath = os.path.join(os.path.dirname(path), warmPath)
    print("warmPath", warmPath)

    print("Finding warm requests......")
    file=open(path, "r")
    reader=file.readlines()

    for line in reader:
        # print(line)
        info=line.split(" ")
        typee = info[0].strip()
        name = info[1].strip()

        if typee == "R":
            if name not in putNames:
                warmNames.add(name)
        else:
            putNames.add(name)

    print(warmNames)
    with open(warmPath, "w", newline="") as warmFile:
        for name in warmNames:
            warmFile.write("I "+name.strip()+"\n")


def getProcessedResult(path):
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
        for line in presults:
            writer.writerow(line)


def getBatchResultsProcessed(rootdir):
    fileList=os.listdir(rootdir)

    for file in fileList:
        if ".log" in file:
            print("Processing", file)
            getProcessedResult(os.path.join(rootdir,file))


if __name__=="__main__":
    # path=r"./rawYCSBTraces/test5k.txt"
    # getYCSBWarmFile(path)

    resultRoot=r"F:\Coding\Python\ali-trace\latencies"
    getBatchResultsProcessed(resultRoot)
