import logging
import os
import urllib
import subprocess
import mimetypes

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from boto.s3.key import Key

from . import vars
from .s3_connection import get_s3_connection

log = logging.getLogger(__name__)


@view_config(route_name='files', renderer='templates/filemanager.pt')
def files(request):
    bucket = get_s3_connection().get_bucket(vars.imagesbucket)
    if 'action' in request.GET.keys() and request.GET['action'] == 'delete':
        for key in request.GET.keys():
            if(key.startswith('remove_')):
                filename = key[7:]
                s3key = Key(bucket)
                s3key.key = filename
                bucket.delete_key(s3key)
        return HTTPFound(location=request.application_url + "/files/")

    files = [obj.key for obj in bucket.list()]
    return {'files': files}


ERR_INVALID_FILENAME = "Virheellinen tiedostonimi."


@view_config(route_name='upload')
def upload(request):
    POSTfiles = request.POST.getall('file')
    bucket = get_s3_connection().get_bucket(vars.imagesbucket)

    for file in POSTfiles:
        filename = file.filename
        file_contents = file.file

        filename = filename.split("/")[-1] # Remove ../'s and other nasty things
        filename = urllib.request.pathname2url(filename)

        if len(filename) == 0:
            return Response(ERR_INVALID_FILENAME)

        content_type, encoding = mimetypes.guess_type(filename)
        content_type = content_type or 'application/octet-stream'

        headers = {'Content-Type': content_type}

        key = Key(bucket)
        key.key = filename
        key.set_contents_from_file(file_contents, headers=headers)

    return Response('OK')
