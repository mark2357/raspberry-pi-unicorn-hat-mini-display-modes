#!/usr/bin/env python3
'''script that should be run to start the program/script'''



import threading
import os

import web

from display_controller import DisplayController
from web_controller import WebController
from helpers.get_project_path import get_project_path

# hides incorrect pylint errors
# pylint: disable=unused-import
from webserver.endpoints.index import Index
from webserver.endpoints.change_mode import ChangeMode
from webserver.endpoints.custom_text import CustomText
from webserver.endpoints.shutdown import Shutdown


# sets working directory to folder of the project
os.chdir(get_project_path())


def add_variables(handler):
    '''adds the display controller and web server only mode to the context alowing it to be accessed by the '''
    web.ctx.display_controller = display_controller
    # when set to true the endpoints don't interact with the display controller as it's not running
    web.ctx.web_server_only_mode = False
    return handler()


def run_display(dc):
    '''function that runs the display controller, should be run on a different thread'''
    dc.run()

if __name__ == "__main__":
    print('creating display controller')
    display_controller = DisplayController()

    p1 = threading.Thread(target=run_display, kwargs={'dc': display_controller})
    print('starting display controller thread')
    p1.start()
    print('finished starting display controller thread')

    print('starting webserver')
    # render = web.template.render(os.path.join(get_project_path(), 'webserver/templates/'))
    render = web.template.render('webserver/templates/')

    urls = (
        '/', 'Index',
        '/change-mode/', 'ChangeMode',
        '/custom-text/', 'CustomText',
        '/shutdown/', 'Shutdown',

    )

    app = WebController(urls, globals())
    app.add_processor(add_variables)
    app.run()

    # is only run after keyboard interrupt is pressed
    display_controller.stop()
    p1.join()
    print('finished waiting for display controller thread to stop')
    print('finished running auto run script')
