from pyramid.view import view_config

"""
@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'app'}
"""

@view_config(route_name='matrix', renderer='templates/matrix.pt')
def matrix(request):
    devices = ['pi1', 'pi2', 'kmarket', 'tori']
    pages = ['ad1', 'ad2', 'nastori', 'other']

    table = []
    table.append([''] + devices)

    for page in pages:
        temp = [page]
        for device in devices:
            temp.append("<" + device + "|" + page + ">")
        table.append(temp)

    #return {'table': [['a', 'b'], ['c', 'd'], ['e', 'f']]}
    return {'table': table}
    
@view_config(route_name='files', renderer='templates/filemanager.pt')
def files(request):
    return {'files': ['kuva1.jpg', 'kuva2.jpg', 'mainos3.jpg',]}