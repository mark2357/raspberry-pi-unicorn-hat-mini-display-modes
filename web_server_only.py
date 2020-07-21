#!/usr/bin/env python3
'''script that only runs the webserver and not the display controller used for easier development of webpage'''


import web

from web_controller import WebController

# hides incorrect pylint errors
# pylint: disable=unused-import
from webserver.endpoints.index import Index
from webserver.endpoints.change_mode import ChangeMode
from webserver.endpoints.custom_text import CustomText
from webserver.endpoints.shutdown import Shutdown


def add_variables(handler):
    '''adds the display controller and web server only mode to the context alowing it to be accessed by the '''

    # when set to true the endpoints don't interact with the display controller as it's not running
    web.ctx.web_server_only_mode = True
    return handler()


if __name__ == "__main__":
    try:
        print('starting webserver')

        render = web.template.render('webserver/templates/')

        urls = (
            '/', 'Index',
            '/change-mode/', 'ChangeMode',
            '/custom-text/', 'CustomText',
            '/shutdown/', 'Shutdown'
        )

        app = WebController(urls, globals())
        app.add_processor(add_variables)
        app.run()

    except KeyboardInterrupt:
        print('KeyboardInterrupt')
