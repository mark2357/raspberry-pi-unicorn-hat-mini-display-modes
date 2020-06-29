

import time
from unicornhatmini import UnicornHATMini
from gpiozero import Button

# from shutdown_script import shutdown_script
from helpers.get_config import get_config
from modes.clock_mode import ClockMode
from modes.numbers_fact_text_mode import NumbersFactTextMode
from modes.poke_random_info_text_mode import PokeRandomInfoTextMode


class DisplayController:
    def __init__(self):
        self.mode_index = 2
        self.MIN_MODE = 0
        self.MAX_MODE = 2
        self.mode = None
        self.unicornhatmini = UnicornHATMini()
        self.config = get_config()

    def mode_increment(self):
        '''used to go to the next mode'''
        self.mode_index += 1
        if self.mode_index > self.MAX_MODE:
            self.mode_index = self.MIN_MODE
        self.update_mode()


    def mode_decrement(self):
        '''used to go to the next previous'''
        self.mode_index -= 1
        if self.mode_index < self.MIN_MODE:
            self.mode_index = self.MAX_MODE
        self.update_mode()


    def update_mode(self):
        if self.mode_index == 0:
            self.mode = ClockMode(self.unicornhatmini, self.config)
        elif self.mode_index == 1:
            self.mode = NumbersFactTextMode(self.unicornhatmini, self.config)
        elif self.mode_index == 2:
            self.mode = PokeRandomInfoTextMode(self.unicornhatmini, self.config)
            


    def pressed(self, button):
        # print(button.pin.number)
        if button.pin.number is 5:
            self.mode_increment()
            
        # if button.pin.number is 6:
        
        if button.pin.number is 16:
            self.mode_decrement()
        
        # if button.pin.number is 24:
            # clears leds before shuting down system
            # unicornhatmini.clear()
            # shutdown_script()


    def run(self):
        button_a = Button(5)
        button_b = Button(6)
        button_x = Button(16)
        button_y = Button(24)

        self.unicornhatmini.set_brightness(float(self.config['GENERAL']['BRIGHTNESS']))
        self.unicornhatmini.set_rotation(int(self.config['GENERAL']['ROTATION']))
        self.update_mode()

        try:
            button_a.when_pressed = self.pressed
            button_b.when_pressed = self.pressed
            button_x.when_pressed = self.pressed
            button_y.when_pressed = self.pressed

            frame_interval = 1.0 / float(self.config['GENERAL']['FPS'])

            while True:
                start_time = time.time()
                self.mode.display_frame()
                end_time = time.time()
                if end_time - start_time < frame_interval:
                    time.sleep(frame_interval - (end_time - start_time))

        except KeyboardInterrupt:
            button_a.close()
            button_b.close()
            button_x.close()
            button_y.close()
