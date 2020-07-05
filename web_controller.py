'''contains custom webserver class'''
import web
from web.httpserver import StaticMiddleware

class WebController(web.application):
    '''custom web controller class that uses /webserver/static for static files and port 80'''

    # pylint: disable=arguments-differ
    def run(self, port=8080):
        '''starts web server'''
        # 'lambda app: StaticMiddleware(app, '/webserver/')' is used to allow static files to be hosted from within the webserver folder
        func = self.wsgifunc(lambda app: StaticMiddleware(app, '/webserver/'))
        return web.httpserver.runsimple(func, ('0.0.0.0', port))
