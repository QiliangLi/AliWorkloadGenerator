import os
import pandas as pd


def getTimes(path):
    data = pd.read_csv(path)
    data["NativeecTimes"] = data[["replicas", "nativeec"]].apply(lambda x: round(x["nativeec"] / x["replicas"], 2),
                                                                 axis=1)
    data["MicroecTimes"] = data[["replicas", "microec"]].apply(lambda x: round(x["microec"] / x["replicas"], 2), axis=1)
    data = data.drop(['No', 'replicas', 'nativeec', 'microec'], axis=1)
    data.sort_values("Size", inplace=True)
    # print(data.to_string())
    savePath=os.path.join(os.path.dirname(path), "times."+os.path.basename(path))
    data.to_csv(savePath, index=False)


if __name__ == "__main__":
    rootdir=r"F:\Coding\Python\ali-trace\latencies"
    degradePossList = [0.5, 1.0]
    for poss in degradePossList:
        getTimes(os.path.join(rootdir, "sum."+str(poss)+".ibm.csv"))
