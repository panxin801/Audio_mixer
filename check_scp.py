import os, sys
currentPath = os.getcwd()

if len(sys.argv) != 3:
    print("param num error. Need 2 params.")
    exit(1)

baseFile = sys.argv[1]
needFix = sys.argv[2]

baseFile = os.path.join(currentPath, baseFile)
needFix = os.path.join(currentPath, needFix)

searchDict = {}
for line in open(needFix, "rt", encoding="utf-8"):
    line = line.strip()
    try:
        uttid, text = line.split(" ", 1)
        searchDict.update({uttid: text})
    except Exception:
        print(line + " Error.")

writeFile = needFix + "new"
wF = open(writeFile, "wt", encoding="utf-8")
for line in open(baseFile, "rt").readlines():
    uttid = line.strip().split(" ")[0]
    if uttid in searchDict:
        wF.write("%s %s\n" % (uttid, searchDict.get(uttid)))

wF.close()
print("Done!")