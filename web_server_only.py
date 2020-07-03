#!/usr/bin/env python3
'''script that only runs the webserver and not the display controller'''


import web
from web.httpserver import StaticMiddleware
import threading
import json


# defines class used for handling webserver requests
class index:
    def GET(self):
        # return "Hello, world!"
        mode_names = ['Clock', 'Numbers Facts', 'Random Pokemon Info', 'Covid 19 New Cases', 'Pixel Rain']
        return render.index(mode_names)

    def POST(self):
        data = web.data() # you can get data use this method
        json_data = json.loads(data)
        print(json_data['mode'])
        
        # returns the mode that was sent (in full system this will send the new mode)
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Content-Type', 'application/json')
        return "{\"mode\": " + str(json_data['mode']) + "}"


if __name__ == "__main__":
    try:
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
