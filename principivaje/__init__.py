from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from deform_bootstrap import includeme

from .util import get_extensions


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # session factory
    session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    config = Configurator(settings=settings, session_factory=session_factory)
    config.set_request_property(get_extensions, name="ext")
    includeme(config)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('deform_static', 'deform:static')
    config.add_route('home', '/')
    config.add_route('mlp', '/mlp')
    config.add_route('delta', '/delta')
    config.add_route('changes', '/changes')
    config.scan()
    return config.make_wsgi_app()
