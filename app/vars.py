import os
import sys

# Paths

basepath = "/displaymanage/"
if not os.path.isdir(basepath):
    print("Not installed in " + basepath)
    sys.exit(1)

datapath = os.path.join(basepath, "data")
if not os.path.isdir(datapath):
    os.mkdir(datapath)

matrixpath = os.path.join(datapath, "matrix.json")
devicespath = os.path.join(datapath, "devices.json")

logpath = os.path.join(basepath, "logs/")
if not os.path.isdir(logpath):
    os.mkdir(logpath)

# S3

imagesbucket = "nastorimedia"
imagesurl = "s3://" + imagesbucket + "/"

s3authfile = os.path.join(datapath, "s3credentials.conf")
