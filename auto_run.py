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
        # return "Hello, world!"
        return render.index()

    def POST(self):
        global display_controller
        data = web.data() # you can get data use this method
        json_data = json.loads(data)
        print(json_data['mode'])
        display_controller.set_mode(json_data['mode'])
        raise web.seeother('/')


def run_display():
    global display_controller
    display_controller.run()


if __name__ == "__main__":
    try:
        print(f'__name__ is: {__name__}')
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
        print('p1.join() finished')
