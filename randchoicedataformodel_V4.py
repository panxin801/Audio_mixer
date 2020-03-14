import os
import sys
import random

if __name__ == "__main__":
    currentPath = r"/data/ASR_Datasets/Dataset_px_yue/data/train_no_noise"
    savePath = r"/data/ASR_Datasets/Dataset_px_yue/data"

    percent = 0.15
    seed = 1235
    backffix = "_with_noise"

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
        except:
            empty = True
            print(line)
    # Done text dict make

    if empty:
        print("Blank line occurs!!!")
        sys.exit(1)

    readFilename = os.path.join(currentPath, "wav.scp")
    fileContext = {}
    for line in open(readFilename, "rt").readlines():
        line = line.strip()
        utt, path = line.split(" ")
        utt = str(utt)
        fileContext.update([(utt, path)])
    # Done wav dict make

    utt2spkContext = {}
    for line in open(
            os.path.join(currentPath, "utt2spk"), "rt",
            encoding="utf-8").readlines():
        line = line.strip()
        utt, spk = line.split(" ")
        utt = str(utt)
        spk = str(spk)
        utt2spkContext.update([(utt, spk)])
    # Done utt2spk dict make

    fileKeys = list(fileContext.keys())
    originCount = len(fileContext)
    outCount = int(originCount * percent)
    random.seed(seed)
    indexList = random.sample(range(1, originCount + 1), outCount)
    indexList.sort()  # 需要的索引列表

    saveName = "wav" + backffix + ".scp"
    with open(os.path.join(savePath, saveName), "wt", encoding="utf-8") as f:
        for i in indexList:
            key = fileKeys[i - 1]
            value = fileContext.get(key)
            f.write("%s %s\n" % (key, value))

    saveName = "utt2spk" + backffix
    with open(os.path.join(savePath, saveName), "wt", encoding="utf-8") as f:
        for i in indexList:
            key = fileKeys[i - 1]
            value = utt2spkContext.get(key)
            f.write("%s %s\n" % (key, value))

    saveName = "text" + backffix
    with open(os.path.join(savePath, saveName), "wt", encoding="utf-8") as f:
        for i in indexList:
            key = fileKeys[i - 1]
            value = textContext.get(key)
            f.write("%s %s\n" % (key, value))
    print("done!")
