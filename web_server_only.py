#!/usr/bin/env python3
'''script that only runs the webserver and not the display controller'''


import json
import web

from web_controller import WebController

# defines class used for handling webserver requests
class Index:
    '''class used for handling web requests'''

    # pylint: disable=invalid-name
    def GET(self):
        '''handles get requests to the server'''
        try:
            mode_names = ['Clock', 'Numbers Facts', 'Random Pokemon Info', 'Covid 19 New Cases', 'Pixel Rain']
            current_mode_index = 0
            return render.index(mode_names, current_mode_index)
        except:
            print('internal server error')
            return web.InternalError()


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


if __name__ == "__main__":
    try:
        print('starting webserver')

        render = web.template.render('webserver/templates/')

        urls = (
            '/', 'Index',
        )

        app = WebController(urls, globals())
        app.run()

    except KeyboardInterrupt:
        print('KeyboardInterrupt')
