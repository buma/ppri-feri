from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from deform_bootstrap import includeme

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # session factory
    session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    config = Configurator(settings=settings, session_factory=session_factory)
    includeme(config)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('deform_static', 'deform:static')
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
