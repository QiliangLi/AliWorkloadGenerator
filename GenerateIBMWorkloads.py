from DockerTraceAnalysis import *


if __name__ == "__main__":
    path = r"./data_centers"
    # subRoot = r"0706subDal09_6h"
    subRoot = r"0811subDal09"
    # detailedInfoPath = r"F:\Coding\Python\ali-trace\results\0706subDal09_6h.csv"
    detailedInfoPath = getZoneFileList(path, subRoot)

    filterPath = getFilterTraces(detailedInfoPath, 1 * 1024, 1024 * 1024 * 1024)
    warmPath = getWarmRequest(filterPath)

    eraseWarmDuplicatedPut(filterPath)
    eraseWarmDuplicatedPut(warmPath)
    eraseTestDuplicatedPut(warmPath, filterPath)

    testModPath = getModifiedRequestSizes(filterPath, 16 * 1024, 4)
    warmModPath = getModifiedRequestSizes(warmPath, 16 * 1024, 4)

    for pos in np.arange(0.5, 1.1, 0.5):
        tmpfile = getRandomIsDegradeRead(warmModPath, pos)
        fillReadInWarm(tmpfile, pos)
    for pos in np.arange(0.5, 1.1, 0.5):
        getRandomIsDegradeRead(testModPath, pos)