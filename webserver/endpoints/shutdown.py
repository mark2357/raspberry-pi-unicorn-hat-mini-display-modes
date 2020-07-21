'''handles the /change-mode requests'''


import web

from shutdown_script import shutdown_script

class Shutdown:
    '''handles the requests for the /shutdown/ endpoint'''
    # pylint: disable=invalid-name
    def POST(self):
        '''handles post requests to the server'''
        print('starting server shutdown process')

        # shutsdown the LEDs
        # display_controller is added via a add_processor
        # pylint: disable=no-member
        if web.ctx.web_server_only_mode:
            print('starting server shutdown process')
        else:
            web.ctx.display_controller.stop()

        shutdown_script()
        web.header('Content-Type', 'text/plain')
        return web.OK()
