import os
import sys
import random


def write_new_base_file(currentPath, processFileName, textContext):
    num = 0
    tmpSave = os.path.join(currentPath, processFileName + "_new")
    tmpRead = os.path.join(currentPath, processFileName)
    with open(tmpSave, "wt") as f:
        for line in open(tmpRead, "rt").readlines():
            line = line.strip()
            uttid, context = line.split(" ")
            if uttid in textContext.keys():
                f.write("%s %s\n" % (uttid, context))
                num += 1
    print("%s write done." % (tmpSave))
    if num == len(textContext.keys()):
        os.remove(tmpRead)
        os.rename(tmpSave, tmpRead)
    else:
        print("%s dont have same lines with text." % (tmpRead))
        sys.exit(1)


def write_output_file(savePath, saveName, indexList, fileKeys, contextDict):
    with open(os.path.join(savePath, saveName), "wt", encoding="utf-8") as f:
        for i in indexList:
            key = fileKeys[i - 1]
            value = contextDict.get(key)
            f.write("%s %s\n" % (key, value))


if __name__ == "__main__":
    currentPath = sys.argv[1]
    # currentPath = r"C:\Users\PX\Desktop\train_mixed"
    # savePath = r"C:\Users\PX\Desktop"

    percent = 0.1
    seed = 1235
    backffix = "_with_noise"

    if currentPath.endswith("/") or currentPath.endswith("\\"):
        currentPath = currentPath[:-1]
    savePath = os.path.dirname(currentPath)

    textContext = {}
    empty = False
    for line in open(
            os.path.join(currentPath, "text"), "rt",
            encoding="utf-8").readlines():
        line = line.strip()
        # print(line)
        try:
            utt, text = line.split(" ", 1)
            utt = str(utt)
            text = str(text)
            textContext.update([(utt, text)])
        except Exception:
            empty = True
            print(line)
    # Done text dict make

    # Maybe this one is optional
    if empty:
        tmpSave = os.path.join(currentPath, "text_new")
        with open(tmpSave, "wt", encoding="utf-8") as f:
            for key in textContext.keys():
                f.write("%s %s\n" % (key, textContext.get(key)))
        print("Blank line occurs!!!")
        tmpRead = os.path.join(currentPath, "text")
        os.remove(tmpRead)
        os.rename(tmpSave, tmpRead)

        write_new_base_file(currentPath, "utt2spk", textContext)
        write_new_base_file(currentPath, "wav.scp", textContext)

    # Back to regular route
    readFilename = os.path.join(currentPath, "wav.scp")
    fileContext = {}
    for line in open(readFilename, "rt").readlines():
        line = line.strip()
        utt, path = line.split(" ")
        utt = str(utt)
        fileContext.update({utt: path})
    # Done wav dict make

    utt2spkContext = {}
    for line in open(
            os.path.join(currentPath, "utt2spk"), "rt",
            encoding="utf-8").readlines():
        line = line.strip()
        utt, spk = line.split(" ")
        utt = str(utt)
        spk = str(spk)
        utt2spkContext.update({utt: spk})
    # Done utt2spk dict make

    fileKeys = list(fileContext.keys())
    originCount = len(fileContext)
    outCount = int(originCount * percent)
    random.seed(seed)
    indexList = random.sample(range(1, originCount + 1), outCount)
    indexList.sort()  # 需要的索引列表

    saveName = "wav" + backffix + ".scp"
    write_output_file(savePath, saveName, indexList, fileKeys, fileContext)

    saveName = "utt2spk" + backffix
    write_output_file(savePath, saveName, indexList, fileKeys, utt2spkContext)

    saveName = "text" + backffix
    write_output_file(savePath, saveName, indexList, fileKeys, textContext)
    print("done!")
