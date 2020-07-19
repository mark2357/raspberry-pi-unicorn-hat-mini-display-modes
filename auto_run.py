#!/usr/bin/env python3
'''script that should be run to start the program/script'''



import threading
import json
import os
import string

import web

from display_controller import DisplayController
from web_controller import WebController
from shutdown_script import shutdown_script
from helpers.get_project_path import get_project_path
from get_mode_data import get_mode_data

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
            modes_data = get_mode_data()

            custom_text_mode_enabled = modes_data['custom_text_mode']['enabled']
            # removes custom text mode as it's displayed differently
            modes_data.pop('custom_text_mode')

            current_mode_id = display_controller.mode_id
            return render.index(modes_data, custom_text_mode_enabled, current_mode_id)
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
                mode = json_data['mode']
                print(f'new mode selected with id: {mode}')
                global display_controller

                display_controller.set_mode(mode)

                # returns the mode that was sent (in full system this will send the new mode)
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Content-Type', 'application/json')
                return '{"mode": "' + mode + '"}'

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


class CustomText:
    '''handles the requests for the /custom-text/ endpoint'''

    # pylint: disable=invalid-name
    def POST(self):
        '''handles post requests to the server'''
        try:
            # gets post data
            data = web.data()
            # tries to convert data to json (error handled below)
            json_data = json.loads(data)

            # makes sure custom-text is in the json data
            if 'custom-text' in json_data and 'custom-color' in json_data:
                custom_text = str(json_data['custom-text'])
                custom_color = str(json_data['custom-color'])

                color_valid = True
                # validates color string
                if len(custom_color) != 7:
                    color_valid = False
                for x in range(0, len(custom_color)):
                    if x == 0 and custom_color[x] != '#':
                        color_valid = False
                        print('no hash at start')
                    elif x != 0 and custom_color[x] not in string.hexdigits:
                        color_valid = False
                        print(f'digit {x} is not valid')

                if color_valid is False:
                    print(f'custom color {custom_color} is not valid')
                    return web.BadRequest()

                print(f'changing to : custom mode setting custom text to {custom_text}')
                global display_controller

                if isinstance(custom_text, str) and isinstance(custom_color, str):
                    display_controller.set_mode('custom_text_mode', {'custom_text': custom_text, 'custom_color': custom_color})

                # returns the mode that was sent (in full system this will send the new mode)
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Content-Type', 'application/json')
                return "{\"mode\": 7}"

            else:
                print('post request doesn\'t contain custom text to display')
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
        '/custom-text/', 'CustomText',
        '/shutdown/', 'Shutdown',

    )

    app = WebController(urls, globals())
    app.run()

    # is only run after keyboard interrupt is pressed
    display_controller.stop()
    p1.join()
    print('finished waiting for display controller thread to stop')
    print('finished running auto run script')
