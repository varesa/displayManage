import logging
import os
import json
import urllib

from pyramid.response import Response
from pyramid.view import view_config

import vars

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

    devices = ['a', 'b', 'c', 'demo']
    pages = os.listdir(vars.imagespath)

    table = []
    table.append([''] + devices)

    for page in pages:
	temp = [urllib.url2pathname(page)]
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
    
@view_config(route_name='files', renderer='templates/filemanager.pt')
def files(request):
    dir = vars.imagespath
    files = os.listdir(dir)
    return {'files': files}


@view_config(route_name='upload')
def upload(request):
    files = request.POST.getall('file')
    for file in files:
        filename = file.filename
        filedata = file.file

        #filename = filename.split("/")[-1] # Remove ../'s and other nasty things
        filename = urllib.pathname2url(filename)
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

    files = os.listdir(vars.imagespath)
    list = []
    
    for page in pages:
	for file in files:
	    if page == encode2css(file):
		list.append(vars.imagesurl + urllib.pathname2url(file)) # Encode the encoded filename, to pass the %-characters to the server
    list = '\n'.join(list) + '\n'
    return Response(list)