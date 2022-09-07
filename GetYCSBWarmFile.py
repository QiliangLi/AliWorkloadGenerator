import os
import re
import csv
import random
import numpy as np


# 根据YCSB的test.txt生成warm.text
# 消除原始test.txt的第三列乱值
def getYCSBWarmFile(path):
    testList = []
    putNames = set()
    warmNames = set()

    warmPath = "warm-" + os.path.basename(path)
    warmPath = os.path.join(os.path.dirname(path), warmPath)
    print("warmPath", warmPath)

    print("Finding warm requests......")
    file = open(path, "r")
    reader = file.readlines()

    for line in reader:
        # print(line)
        info = line.split(" ")
        typee = info[0].strip()
        name = info[1].strip()
        testList.append([typee, name])

        if typee == "R":
            if name not in putNames:
                warmNames.add(name)
        else:
            putNames.add(name)

    print(warmNames)
    with open(warmPath, "w", newline="") as warmFile:
        for name in warmNames:
            warmFile.write("I " + name.strip() + "\n")

    with open(path, "w", newline="") as testFile:
        for line in testList:
            testFile.write(line[0] + " " + line[1].strip() + "\n")

    return warmPath


def eraseWarmDuplicatedPut(path):
    requests = []
    nameSet = set()

    file = open(path, "r")
    reader = file.readlines()

    for line in reader:
        info = line.split(" ")
        typee = info[0].strip()
        name = info[1].strip()
        if typee == "I" and name not in nameSet:
            nameSet.add(name)
            requests.append(info)
        elif typee == "R":
            requests.append(info)
        else:
            print(line)

    with open(path, "w", newline="") as writer:
        for line in requests:
            writer.write(line[0] + " " + line[1].strip() + "\n")


def eraseTestDuplicatedPut(warmPath, testPath):
    requests = []
    warmNameSet = set()

    file = open(warmPath, "r")
    reader = file.readlines()
    for line in reader:
        info = line.split(" ")
        typee = info[0].strip()
        name = info[1].strip()
        warmNameSet.add(name)

    file = open(testPath, "r")
    reader = file.readlines()
    for line in reader:
        info = line.split(" ")
        typee = info[0].strip()
        name = info[1].strip()
        if typee == "I" and name in warmNameSet:
            print(info)
            continue
        requests.append(info)

    with open(testPath, "w", newline="") as writer:
        for line in requests:
            writer.write(line[0] + " " + line[1].strip() + "\n")


def getRandomIsDegradeRead(path, possibility):
    fileName = str(possibility) + "-" + os.path.basename(path)
    fileName = os.path.join(os.path.dirname(path), fileName)

    requests = []
    file = open(path, "r")
    reader = file.readlines()
    for line in reader:
        info = line.split(" ")
        typee = info[0].strip()
        name = info[1].strip()
        flag = False
        if typee == "R" and random.random() < possibility:
            flag = True
        info.append(flag)
        requests.append(info)

    with open(fileName, "w", newline="") as writer:
        for line in requests:
            writer.write(line[0].strip() + " " + line[1].strip() + " " + str(line[2]) + "\n")

    return fileName


def fillReadInWarm(path, possibility):
    putRequests = []
    getRequests = []

    file = open(path, "r")
    reader = file.readlines()
    for line in reader:
        info = line.split(" ")
        typee = info[0].strip()
        name = info[1].strip()
        putRequests.append(info)
        flag = False
        if typee == "I" and random.random() < possibility:
            flag = True
        record = ["R", name, flag]
        getRequests.append(record)

    requests = putRequests + getRequests

    with open(path, "w", newline="") as writer:
        for line in requests:
            writer.write(line[0].strip() + " " + line[1].strip() + " " + str(line[2]).strip() + "\n")


# 将crail里输出的log结果转换成csv格式：latency,type
def getProcessedResult(path):
    processedPath = "processed-" + os.path.basename(path).split(".log")[0] + ".csv"
    processedPath = os.path.join(os.path.dirname(path), processedPath)
    presults = []
    file = open(path, "r")
    reader = file.readlines()

    for line in reader:
        if "Request " in line and "type" in line:
            latency = re.findall(r"\d+\.?\d*", line)[-1]
            typee = line.split("type ")[1].strip()
            presults.append([latency, typee])

    with open(processedPath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for line in presults:
            writer.writerow(line)


def getBatchResultsProcessed(rootdir):
    fileList = os.listdir(rootdir)

    for file in fileList:
        if ".log" in file and "ycsb" in file and "processed" not in file:
            print("Processing", file)
            getProcessedResult(os.path.join(rootdir, file))


if __name__ == "__main__":
    testPath = r"./rawYCSBTraces/test2w.txt"
    warmPath = getYCSBWarmFile(testPath)

    eraseWarmDuplicatedPut(testPath)
    eraseWarmDuplicatedPut(warmPath)
    eraseTestDuplicatedPut(warmPath, testPath)

    for pos in np.arange(0, 1.1, 2):
        tmpfile = getRandomIsDegradeRead(warmPath, pos)
        fillReadInWarm(tmpfile, pos)
    for pos in np.arange(0, 1.1, 2):
        getRandomIsDegradeRead(testPath, pos)

    # resultRoot = r"F:\Coding\Python\ali-trace\latencies"
    # getBatchResultsProcessed(resultRoot)
