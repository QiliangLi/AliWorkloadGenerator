import csv
import os

def analysisCDFCount(countPath, writeRequestNum, clientNum, minObjectSize, maxObjectSize):
    countCDFFile=open(countPath,"r")
    countReader=csv.DictReader(countCDFFile)

    for line in countReader:
        print(line)

        print(float(line['size'])/1024)


if __name__=="__main__":
    countPath=r"cdf_count.csv"
    freqPath=r"cdf_frequency.csv"

    writeRequestNum=1000
    readRequestNum=1000

    clientNum=6

    minObjectSize=64*1024
    maxObjectSize=64*1024*1024

    analysisCDFCount(countPath,writeRequestNum,clientNum,minObjectSize,maxObjectSize)

    # folder=os.path.exists(str(clientNum))
    #
    # if not folder:
    #     os.makedirs(str(clientNum))