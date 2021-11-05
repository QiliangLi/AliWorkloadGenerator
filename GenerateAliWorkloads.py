import csv
import os


def getCDFDict(path):
    cdfFile=open(path, "r")
    reader=csv.DictReader(cdfFile)
    filename=os.path.basename(path).split(".csv")[0]

    cdfRatio={}
    lastCDF=0

    for line in reader:
        print(line)
        print(float(line['size'])/1024)

        cdfRatio[int(line['size'])]=float(line[filename])-lastCDF


if __name__=="__main__":
    countPath=r"cdf_count.csv"
    freqPath=r"cdf_frequency.csv"

    writeRequestNum=1000
    readRequestNum=1000

    clientNum=6

    minObjectSize=64*1024
    maxObjectSize=64*1024*1024

    getCDFDict(countPath)

    # folder=os.path.exists(str(clientNum))
    #
    # if not folder:
    #     os.makedirs(str(clientNum))