import os

# Paths

basepath = "/displaymanage/"

datapath = os.path.join(basepath, "data")

matrixpath = os.path.join(datapath, "matrix.json")
devicespath = os.path.join(datapath, "devices.json")

logpath = os.path.join(basepath, "logs/")

# S3

imagesbucket = "nastorimedia"
imagesurl = "s3://" + imagesbucket + "/"

s3authfile = os.path.join(datapath, "s3credentials.conf")