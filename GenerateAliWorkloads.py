import csv
import os


def getCDFDict(path):
    cdfFile = open(path, "r")
    reader = csv.DictReader(cdfFile)
    filename = os.path.basename(path).split(".csv")[0]

    cdfRatio = {}
    lastCDF = 0

    for line in reader:
        # print(line)
        # print(float(line['size'])/1024)
        cdfRatio[int(line['size'])] = float(line[filename]) - lastCDF
        lastCDF += cdfRatio[int(line['size'])]

    print(cdfRatio)
    return cdfRatio


def getHundredNormalizedRatioDict(cdfRatio, minObjectSize, maxObjectSize):
    sumRatio = 0
    hundredNormalizedRatio = {}
    for objectSize in cdfRatio:
        if objectSize >= minObjectSize and objectSize <= maxObjectSize:
            sumRatio += cdfRatio[objectSize]

    print("sumRatio ", sumRatio)

    for objectSize in cdfRatio:
        if objectSize >= minObjectSize and objectSize <= maxObjectSize:
            hundredNormalizedRatio[objectSize] = cdfRatio[objectSize] / sumRatio

    tmpSum = 0
    conditionSum = 0
    for objectSize in hundredNormalizedRatio:
        tmpSum += hundredNormalizedRatio[objectSize]
        if objectSize < 1024 * 1024:
            conditionSum += hundredNormalizedRatio[objectSize]
        print("objectSize ", objectSize / 1024, cdfRatio[objectSize], hundredNormalizedRatio[objectSize])

    print(tmpSum)
    print(conditionSum)


def generateWorkload(path, requestNum, clientNum, minObjectSize, maxObjectSize):
    cdfRatio = getCDFDict(path)
    hundredNormalizedRatio = getHundredNormalizedRatioDict(cdfRatio, minObjectSize, maxObjectSize)


if __name__ == "__main__":
    countPath = r"cdf_count.csv"
    freqPath = r"cdf_frequency.csv"

    writeRequestNum = 1000
    readRequestNum = 1000

    clientNum = 6

    minObjectSize = 1024 * 1024
    maxObjectSize = 64 * 1024 * 1024

    generateWorkload(countPath, writeRequestNum, clientNum, minObjectSize, maxObjectSize)

    # folder=os.path.exists(str(clientNum))
    #
    # if not folder:
    #     os.makedirs(str(clientNum))
