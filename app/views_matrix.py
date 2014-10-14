import logging
import os
import json
import urllib

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from . import vars

log = logging.getLogger(__name__)


def encode2css(s):
    s = s.replace('%', '')
    s = s.replace('.', '')
    return s


@view_config(route_name='matrix', renderer='templates/matrix.pt')
def matrix(request):
    newdata = {}
    for pair in request.POST.items():
        log.debug(pair)
        key = pair[0]
        """:type : str"""
        val = pair[1]
        """:type : str"""

        if val.startswith("cb_"):
            val = val.split('cb_')[1]
            device, page = val.split("-_-")
            if not device in newdata.keys():
                newdata[device] = []
            newdata[device].append(page)

            log.debug(device + ": " + page)

    if not len(newdata) == 0:
        matrixfile = open(vars.matrixpath, "w")
        json.dump(newdata, matrixfile)
        matrixfile.close()
    else:
        matrixfile = open(vars.matrixpath, "r")
        newdata = json.load(matrixfile)
        matrixfile.close()

    devices = ['kirkko', 'paju', 'liike', 'kauppa', 'demo', 'test']
    pages = os.listdir(vars.imagespath)

    table = []
    table.append([''] + devices)

    for page in pages:
        temp = [urllib.request.url2pathname(page)]
        page = encode2css(page)
        for device in devices:
            extra_classes = ''
            if device in newdata.keys():
                if page.replace('.', '') in newdata[device]:
                    extra_classes += ' checked'
            temp.append([device + "-_-" + page, extra_classes])
        table.append(temp)

    logging.debug(table)

    return {'table': table}