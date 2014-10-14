from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)

    # Image - deice selection
    config.add_route('matrix', '/')

    # Image upload/management
    config.add_route('files', '/files/')
    config.add_route('upload', '/upload/')

    # Endpoint for device queries
    config.add_route('get_pages', '/get_pages/')

    config.scan()
    return config.make_wsgi_app()
