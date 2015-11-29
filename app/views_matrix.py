import logging
import urllib

from pyramid.view import view_config

from app.devicesWrapper import DevicesWrapper
from app.matrixWrapper import MatrixWrapper
from app import vars
from app.s3_connection import get_s3_connection


log = logging.getLogger(__name__)


def encode2css(s):
    s = s.replace('%', '')
    s = s.replace('.', '')
    return s


@view_config(route_name='matrix', renderer='templates/matrix.pt')
def matrix(request):
    newdata = {}
    for pair in request.POST.items():
        key = pair[0]
        """:type : str"""
        val = pair[1]
        """:type : str"""

        if val.startswith("cb_"):
            val = val.split('cb_')[1]
            device, page = val.split("-_-")
            if device not in newdata.keys():
                newdata[device] = []
            newdata[device].append(page)

    if len(newdata):
        MatrixWrapper().write(newdata)
    else:
        newdata = MatrixWrapper().get()

    devices = DevicesWrapper().get()
    
    bucket = get_s3_connection().get_bucket(vars.imagesbucket)
    
    pages = [key.key for key in bucket.list()]

    table = list()
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
