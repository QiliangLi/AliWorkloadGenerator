import csv
import os


rate=0.03


def saveLatencies(latencies, savePath):
    if len(latencies) != 0:
        latencies.sort()
        bound = int(len(latencies) * rate)
        with open(savePath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for line in latencies[:-bound]:
            # for line in latencies:
                writer.writerow([line])


def mergeLogs(pathList, scheme, poss):
    putLatencies=[]
    getLatencies=[]
    degradeGetLatencies=[]
    rootdir = ""

    for path in pathList:
        rootdir=os.path.dirname(path)
        with open(path, "r") as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                typee = line[2]
                if typee == "PUT":
                    putLatencies.append(int(round(float(line[-1]),1)))
                else:
                    flag = line[3]
                    if flag == "true":
                        degradeGetLatencies.append(int(round(float(line[-1]),1)))
                    else:
                        getLatencies.append(int(round(float(line[-1]),1)))

    putPath = os.path.join(rootdir, "write." + scheme + "." + str(poss) + ".ycsb.csv")
    saveLatencies(putLatencies, putPath)
    getPath = os.path.join(rootdir, "read." + scheme + "." + str(poss) + ".ycsb.csv")
    saveLatencies(getLatencies, getPath)
    degradePath = os.path.join(rootdir, "degraderead." + scheme + "." + str(poss) + ".ycsb.csv")
    saveLatencies(degradeGetLatencies, degradePath)


def mergeLatencies(pathList, operation, poss):
    recordList = []
    rootdir=os.path.dirname(pathList[0])
    with open(pathList[0], "r") as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            recordList.append(line)
    for path in pathList[1:]:
        index=0
        with open(path, "r") as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                recordList[index].append(line[-1])
                index+=1

    savePath=os.path.join(rootdir, operation+"."+str(poss)+".ycsb.csv")
    with open(savePath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for line in recordList:
            writer.writerow(line)


if __name__=="__main__":
    rootdir=r"F:\Coding\Python\ali-trace\latencies\ycsb"
    schemeList = ["replicas", "nativeec", "microec"]
    degradePossList = [0.0]
    prefixList = ["n0", "n1", "n2", "n3"]

    subLogList=[]
    for poss in degradePossList:
        for scheme in schemeList:
            subLogList.clear()
            for prefix in prefixList:
                mergePath=os.path.join(rootdir, prefix+"."+scheme+"."+str(poss)+".ycsb.csv")
                subLogList.append(mergePath)
            print(subLogList)
            mergeLogs(subLogList, scheme, poss)

    operationList=["read", "write"]
    for poss in degradePossList:
        for operation in operationList:
            subLogList.clear()
            for scheme in schemeList:
                mergePath = os.path.join(rootdir, operation + "." + scheme + "." + str(poss) + ".ycsb.csv")
                subLogList.append(mergePath)
            print(subLogList)
            mergeLatencies(subLogList, operation, poss)
