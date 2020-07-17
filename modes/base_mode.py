'''contains class BaseMode that is used as a base for all other modes'''

class BaseMode:
    '''base mode that all other modes extend'''
    # pylint: disable=unused-argument
    def __init__(self, unicornhatmini, config, custom_options=None):
        self.unicornhatmini = unicornhatmini
        self.config = config


    def display_frame(self):
        '''base mode called by display controller to render each frame of mode should return the time to wait until the next frame'''
        return 30
