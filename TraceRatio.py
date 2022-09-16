import csv


def getBoundRatio(path, bound):
    requestCounter=0
    boundCounter=0
    sumFootprint=0
    boundFootprint=0
    with open(path, "r") as resultFile:
        reader = csv.reader(resultFile)

        for line in reader:
            sizee = int(line[2])
            sumFootprint += sizee / 1024 / 1024 / 1024
            requestCounter+=1
            if sizee <= bound:
                boundFootprint += sizee / 1024 / 1024 / 1024
                boundCounter+=1

    print(requestCounter, boundCounter, "request ratio ", boundCounter/requestCounter, sumFootprint, boundFootprint, "footprint ratio ", boundFootprint/sumFootprint)
    return requestCounter, boundCounter,


if __name__=="__main__":
    path=r"./results/dev-mon01.csv"
    bound = 64*1024
    getBoundRatio(path, bound)