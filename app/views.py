import logging
import os

from pyramid.response import Response
from pyramid.view import view_config

import vars

log = logging.getLogger(__name__)

"""
@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'app'}
"""

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

    devices = ['pi1', 'pi2', 'kmarket', 'tori']
    #pages = ['ad1', 'ad2', 'nastori', 'other']
    """pages = []
    log.debug(pages)
    for page in os.listdir(vars.imagespath):
        new = page.replace('.', '')
        pages.append(new)
    log.debug(pages)"""
    pages = os.listdir(vars.imagespath)

    table = []
    table.append([''] + devices)

    log.debug(newdata)

    for page in pages:
        temp = [page]
        for device in devices:
            extra_classes = ''
            if device in newdata.keys():
        	log.debug('Device found: ' +device)
                if page in newdata[device]:
            	    log.debug('Page ' + page + ' checked for device')
                    extra_classes += ' checked'
            temp.append([device + "-_-" + page, extra_classes])
        table.append(temp)

    logging.debug(table)

    #return {'table': [['a', 'b'], ['c', 'd'], ['e', 'f']]}
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

        filename = filename.split("/")[-1] # Remove ../'s and other nasty things
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