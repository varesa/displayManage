import os

basepath = "/var/www/python/displaymanage/"

imagespath = os.path.join(basepath, "data", "images/")
matrixpath = os.path.join(basepath, "data", "matrix.json")
logpath = os.path.join(basepath, "logs/")

imagesbucket = "nastorimedia"
imagesurl = "s3://" + imagesbucket