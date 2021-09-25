#`# Randomly pick 8 samples from each test case group in "./kplib"
import os, random

def rmdir(path):
    if (not os.path.isdir(path)): return

    fl = os.listdir(path)
    for i in fl:
        subPath = path + "/" + i
        if (os.path.isdir(subPath)):
            rmdir(subPath)
            continue
        os.remove(subPath)

    os.rmdir(path)


srcPath = "./kplib" # test cases folder
destPath = "./picked_test_cases" # picked test cases folder

RGroup = "R10000" # or "R10000"

rmdir(destPath) # remove old test_cases folder
os.mkdir(destPath)

for i in os.listdir(srcPath):
    os.mkdir(destPath + "/" + i)
    for j in os.listdir(srcPath + "/" + i):
        srcTestCase = os.listdir(srcPath + "/" + i + "/" + j + "/" + RGroup)
        os.rename(srcPath + "/" + i + "/" + j + "/" + RGroup + "/" + srcTestCase[random.randint(0, len(srcTestCase) - 1)], destPath + "/" + i + "/" + j + ".kp")
