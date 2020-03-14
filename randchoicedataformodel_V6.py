import os
import sys
import random

if __name__ == "__main__":
    currentPath = r"/home/panxin/kaldi/egs/aishell2_kefu/s5/data/train"
    savePath = r"/home/panxin/kaldi/egs/aishell2_kefu/s5/data"

    percent = 0.1
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

    # maybe this one is optional
    tmpSave = os.path.join(currentPath, "text_new")
    with open(tmpSave, "wt", encoding="utf-8") as f:
        for key in textContext.keys():
            f.write("%s %s\n" % (key, textContext.get(key)))

    tmpSave = os.path.join(currentPath, "utt2spk_new")
    tmpRead = os.path.join(currentPath, "utt2spk")
    with open(tmpSave, "wt") as f:
        for line in open(tmpRead, "wt").readlines():
            line = line.strip()
            uttid, spkid = line.split(" ")
        if uttid in textContext.keys():
            f.write("%s %s\n" % (uttid, spkid))
    tmpSave = os.path.join(currentPath, "wav.scp_new")
    tmpRead = os.path.join(currentPath, "wav.scp")
    with open(tmpSave, "wt", encoding="utf-8") as f:
        for line in open(tmpRead, "wt").readlines():
            line = line.strip()
            uttid, path = line.split(" ")
        if uttid in textContext.keys():
            f.write("%s %s\n" % (uttid, path))

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