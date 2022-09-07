import csv
import os


def mergeSubLogs(pathList, savePath):
    recordList = []
    for path in pathList:
        with open(path, "r") as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                if "No" in line:
                    continue
                recordList.append(line[1:])

    with open(savePath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["No", "Size", "Type", "IsDegradeRead", "replicas", "nativeec", "microec"])
        index = 0
        for line in recordList:
            writer.writerow([index]+line)
            index+=1


if __name__=="__main__":
    saveRootdir=r"F:\Coding\Python\ali-trace\latencies"
    rootdirList=[r"F:\Coding\Python\ali-trace\latencies\0706subDal09_6h", r"F:\Coding\Python\ali-trace\latencies\0808subDal09", r"F:\Coding\Python\ali-trace\latencies\0811subDal09"]
    degradePossList=[0.5, 1.0]

    pathList=[]
    for poss in degradePossList:
        pathList.clear()
        for rootdir in rootdirList:
            path = os.path.join(rootdir, str(poss)+".ibm.csv")
            pathList.append(path)
        print(pathList)
        mergeSubLogs(pathList, os.path.join(saveRootdir, "sum."+str(poss)+".ibm.csv"))
