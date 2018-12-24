from pyramid.config import Configurator
from pyramid.view import exception_view_config
from pyramid.response import Response

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings) 
    config.include('pyramid_mako')
    config.include('.routes')
    config.add_exception_view(error_view)
    config.scan()
    return config.make_wsgi_app()

@exception_view_config(ValueError, renderer='templates/404.mako')
def error_view(request):
    return {'error':'Please check that your excel sheet has correct header, time and date format as mentioned on main page'}