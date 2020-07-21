'''handles the /change-mode requests'''

import json
import web

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

                # display_controller is added via a add_processor
                # pylint: disable=no-member
                if not web.ctx.web_server_only_mode:
                    web.ctx.display_controller.set_mode(mode)

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
