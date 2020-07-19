#!/usr/bin/env python3
'''script that only runs the webserver and not the display controller'''


import json
import string

import web

from web_controller import WebController
from get_mode_data import get_mode_data
# defines class used for handling webserver requests
class Index:
    '''handles the requests for the / endpoint'''

    # pylint: disable=invalid-name
    def GET(self):
        '''handles get requests to the server'''
        try:
            modes_data = get_mode_data()

            custom_text_mode_enabled = modes_data['custom_text_mode']['enabled']

            current_mode_id = 'clock_mode'
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
                mode = int(json_data['mode'])
                print(f'new mode selected with index: {mode}')

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
                for index, char in enumerate(custom_color):
                    if index == 0 and char != '#':
                        color_valid = False
                        print('no hash at start')
                    elif index != 0 and char not in string.hexdigits:
                        color_valid = False
                        print(f'digit {index} is not valid')

                if color_valid is False:
                    print(f'custom color {custom_color} is not valid')
                    return web.BadRequest()


                print(f'changing to : custom mode setting custom text to {custom_text} and custom color to {custom_color}')
                # returns the mode that was sent (in full system this will send the new mode)
                web.header('Access-Control-Allow-Origin', '*')
                web.header('Content-Type', 'application/json')
                return "{\"custom-text\": " + custom_text + ", \"custom-color\": " + custom_color + " }"

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
        web.header('Content-Type', 'text/plain')
        return web.OK()

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
        app.run()

    except KeyboardInterrupt:
        print('KeyboardInterrupt')
