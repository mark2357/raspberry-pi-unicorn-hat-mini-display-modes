#!/usr/bin/env python3
'''script that should be run to start the program/script'''


from display_controller import DisplayController

import web
from web.httpserver import StaticMiddleware
import threading
import json


# defines class used for handling webserver requests
class index:
    def GET(self):
        try:
            mode_names = ['Clock', 'Numbers Facts', 'Random Pokemon Info', 'Covid 19 New Cases', 'Pixel Rain']
            current_mode_index = 0
            return render.index(mode_names, current_mode_index)
        except:
            print('internal server error')
            return web.InternalError()

    def POST(self):
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
                print(f'post request doesn\'t contain new mode')
                return web.BadRequest()
        except ValueError:
            # catches error from json.loads
            print('data from post request is not valid json')
            return web.BadRequest()
        except:
            print('internal server error')
            return web.InternalError()



def run_display():
    '''function that runs the display controller, should be run on a different thread'''
    global display_controller
    display_controller.run()


if __name__ == "__main__":
    try:
        print('creating display controller')
        display_controller = DisplayController()

        p1 = threading.Thread(target = run_display)
        print('starting display controller thread')
        p1.start()
        print('finished starting display controller thread')


        print('starting webserver')
        render = web.template.render('webserver/templates/')

        urls = (
            '/', 'index',
        )

        app = web.application(urls, globals())
        # 'lambda app: StaticMiddleware(app, '/webserver/')' is used to allow static files to be hosted from within the webserver folder
        app.run(lambda app: StaticMiddleware(app, '/webserver/'))

    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        display_controller.stop()
        p1.join()
        print('finished waiting for display controller thread to stop')
