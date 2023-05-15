import os
import pandas as pd
import sys


def getMean(path):
    data = pd.read_csv(path)
    first = data[data.index % 2 == 0]
    second = data[data.index % 2 == 1]

    # print(first.to_string())
    # print(second.to_string())
    # print(first["Latency"].sum() / len(first["Latency"]))
    # print(second["Latency"].sum() / len(second["Latency"]))

    return str(format(first["stage1"].sum() / len(first["stage1"]), '.1f')) + "," + str(format(
        second["stage1"].sum() / len(second["stage1"]), '.1f')) + "," + str(format(
        first["stage2"].sum() / len(first["stage2"]), '.1f')) + "," + str(format(
        second["stage2"].sum() / len(second["stage2"]), '.1f')) + "," + str(format(
        first["stage3"].sum() / len(first["stage3"]), '.1f')) + "," + str(format(
        second["stage3"].sum() / len(second["stage3"]), '.1f')) + "," + str(format(
        first["stage4"].sum() / len(first["stage4"]), '.1f')) + "," + str(
        format(second["stage4"].sum() / len(second["stage4"]), '.1f'))


if __name__ == "__main__":
    # path = r"./tmp1.csv"
    # print(getMean(path))
    print(str(sys.argv[1]) + ",", getMean(sys.argv[2]))
