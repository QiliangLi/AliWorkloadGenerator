import os
import pandas as pd
import sys


def getMean(path):
    data = pd.read_csv(path)
    # print(data["Latency"].sum() / len(data["Latency"]))
    return data["Latency"].sum() / len(data["Latency"])


if __name__ == "__main__":
    # path = r"./tmp.csv"
    # getMean(path)
    print(str(sys.argv[1])+",", getMean(sys.argv[2]))
