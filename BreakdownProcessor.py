import re


def getAckResultsProcessed(path, k, m, networkRound, warmTimes):
    ackLatencies=[]
    loopLatencies=[]
    file=open(path, "r")
    reader=file.readlines()

    for line in reader:
        latency = float(re.findall(r"\d+\.?\d*", line)[-1])
        ackLatencies.append(latency)

    ackNumPerLoop=(k+m)*networkRound
    ackLatencies=ackLatencies[(k+m):]
    # print(len(ackLatencies))

    for upperBound in range(ackNumPerLoop, len(ackLatencies)+1, ackNumPerLoop):
        # print("range", upperBound-ackNumPerLoop, upperBound)
        loopLatencies.append(sum(ackLatencies[upperBound-ackNumPerLoop : upperBound]))

    for i in range(len(loopLatencies)):
        print("Loop", i, "ack (us)", loopLatencies[i] / 1000.0)

    print("Ack avg latency (us)", sum(loopLatencies[warmTimes:])/(len(loopLatencies[warmTimes:])*1000.0))


if __name__=="__main__":
    ackPath=r"./breakdown/ack.breakdown"
    getAckResultsProcessed(ackPath, 4, 2, 16, 500)