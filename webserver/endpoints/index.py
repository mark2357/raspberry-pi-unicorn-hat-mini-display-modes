'''handles the /index requests'''
import web

from get_mode_data import get_mode_data

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

            # display_controller and web_server_only_mode is added via a add_processor
            # pylint: disable=no-member
            if web.ctx.web_server_only_mode:
                current_mode_id = 'clock_mode'
            else:
                current_mode_id = web.ctx.display_controller.mode_id

            render = web.template.render('webserver/templates/')

            return render.index(modes_data, custom_text_mode_enabled, current_mode_id)
        except:
            print('internal server error')
            return web.InternalError()
