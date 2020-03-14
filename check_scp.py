import os, sys
currentPath = os.getcwd()

if len(sys.argv) != 3:
    print("param num error. Need 2 params.")
    exit(1)

baseFile = sys.argv[1]
needFix = sys.argv[2]

baseFile = os.path.join(currentPath, baseFile)
needFix = os.path.join(currentPath, needFix)

baseDict = {}
for line in open(baseFile, "rt").readlines():
    uttid, filepath = line.strip().split(" ")
    baseDict.update({uttid: filepath})

writeFile = needFix + "new"
wF = open(writeFile, "wt", encoding="utf-8")
for line in open(needFix, "rt", encoding="utf-8"):
    line = line.strip()
    uttid, text = line.split(" ", 1)
    if uttid in baseDict:
        wF.write("%s %s\n" % (uttid, text))
wF.close()
print("Done!")