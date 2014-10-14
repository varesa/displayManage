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


def write_to_file(filepath, file_contents):
    tmp_filepath = filepath + '~'

    fout = open(tmp_filepath, 'w')
    file_contents.seek(0)
    while True:
        data = file_contents.read(2 << 16)
        if not data:
            break
        fout.write(data)

    fout.close()
    os.rename(tmp_filepath, filepath)


ERR_INVALID_FILENAME = "Virheellinen tiedostonimi."


@view_config(route_name='upload')
def upload(request):
    POSTfiles = request.POST.getall('file')
    for file in POSTfiles:
        filename = file.filename
        file_contents = file.file

        filename = filename.split("/")[-1] # Remove ../'s and other nasty things
        filename = urllib.request.pathname2url(filename)

        if len(filename) == 0:
            return Response(ERR_INVALID_FILENAME)

        file_path = os.path.join(vars.imagespath, filename)
        write_to_file(file_path, file_contents)

    return Response('OK')