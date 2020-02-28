import os, sys
from sys import argv


def main():
    currentPath = os.getcwd()
    print("%d params." % (len(argv) - 1))
    wavRead = argv[1]
    noiseRead = argv[2]

    wavRead = os.path.join(currentPath, wavRead)
    noiseRead = os.path.join(currentPath, noiseRead)
    if not (os.path.exists(wavRead) and os.path.exists(noiseRead)):
        print("%s or %s not exists." % (wavRead, noiseRead))
        sys.exit(1)
    wavSave = os.path.join(currentPath, "wav.scp")
    noiseSave = os.path.join(currentPath, "noise.scp")
    writeNewFile(wavRead, wavSave, 10001)
    writeNewFile(noiseRead, noiseSave, 20001)
    print("Done")


def writeNewFile(readDir, saveFile, startIndex):
    wavName = []
    for __, __, files in os.walk(readDir):
        for fileNameExt in files:
            wavName.append(os.path.splitext(fileNameExt)[0])

    writeFile = open(saveFile, "wt", encoding="utf-8")
    start = startIndex
    for name in wavName:
        name = os.path.join(readDir, name)
        writeFile.write("%s %s%s\n" % (start, name, ".wav"))
        start += 1
    writeFile.close()
    wavName.clear()


if __name__ == "__main__":
    main()