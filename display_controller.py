'''contains class used to controll switching between differerent display modes'''

import time
from unicornhatmini import UnicornHATMini
from gpiozero import Button
import random

# from shutdown_script import shutdown_script
from helpers.get_config import get_config
from modes.clock_mode import ClockMode
from modes.numbers_fact_text_mode import NumbersFactTextMode
from modes.poke_random_info_text_mode import PokeRandomInfoTextMode
from modes.covid_19_new_cases_text_mode import Covid19NewCasesTextMode
from modes.pixel_rain_mode import PixelRainMode



class DisplayController:
    '''used to controll switching between the different dispaly modes'''
    def __init__(self):
        self.modes = [ClockMode, NumbersFactTextMode, PokeRandomInfoTextMode, Covid19NewCasesTextMode, PixelRainMode]
        self.mode = None
        self.unicornhatmini = UnicornHATMini()
        self.config = get_config()
        self.mode_index = int(self.config['GENERAL']['INITIAL_MODE_INDEX'])
        self.mode_update_needed = False
        self.id = random.randrange(0, 100)
        print(f'DisplayController init {self.id}')

    def mode_increment(self):
        '''used to go to the next mode'''
        self.mode_index += 1
        if self.mode_index > self.get_max_mode_index():
            self.mode_index = 0
        self.mode_update_needed = True


    def mode_decrement(self):
        '''used to go to the next previous'''
        self.mode_index -= 1
        if self.mode_index < 0:
            self.mode_index = self.get_max_mode_index()
        self.mode_update_needed = True


    def set_mode(self, newMode):
        print(f'set_mode called {self.id}')
        self.mode_index = newMode
        if self.mode_index > self.get_max_mode_index():
            self.mode_index = 0
        
        elif self.mode_index < 0:
            self.mode_index = self.get_max_mode_index()

        self.mode_update_needed = True
        print(f'self.mode_update_needed: {self.mode_update_needed}')



    def update_mode(self):
        '''updates the current mode by instancating new mode instance'''
        if self.mode_index < 0 or self.mode_index > self.get_max_mode_index():
            print(f"error mode index is outside mode range it's value is {self.mode_index}")
            return

        self.mode = self.modes[self.mode_index](self.unicornhatmini, self.config)
        self.mode_update_needed = False


    def get_max_mode_index(self):
        '''returns the max value mode_index should be'''
        return len(self.modes) - 1


    def pressed(self, button):
        '''called when a button is pressed'''
        # print(button.pin.number)
        if button.pin.number is 5:
            self.mode_increment()

        # if button.pin.number is 6:

        if button.pin.number is 16:
            self.mode_decrement()

        # if button.pin.number is 24:
            # clears led colour before shuting down system
            # unicornhatmini.clear()
            # shutdown_script()


    def run(self):
        '''used to start running the led display'''
        # button_a = Button(5)
        # button_b = Button(6)
        # button_x = Button(16)
        # button_y = Button(24)

        self.unicornhatmini.set_brightness(float(self.config['GENERAL']['BRIGHTNESS']))
        self.unicornhatmini.set_rotation(int(self.config['GENERAL']['ROTATION']))
        self.update_mode()
        self.running = True
        try:
            # button_a.when_pressed = self.pressed
            # button_b.when_pressed = self.pressed
            # button_x.when_pressed = self.pressed
            # button_y.when_pressed = self.pressed

            frame_interval = 1.0 / float(self.config['GENERAL']['FPS'])

            while self.running:
                start_time = time.time()
                
                self.mode.display_frame()

                end_time = time.time()
                if end_time - start_time < frame_interval:
                    time.sleep(frame_interval - (end_time - start_time))

                if self.mode_update_needed == True:
                    self.update_mode()

                # print(f'self.mode_update_needed {self.mode_update_needed}, {self.mode_index}')


        except KeyboardInterrupt:
            print('KeyboardInterrupt')

            # button_a.close()
            # button_b.close()
            # button_x.close()
            # button_y.close()


    def stop(self):
        '''used to stop execution of the display controller'''
        self.running = False
