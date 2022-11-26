import os
import re

sizeBound = 1024 * 1024
maxRatio = 0.05
minRatio = 0.02


def getErrorBarInfo(path, ratio):
    avgLatency=0
    latencyList=[]
    logFile=open(path)
    lines = logFile.readlines()
    for line in lines:
        if "avgLoopLatency(us)" in line:
            avgLatency = float(re.findall(r"\d+\.?\d*", line)[0])
        if "Loop " in line and "(us) " in line:
            latencyList.append(float(re.findall(r"\d+\.?\d*", line)[-1]))

    logFile.close()
    optimizedNum = int(len(latencyList) * ratio)
    # print(len(latencyList), optimizedNum)
    latencyList.sort()
    latencyList = latencyList[optimizedNum:-optimizedNum]
    # print(len(latencyList))

    # print(avgLatency, latencyList[0], latencyList[-1])
    return round(avgLatency), round(latencyList[0]), round(latencyList[-1])


def getWriteErrorBar(rootdir):
    suffixList=[".rep1.log", ".replicas.log", ".eccache.log", ".microec.log"]
    sizeList=[1024]
    size = 64 * 1024
    while size <= 64 * 1024 * 1024:
        sizeList.append(size)
        size = size * 4
    print(sizeList)

    for size in sizeList:
        for suffix in suffixList:
            ratio = 0.0
            if size >= sizeBound:
                ratio = minRatio
            else:
                ratio = maxRatio

            logPath = os.path.join(rootdir, str(size)+suffix)
            avgLatency, minLatency, maxLatency = getErrorBarInfo(logPath, ratio)
            print(os.path.basename(logPath)+","+str(avgLatency)+","+str(minLatency)+","+str(maxLatency))
            # print(os.path.basename(logPath)+","+str(minLatency)+","+str(maxLatency))


def getReadErrorBar(rootdir):
    suffixList=[".read.replicas.log", ".read.eccache.log", ".read.microec.log"]
    sizeList=[]
    size = 64 * 1024
    while size <= 16 * 1024 * 1024:
        sizeList.append(size)
        size = size * 4
    print(sizeList)

    for size in sizeList:
        for suffix in suffixList:
            ratio = 0.0
            if size >= sizeBound:
                ratio = minRatio
            else:
                ratio = maxRatio

            logPath = os.path.join(rootdir, str(size)+suffix)
            avgLatency, minLatency, maxLatency = getErrorBarInfo(logPath, ratio)
            # print(os.path.basename(logPath)+","+str(avgLatency)+","+str(minLatency)+","+str(maxLatency))
            print(os.path.basename(logPath)+","+str(minLatency)+","+str(maxLatency))


def getDegradeReadErrorBar(rootdir):
    suffixList=[".degradeRead.replicas.log", ".degradeRead.eccache.log", ".degradeRead.microec.log"]
    sizeList=[]
    size = 64 * 1024
    while size <= 16 * 1024 * 1024:
        sizeList.append(size)
        size = size * 4
    print(sizeList)

    for size in sizeList:
        for suffix in suffixList:
            ratio = 0.0
            if size >= sizeBound:
                ratio = minRatio
            else:
                ratio = maxRatio

            logPath = os.path.join(rootdir, str(size)+suffix)
            avgLatency, minLatency, maxLatency = getErrorBarInfo(logPath, ratio)
            # print(os.path.basename(logPath)+","+str(avgLatency)+","+str(minLatency)+","+str(maxLatency))
            print(os.path.basename(logPath)+","+str(minLatency)+","+str(maxLatency))


def getRecovery1lostErrorBar(rootdir):
    suffixList=[".recovery.replicas.log", ".recovery.eccache.log", ".recovery.microec.log"]
    sizeList=[]
    size = 64 * 1024
    while size <= 16 * 1024 * 1024:
        sizeList.append(size)
        size = size * 4
    print(sizeList)

    for size in sizeList:
        for suffix in suffixList:
            ratio = 0.0
            if size >= sizeBound:
                ratio = minRatio
            else:
                ratio = maxRatio

            logPath = os.path.join(rootdir, str(size)+suffix)
            avgLatency, minLatency, maxLatency = getErrorBarInfo(logPath, ratio)
            # print(os.path.basename(logPath)+","+str(round(1000000.0/avgLatency))+","+str(round(1000000.0/maxLatency))+","+str(round(1000000.0/minLatency)))
            print(os.path.basename(logPath)+","+str(round(1000000.0/maxLatency))+","+str(round(1000000.0/minLatency)))


def getRecovery2lostErrorBar(rootdir):
    suffixList=[".recovery.replicas.2fail.log", ".recovery.eccache.2fail.log", ".recovery.microec.2fail.log"]
    sizeList=[]
    size = 64 * 1024
    while size <= 16 * 1024 * 1024:
        sizeList.append(size)
        size = size * 4
    print(sizeList)

    for size in sizeList:
        for suffix in suffixList:
            ratio = 0.0
            if size >= sizeBound:
                ratio = minRatio
            else:
                ratio = maxRatio

            logPath = os.path.join(rootdir, str(size)+suffix)
            avgLatency, minLatency, maxLatency = getErrorBarInfo(logPath, ratio)
            # print(os.path.basename(logPath)+","+str(round(1000000.0/avgLatency))+","+str(round(1000000.0/maxLatency))+","+str(round(1000000.0/minLatency)))
            print(os.path.basename(logPath)+","+str(round(1000000.0/maxLatency))+","+str(round(1000000.0/minLatency)))


if __name__=="__main__":
    path=r"F:\Coding\Python\ali-trace\latencies\errorbar\text.log"
    writeRootdir = r"F:\Coding\Python\ali-trace\latencies\errorbar\write"
    readRootdir = r"F:\Coding\Python\ali-trace\latencies\errorbar\read"
    degradeReadRootdir = r"F:\Coding\Python\ali-trace\latencies\errorbar\degradeRead1lost"
    recovery1lostRootdir = r"F:\Coding\Python\ali-trace\latencies\errorbar\recovery1lost"
    recovery2lostRootdir = r"F:\Coding\Python\ali-trace\latencies\errorbar\recovery2lost"
    # getErrorBarInfo(path, ratio)

    getWriteErrorBar(writeRootdir)
    # getReadErrorBar(readRootdir)
    # getDegradeReadErrorBar(degradeReadRootdir)
    # getRecovery1lostErrorBar(recovery1lostRootdir)
    # getRecovery2lostErrorBar(recovery2lostRootdir)