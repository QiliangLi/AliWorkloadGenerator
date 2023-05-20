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
        writer.writerow(["No", "Size", "Type", "IsDegradeRead", "replicas", "nativeec", "hydra", "microec"])
        for line in recordList:
            writer.writerow(line)


if __name__=="__main__":
    # rootdir=r"F:\Coding\Python\ali-trace\latencies\0808subDal09"
    # schemeList=["replicas", "nativeec", "microec"]
    # # degradePossList=[0.25, 0.5, 0.75, 1.0]
    # degradePossList=[0.5, 1.0]
    # suffix="ibm"
    #
    # for poss in degradePossList:
    #     mergePath=os.path.join(rootdir, str(poss)+"."+suffix+".csv")
    #     subList=[]
    #     print(mergePath)
    #     for scheme in schemeList:
    #         subPath=os.path.join(rootdir, scheme+"."+str(poss)+"."+suffix+".csv")
    #         subList.append(subPath)
    #         print(subPath)
    #     mergeLogs(mergePath, subList)


    # rootdirList = [r"F:\Coding\Python\ali-trace\latencies\optimal-ibm\0706subDal09_6h", r"F:\Coding\Python\ali-trace\latencies\optimal-ibm\0808subDal09", r"F:\Coding\Python\ali-trace\latencies\optimal-ibm\0811subDal09"]
    rootdirList = [r"F:\Coding\Python\ali-trace\latencies\0706subDal09_6h", r"F:\Coding\Python\ali-trace\latencies\0808subDal09", r"F:\Coding\Python\ali-trace\latencies\0811subDal09"]
    schemeList = ["replicas", "nativeec", "hydra", "microec"]
    # degradePossList=[0.25, 0.5, 0.75, 1.0]
    degradePossList = [0.5]
    suffix = "ibm"

    for rootdir in rootdirList:
        for poss in degradePossList:
            mergePath = os.path.join(rootdir, str(poss) + "." + suffix + ".csv")
            subList = []
            print(mergePath)
            for scheme in schemeList:
                subPath = os.path.join(rootdir, scheme + "." + str(poss) + "." + suffix + ".csv")
                subList.append(subPath)
                print(subPath)
            mergeLogs(mergePath, subList)


    # replicasRootDir=r"F:\Coding\Python\ali-trace\latencies"
    # schemeList = ["nativeec", "microec"]
    # degradePossList = [0.5, 1.0]
    # suffix = "ibm"
    #
    # # allroot = r"F:\Coding\Python\ali-trace\latencies\4core-ibm-latencies"
    # allroot = r"F:\Coding\Python\ali-trace\latencies\1core-ibm-latencies"
    # rootdirList = ["0706subDal09_6h", "0808subDal09", "0811subDal09"]
    # subIndexList = list(range(11))
    # for rootdir in rootdirList:
    #     for index in subIndexList:
    #         for poss in degradePossList:
    #             subList=[]
    #             subList.append(os.path.join(replicasRootDir, rootdir, "replicas."+str(poss)+"."+suffix+".csv"))
    #             mergePath=os.path.join(allroot, rootdir, str(index), str(poss) + ".ibm.csv")
    #             # print(os.path.join(allroot, rootdir, str(index), str(poss) + ".ibm.csv"))
    #             for scheme in schemeList:
    #                 subList.append(os.path.join(allroot, rootdir, str(index), scheme+"."+str(poss) + ".ibm.csv"))
    #             # print(mergePath, subList)
    #             mergeLogs(mergePath, subList)