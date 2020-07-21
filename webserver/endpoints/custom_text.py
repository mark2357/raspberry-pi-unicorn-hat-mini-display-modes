'''handles the /change-mode requests'''

import json
import string

import web

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
                    elif index != 0 and char not in string.hexdigits:
                        color_valid = False

                if color_valid is False:
                    print(f'custom color {custom_color} is not valid')
                    return web.BadRequest()

                print(f'changing to : custom mode setting custom text to {custom_text}')

                if isinstance(custom_text, str) and isinstance(custom_color, str):
                    # display_controller is added via a add_processor
                    # pylint: disable=no-member

                    if web.ctx.web_server_only_mode:
                        print(f'changed to custom text mode with custom text: {custom_text} with custom color: {custom_color}')
                    else:
                        web.ctx.display_controller.set_mode('custom_text_mode', {'custom_text': custom_text, 'custom_color': custom_color})




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
