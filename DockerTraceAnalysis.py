import os
import json
import csv


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


if __name__ == "__main__":
    path = r"./data_centers"
    # get_filelist(path)

    detailedInfoPath = r"F:\Coding\Python\ali-trace\results\dal09.csv"
    getDetailedInfo(detailedInfoPath)

    # with open(r"F:\Coding\Python\ali-trace\data_centers\dal09\prod-dal09-logstash-2017.06.20-0.json","r") as f:
    #     data=json.load(f)
    #
    #     print(type(data[0]))
