'''contains class used to controll switching between differerent display modes'''

import time
from unicornhatmini import UnicornHATMini

# from shutdown_script import shutdown_script
from helpers.get_config import get_config
from get_mode_data import get_mode_data, get_valid_mode_ids


class DisplayController:
    '''used to controll switching between the different dispaly modes'''
    def __init__(self):
        self.modes_data = get_mode_data()
        self.mode = None
        self.unicornhatmini = UnicornHATMini()
        self.config = get_config()
        mode_id = self.config.get('GENERAL', 'INITIAL_MODE_ID', fallback='clock_mode')
        if mode_id not in get_valid_mode_ids():
            print(f'initial mode id of {mode_id} is not a valid, clock_mode is being used instead')
            mode_id = 'clock_mode'


        self.mode_id = mode_id
        self.mode_update_needed = False
        self.running = False
        self.mode_custom_options = None


    def set_mode(self, new_mode_id, custom_options=None):
        '''sets the current mode'''

        if new_mode_id not in get_valid_mode_ids():
            print(f'cannot change to mode with id: {new_mode_id} as it is invalid or disabled')
            return


        self.mode_id = new_mode_id
        self.mode_custom_options = custom_options
        self.mode_update_needed = True
        print(f'self.mode_update_needed: {self.mode_update_needed}')


    def update_mode(self):
        '''updates the current mode by instancating new mode instance'''

        # only passes custom options if it's not None
        if self.mode_custom_options is None:
            self.mode = self.modes_data[self.mode_id]['class_constructor'](self.unicornhatmini, self.config)
        else:
            self.mode = self.modes_data[self.mode_id]['class_constructor'](self.unicornhatmini, self.config, self.mode_custom_options)
        self.mode_update_needed = False


    def run(self):
        '''used to start running the led display'''
        self.unicornhatmini.set_brightness(self.config.getfloat('GENERAL', 'BRIGHTNESS', fallback=0.1))
        self.unicornhatmini.set_rotation(self.config.getint('GENERAL', 'ROTATION', fallback=0))
        self.update_mode()
        self.running = True

        frame_interval = 1.0 / 30

        while self.running:
            start_time = time.time()

            frame_interval = 1.0 / self.mode.display_frame()

            end_time = time.time()
            if end_time - start_time < frame_interval:
                time.sleep(frame_interval - (end_time - start_time))

            if self.mode_update_needed is True:
                self.update_mode()


        if not self.running:
            print('display controller shutting down')
            self.unicornhatmini.clear()
            self.unicornhatmini.show()


    def stop(self):
        '''used to stop execution of the display controller'''
        self.running = False
