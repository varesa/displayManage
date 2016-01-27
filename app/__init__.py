from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('logs', '../logs')

    # Image - device selection
    config.add_route('matrix', '/')

    # Device management
    config.add_route('devices', '/devices/')

    # Image upload/management
    config.add_route('files', '/files/')
    config.add_route('upload', '/upload/')

    # Endpoint for device queries
    config.add_route('get_pages', '/get_pages/')

    config.scan()
    return config.make_wsgi_app()
