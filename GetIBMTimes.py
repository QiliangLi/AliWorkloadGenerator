import os
import pandas as pd


def getBoundNum(path, data, bound):
    nativeBoundNum = data["NativeecTimes"][data["NativeecTimes"] > bound].count()
    asyncBoundNum = data["HydraTimes"][data["HydraTimes"] > bound].count()
    microecBoundNum = data["MicroecTimes"][data["MicroecTimes"] > bound].count()

    print(path, nativeBoundNum, asyncBoundNum, microecBoundNum)


def optimizeResults(data, ratio):
    optimizedNum = int(data.shape[0] * ratio)
    print("optimizedNum ", optimizedNum * 2)

    data.sort_values("NativeecTimes", ascending=False, inplace=True)
    data.reset_index(drop=True, inplace=True)
    data.drop(index=list(range(optimizedNum+1)), axis=0, inplace=True)
    data.reset_index(drop=True, inplace=True)

    data.sort_values("HydraTimes", ascending=False, inplace=True)
    data.reset_index(drop=True, inplace=True)
    data.drop(index=list(range(optimizedNum + 1)), axis=0, inplace=True)
    data.reset_index(drop=True, inplace=True)

    data.sort_values("MicroecTimes", ascending=False, inplace=True)
    data.reset_index(drop=True, inplace=True)
    data.drop(index=list(range(optimizedNum + 1)), axis=0, inplace=True)
    data.reset_index(drop=True, inplace=True)

    # data.to_csv(r"F:\Coding\Python\ali-trace\latencies\optimized-test.csv", index=False)
    return data


def getTimes(path, bound = 3, ratio = 0.05):
    data = pd.read_csv(path)
    data["NativeecTimes"] = data[["replicas", "nativeec"]].apply(lambda x: round(x["nativeec"] / x["replicas"], 2),
                                                                 axis=1)
    data["HydraTimes"] = data[["replicas", "hydra"]].apply(lambda x: round(x["hydra"] / x["replicas"], 2),
                                                                 axis=1)
    data["MicroecTimes"] = data[["replicas", "microec"]].apply(lambda x: round(x["microec"] / x["replicas"], 2), axis=1)
    data = data.drop(['No', 'replicas', 'nativeec', 'hydra', 'microec'], axis=1)

    data = optimizeResults(data, ratio)

    data.sort_values("Size", inplace=True)
    # print(data.to_string())
    savePath = os.path.join(os.path.dirname(path), "optimized" + str(ratio) + ".times." + os.path.basename(path))
    data.to_csv(savePath, index=False)

    getBoundNum(path, data, bound)


def getTimesWithLatency(path, ratio = 0.05):
    data = pd.read_csv(path)
    data["NativeecTimes"] = data[["replicas", "nativeec"]].apply(lambda x: round(x["nativeec"] / x["replicas"], 2),
                                                                 axis=1)
    data["HydraTimes"] = data[["replicas", "hydra"]].apply(lambda x: round(x["hydra"] / x["replicas"], 2),
                                                               axis=1)
    data["MicroecTimes"] = data[["replicas", "microec"]].apply(lambda x: round(x["microec"] / x["replicas"], 2), axis=1)

    data = optimizeResults(data, ratio)

    data.sort_values("Size", inplace=True)
    # print(data.to_string())
    savePath = os.path.join(os.path.dirname(path), "optimized" + str(ratio) + "." + os.path.basename(path))
    data.to_csv(savePath, index=False)


if __name__ == "__main__":
    # degradePossList = [0.5, 1.0]
    degradePossList = [0.5]
    bound = 3
    ratio = 0.1

    rootdir = r"F:\Coding\Python\ali-trace\latencies"
    for poss in degradePossList:
        getTimesWithLatency(os.path.join(rootdir, "sum." + str(poss) + ".ibm.csv"), ratio)

    # rootdir=r"F:\Coding\Python\ali-trace\latencies"
    # # rootdir=r"F:\Coding\Python\ali-trace\latencies\optimal-ibm"
    # for poss in degradePossList:
    #     getTimes(os.path.join(rootdir, "sum."+str(poss)+".ibm.csv"), bound, ratio)

    # rootdirList=[r"F:\Coding\Python\ali-trace\latencies\0706subDal09_6h", r"F:\Coding\Python\ali-trace\latencies\0808subDal09", r"F:\Coding\Python\ali-trace\latencies\0811subDal09"]
    # # rootdirList = [r"F:\Coding\Python\ali-trace\latencies\optimal-ibm\0706subDal09_6h",
    # #                r"F:\Coding\Python\ali-trace\latencies\optimal-ibm\0808subDal09",
    # #                r"F:\Coding\Python\ali-trace\latencies\optimal-ibm\0811subDal09"]
    # for rootdir in rootdirList:
    #     for poss in degradePossList:
    #         getTimes(os.path.join(rootdir, str(poss) + ".ibm.csv"), bound)

    # # allroot=r"F:\Coding\Python\ali-trace\latencies\4core-ibm-latencies"
    # allroot=r"F:\Coding\Python\ali-trace\latencies\1core-ibm-latencies"
    # rootdirList=["0706subDal09_6h", "0808subDal09", "0811subDal09"]
    # subIndexList=list(range(1))
    # for rootdir in rootdirList:
    #     for poss in degradePossList:
    #         for index in subIndexList:
    #             # print(os.path.join(allroot, rootdir, str(index), str(poss) + ".ibm.csv"))
    #             getTimes(os.path.join(allroot, rootdir, str(index), str(poss) + ".ibm.csv"), bound)


    # data = pd.read_csv(r"F:\Coding\Python\ali-trace\latencies\test.csv")
    # optimizeResults(data, 0.05)
