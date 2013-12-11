import logging
log = logging.getLogger(__name__)

from pyramid.view import view_config

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
    pages = ['ad1', 'ad2', 'nastori', 'other']

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
    return {'files': ['kuva1.jpg', 'kuva2.jpg', 'mainos3.jpg',]}