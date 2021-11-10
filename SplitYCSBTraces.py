import os
import math


def createDirs(basedir, clientNum):
    # mkdir for every client
    for i in range(clientNum):
        folder = os.path.exists(os.path.join(basedir, "client" + str(i)))
        if not folder:
            os.makedirs(os.path.join(basedir, "client" + str(i)))


def splitYCSBTraces(path, basedir, clientNum):
    file=open(path,"r")
    reader=file.readlines()

    types=[]
    objectNames=[]
    for line in reader:
        info=line.split(" ")
        types.append(info[0])
        objectNames.append(info[1])

    splitNum=math.ceil(len(types)/clientNum)
    clientIndex=0
    fileName=os.path.basename(path)

    for lowwerBound in range(0,len(types),splitNum):
        with open(os.path.join(basedir, "client"+str(clientIndex), fileName), "w", newline="") as splitFile:
            subTypes=types[lowwerBound:lowwerBound+splitNum]
            subNames=objectNames[lowwerBound:lowwerBound+splitNum]
            for i in range(len(subTypes)):
                splitFile.write(subTypes[i].strip()+" "+subNames[i].strip()+"\n")

        clientIndex+=1


def getSplitYCSBResults(warmPath, testPath, basedir, clientNum):
    createDirs(basedir, clientNum)
    splitYCSBTraces(warmPath, basedir, clientNum)
    splitYCSBTraces(testPath, basedir, clientNum)


if __name__=="__main__":
    warmPath=r"./RawYCSBTraces/warm.txt"
    testPath=r"./RawYCSBTraces/test.txt"
    basedir=r"./"

    clientNum=6
    getSplitYCSBResults(warmPath, testPath, basedir, clientNum)

    # folder=os.path.exists(str(clientNum))
    #
    # if not folder:
    #     os.makedirs(str(clientNum))