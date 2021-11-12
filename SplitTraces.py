import os
import math


def createDirs(basedir, clientNum):
    # mkdir for every client
    for i in range(clientNum):
        folder = os.path.exists(os.path.join(basedir, "client" + str(i)))
        if not folder:
            os.makedirs(os.path.join(basedir, "client" + str(i)))


def splitYCSBTraces(path, basedir, clientNum):
    file = open(path, "r")
    reader = file.readlines()

    types = []
    objectNames = []
    for line in reader:
        info = line.split(" ")
        types.append(info[0])
        objectNames.append(info[1])

    splitNum = math.ceil(len(types) / clientNum)
    clientIndex = 0
    fileName = os.path.basename(path)

    for lowwerBound in range(0, len(types), splitNum):
        with open(os.path.join(basedir, "client" + str(clientIndex), fileName), "w", newline="") as splitFile:
            subTypes = types[lowwerBound:lowwerBound + splitNum]
            subNames = objectNames[lowwerBound:lowwerBound + splitNum]
            for i in range(len(subTypes)):
                splitFile.write(subTypes[i].strip() + " " + subNames[i].strip() + "\n")

        clientIndex += 1


def getSplitYCSBResults(warmPath, testPath, basedir, clientNum):
    createDirs(basedir, clientNum)
    splitYCSBTraces(warmPath, basedir, clientNum)
    splitYCSBTraces(testPath, basedir, clientNum)


def splitIBMResults(path, basedir, clientNum):
    file = open(path, "r")
    reader = file.readlines()

    lines = []
    for line in reader:
        lines.append(line)

    splitNum = math.ceil(len(lines) / clientNum)
    clientIndex = 0
    fileName = os.path.basename(path)

    for lowwerBound in range(0, len(lines), splitNum):
        with open(os.path.join(basedir, "client" + str(clientIndex), fileName), "w", newline="") as splitFile:
            subLines = lines[lowwerBound:lowwerBound + splitNum]
            for line in subLines:
                splitFile.write(line)

        clientIndex += 1


def getSplitIBMResults(warmPath, testPath, basedir, clientNum):
    createDirs(basedir, clientNum)
    splitIBMResults(warmPath, basedir, clientNum)
    splitIBMResults(testPath, basedir, clientNum)


if __name__ == "__main__":
    ycsbWarmPath = r"./rawYCSBTraces/warm.txt"
    ycsbTestPath = r"./rawYCSBTraces/test.txt"
    basedir = r"./clients/"
    clientNum = 6

    ibmWarmPath = r"./results/warm-filter-dal09.csv"
    ibmTestPath = r"./results/filter-dal09.csv"

    # getSplitYCSBResults(ycsbWarmPath, ycsbTestPath, basedir, clientNum)
    getSplitIBMResults(ibmWarmPath, ibmTestPath, basedir, clientNum)
