import logging
import os
import json
import urllib
import datetime
import calendar

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from . import vars
from .s3_connection import get_s3_connection

log = logging.getLogger(__name__)


def encode2css(s):
    s = s.replace('%', '')
    s = s.replace('.', '')
    return s


def log_connection(name):
    now = datetime.datetime.utcnow()

    date = now.isocalendar()
    year = date[0]
    week = date[1]

    time = calendar.timegm(now.timetuple())

    filename = os.path.join(vars.logpath, str(year) + "-" + str(week)+".log")
    file = open(filename, 'a')
    file.write(name + ": " + str(time) + "\n")


@view_config(route_name='get_pages')
def get_pages(request):
    if 'device' not in request.GET.keys():
        return Response('ERR_DeviceNotSpecified')

    matrixfile = open(vars.matrixpath, 'r')
    matrix = json.load(matrixfile)
    matrixfile.close()

    if request.GET['device'] not in matrix.keys():
        return Response('ERR_DeviceNotFound')

    device = request.GET['device']
    pages = matrix[device]


    bucket = get_s3_connection().get_bucket(vars.imagesbucket)
    files = [key.key for key in bucket.list()]
    
    list = []

    for page in pages:
        for file in files:
            if page == encode2css(file):
                list.append(vars.imagesurl + file)
    list.sort()
    list = '\n'.join(list) + '\n'

    log_connection(device)
    return Response(list)

