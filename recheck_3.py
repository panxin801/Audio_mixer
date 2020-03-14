import os
import sys
import random

if __name__ == "__main__":
    currentPath = r"/home/panxin/kaldi/egs/aishell2_kefu/s5/data/train"
    savePath = r"/home/panxin/kaldi/egs/aishell2_kefu/s5/data"

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
        for line in open(tmpRead, "rt").readlines():
            line = line.strip()
            uttid, spkid = line.split(" ")
            if uttid in textContext.keys():
                f.write("%s %s\n" % (uttid, spkid))
    tmpSave = os.path.join(currentPath, "wav.scp_new")
    tmpRead = os.path.join(currentPath, "wav.scp")
    with open(tmpSave, "wt", encoding="utf-8") as f:
        for line in open(tmpRead, "rt").readlines():
            line = line.strip()
            uttid, path = line.split(" ")
            if uttid in textContext.keys():
                f.write("%s %s\n" % (uttid, path))

    if empty:
        print("Blank line occurs!!!")
        sys.exit(1)

    print("done!")
