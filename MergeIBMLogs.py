import csv
import os


def mergeLogs(mergePath, subList):
    recordList=[]
    with open(subList[0], "r") as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            recordList.append(line)
    for subPath in subList[1:]:
        index=0
        with open(subPath, "r") as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                recordList[index].append(line[-1])
                index+=1

    with open(mergePath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["No", "Size", "Type", "IsDegradeRead", "replicas", "nativeec", "microec"])
        for line in recordList:
            writer.writerow(line)


if __name__=="__main__":
    tracePath=r"F:\Coding\Python\ali-trace\results\mod16k_filter-1KB-1024MB-0706subDal09_6h.csv"
    rootdir=r"F:\Coding\Python\ali-trace\latencies"
    schemeList=["replicas", "nativeec", "microec"]
    # degradePossList=[0.25, 0.5, 0.75, 1.0]
    degradePossList=[0.5, 1.0]
    suffix="ibm"

    for poss in degradePossList:
        mergePath=os.path.join(rootdir, str(poss)+"."+suffix+".csv")
        subList=[]
        print(mergePath)
        for scheme in schemeList:
            subPath=os.path.join(rootdir, scheme+"."+str(poss)+"."+suffix+".csv")
            subList.append(subPath)
            print(subPath)
        mergeLogs(mergePath, subList)
