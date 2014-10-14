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

log = logging.getLogger(__name__)


@view_config(route_name='files', renderer='templates/filemanager.pt')
def files(request):
    if 'action' in request.GET.keys() and request.GET['action'] == 'delete':
        for key in request.GET.keys():
            if(key.startswith('remove_')):
                os.remove(vars.imagespath + key[7:])
        return HTTPFound(location=request.application_url + "/files/")
    return {'files': os.listdir(vars.imagespath)}


@view_config(route_name='upload')
def upload(request):
    files = request.POST.getall('file')
    for file in files:
        filename = file.filename
        filedata = file.file

        #filename = filename.split("/")[-1] # Remove ../'s and other nasty things
        filename = urllib.request.pathname2url(filename)
        if len(filename) == 0:
            return Response('Invalid filename')

        tmp_filename = filename + '~'
        fout = open(os.path.join(vars.imagespath, tmp_filename), 'w')

        filedata.seek(0)
        while True:
            data = filedata.read(2<<16)
            if not data:
                break
            fout.write(data)

        fout.close()
        os.rename(os.path.join(vars.imagespath, tmp_filename), os.path.join(vars.imagespath, filename))

    return Response('OK')
