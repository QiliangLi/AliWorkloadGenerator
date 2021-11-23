import os


def getYCSBWarmFile(path):
    putNames = set()
    warmNames =set()

    warmPath = "warm-" + os.path.basename(path)
    warmPath = os.path.join(os.path.dirname(path), warmPath)
    print("warmPath", warmPath)

    print("Finding warm requests......")
    file=open(path, "r")
    reader=file.readlines()

    for line in reader:
        # print(line)
        info=line.split(" ")
        typee = info[0].strip()
        name = info[1].strip()

        if typee == "R":
            if name not in putNames:
                warmNames.add(name)
        else:
            putNames.add(name)

    print(warmNames)
    with open(warmPath, "w", newline="") as warmFile:
        for name in warmNames:
            warmFile.write("I "+name.strip()+"\n")


if __name__=="__main__":
    path=r"./rawYCSBTraces/test5k.txt"
    getYCSBWarmFile(path)
