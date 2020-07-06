#!/usr/bin/env python3
'''script that should be run to start the program/script'''



import threading
import json
import os

import web

from display_controller import DisplayController
from web_controller import WebController
from shutdown_script import shutdown_script
from helpers.get_project_path import get_project_path

# pylint: disable=invalid-name
display_controller = None


# sets working directory to folder of the project
os.chdir(get_project_path())


# defines class used for handling webserver requests
class Index:
    '''class used for handling web requests'''

    # pylint: disable=invalid-name
    def GET(self):
        '''handles get requests to the server'''
        try:
            mode_names = ['Clock', 'Numbers Facts', 'Random Pokemon Info', 'Covid 19 New Cases', 'Pixel Rain']
            current_mode_index = display_controller.mode_index
            return render.index(mode_names, current_mode_index)
        except:
            print('internal server error')
            return web.InternalError()


class ChangeMode:
    '''handles the requests for the /change-mode/ endpoint'''

    # pylint: disable=invalid-name
    def POST(self):
        '''handles post requests to the server'''
        try:
            # gets post data
            data = web.data()
            # tries to convert data to json (error handled below)
            json_data = json.loads(data)

            mode = None
            # makes sure mode is in the json data
            if 'mode' in json_data:
                mode = int(json_data['mode'])
                print(f'new mode selected with index: {mode}')
                global display_controller

                if isinstance(mode, int):
                    display_controller.set_mode(mode)

                # returns the mode that was sent (in full system this will send the new mode)
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Content-Type', 'application/json')
                return "{\"mode\": " + str(mode) + "}"

            else:
                print('post request doesn\'t contain new mode')
                return web.BadRequest()
        except ValueError:
            # catches error from json.loads
            print('data from post request is not valid json')
            return web.BadRequest()
        except:
            print('internal server error')
            return web.InternalError()


class Shutdown:
    '''handles the requests for the /shutdown/ endpoint'''
    # pylint: disable=invalid-name
    def POST(self):
        '''handles post requests to the server'''
        print('starting server shutdown process')

        # shutsdown the LEDs
        global display_controller
        display_controller.stop()

        shutdown_script()
        web.header('Content-Type', 'text/plain')
        return web.OK()


def run_display():
    '''function that runs the display controller, should be run on a different thread'''
    global display_controller
    display_controller.run()


if __name__ == "__main__":
    print('creating display controller')
    display_controller = DisplayController()

    p1 = threading.Thread(target=run_display)
    print('starting display controller thread')
    p1.start()
    print('finished starting display controller thread')


    print('starting webserver')
    # render = web.template.render(os.path.join(get_project_path(), 'webserver/templates/'))
    render = web.template.render('webserver/templates/')

    urls = (
        '/', 'Index',
        '/change-mode/', 'ChangeMode',
        '/shutdown/', 'Shutdown'
    )

    app = WebController(urls, globals())
    app.run()

    # is only run after keyboard interrupt is pressed
    display_controller.stop()
    p1.join()
    print('finished waiting for display controller thread to stop')
    print('finished running auto run script')
