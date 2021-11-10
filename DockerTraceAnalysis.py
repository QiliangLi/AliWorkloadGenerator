import os
import json
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame, Series


def get_filelist(dir):
    print(os.listdir(dir))

    for subRoot in os.listdir(dir):
        print("Start zone", subRoot, "...")
        names = []
        types = []
        sizes = []

        for fileName in os.listdir(os.path.join(dir, subRoot)):
            jfilePath = os.path.join(dir, subRoot, fileName)
            print("Processing ", jfilePath)

            with open(jfilePath, "r") as jfile:
                jList = json.load(jfile)

                for jrecord in jList:
                    # print(jrecord)
                    if jrecord["http.request.method"] in ["PUT", "GET"]:
                        names.append(jrecord["host"] + jrecord["http.request.uri"])
                        types.append(jrecord["http.request.method"])
                        sizes.append(jrecord["http.response.written"])

        with open(subRoot + ".csv", "w", newline="") as resultFile:
            writer = csv.writer(resultFile)
            for i in range(len(names)):
                writer.writerow([names[i], types[i], sizes[i]])

        print("Zone", subRoot, "Finished!")


def getDetailedInfo(path):
    types = []
    sizes = []
    nameSet = set()
    putCounter = 0
    putSize = 0
    singlePutCounter = 0
    singlePutSize = 0
    getCounter = 0
    getSize = 0

    putGreaterThan1MRequestCounter = 0
    putGreaterThan1MSize = 0
    getGreaterThan1MRequestCounter = 0
    getGreaterThan1MSize = 0

    with open(path, "r") as resultFile:
        reader = csv.reader(resultFile)

        for line in reader:
            name = line[0]
            typee = line[1]
            sizee = int(line[2])
            print(name, typee, sizee)

            if typee == "PUT":
                putCounter += 1
                putSize += sizee / 1024 / 1024 / 1024

                if sizee >= 1024 * 1024:
                    putGreaterThan1MRequestCounter += 1

                if name not in nameSet:
                    singlePutCounter += 1
                    singlePutSize += sizee / 1024 / 1024 / 1024
            else:
                getCounter += 1
                getSize += sizee / 1024 / 1024 / 1024

                if sizee >= 1024 * 1024:
                    getGreaterThan1MRequestCounter += 1

            nameSet.add(name)
            types.append(typee)
            sizes.append(sizee)

    print("Request num", len(types))
    print("Put request num", putCounter, "sum size(GB)", putSize, "single put num", singlePutCounter, "sum size(GB)",
          singlePutSize)
    print("Put size greater than 1M num", putGreaterThan1MRequestCounter)

    print("Get request num", getCounter, "sum size(GB)", getSize)
    print("Get size greater than 1M num", getGreaterThan1MRequestCounter)


def plotCDF(path):
    putRecord = {}
    putRecord['Size'] = []
    getRecord = {}
    getRecord['Size'] = []

    data = pd.read_csv(path, header=None)
    data.columns = ['Name', 'Type', 'Size']

    # # 将size转换成MB
    # data['Size'] /= 1024 * 1024
    # 将size转换成KB
    data['Size'] /= 1024
    # print(data)

    # 获取数据的总数
    requestNum = len(data['Size'])
    for index, row in data.iterrows():
        if row['Type'] == "PUT":
            putRecord['Size'].append(row['Size'])
        else:
            getRecord['Size'].append(row['Size'])

    putRequestNum = len(putRecord['Size'])
    getRequestNum = len(getRecord['Size'])
    print(requestNum, putRequestNum, getRequestNum)

    putDf = DataFrame(putRecord)
    getDf = DataFrame(getRecord)

    # 将数据转换为Series
    Data = pd.Series(data['Size'])
    putData = pd.Series(putDf['Size'])
    getData = pd.Series(getDf['Size'])

    # 利用value_counts方法进行分组频数计算
    Fre = Data.value_counts()
    putFre = putData.value_counts()
    getFre = getData.value_counts()
    # print(Fre)

    # 对获得的表格整体按照索引自小到大进行排序
    Fre_sort = Fre.sort_index(axis=0, ascending=True)
    putFre_sort = putFre.sort_index(axis=0, ascending=True)
    getFre_sort = getFre.sort_index(axis=0, ascending=True)
    # print(Fre_sort)

    # 重置表格索引
    Fre_df = Fre_sort.reset_index()
    putFre_df = putFre_sort.reset_index()
    getFre_df = getFre_sort.reset_index()

    # 将列表列索引重命名
    Fre_df.columns = ['Size', 'Fre']
    putFre_df.columns = ['Size', 'Fre']
    getFre_df.columns = ['Size', 'Fre']
    # print(Fre_df)
    # print(type(Fre_df))

    # 将频数转换成概率
    Fre_df['Fre'] = Fre_df['Fre'] / requestNum
    putFre_df['Fre'] = putFre_df['Fre'] / putRequestNum
    getFre_df['Fre'] = getFre_df['Fre'] / getRequestNum

    # 利用cumsum函数进行概率的累加并按照顺序添加到表格中
    Fre_df['cumsum'] = np.cumsum(Fre_df['Fre'])
    putFre_df['cumsum'] = np.cumsum(putFre_df['Fre'])
    getFre_df['cumsum'] = np.cumsum(getFre_df['Fre'])

    # 创建画布
    plot = plt.figure()
    # 只有一张图，也可以多张
    ax1 = plot.add_subplot(1, 1, 1)
    # 按照Rds列为横坐标，累计概率分布为纵坐标作图
    ax1.plot(Fre_df['Size'], Fre_df['cumsum'], label="ALL")
    ax1.plot(putFre_df['Size'], putFre_df['cumsum'], label="PUT")
    ax1.plot(getFre_df['Size'], getFre_df['cumsum'], label="GET")
    # 图的标题
    ax1.set_title("CDF")
    # 横轴名
    ax1.set_xlabel("Object Size(KB)")
    # 纵轴名
    ax1.set_ylabel("P")
    # 横轴的界限
    ax1.set_xlim(-1, 16)
    plt.legend()
    # 图片显示
    plt.show()


if __name__ == "__main__":
    path = r"./data_centers"
    # get_filelist(path)

    detailedInfoPath = r"F:\Coding\Python\ali-trace\results\dal09.csv"
    # getDetailedInfo(detailedInfoPath)
    plotCDF(detailedInfoPath)

    # testPath=r"./test.csv"
    # plotCDF(testPath)

    # with open(r"F:\Coding\Python\ali-trace\data_centers\dal09\prod-dal09-logstash-2017.06.20-0.json","r") as f:
    #     data=json.load(f)
    #
    #     print(type(data[0]))
