

from helpers.text_display import TextDisplay
from helpers.get_text_width import get_text_width


class ScrollingTextBaseMode:
    def __init__(self, unicornhatmini, config):
        self.unicornhatmini = unicornhatmini
        self.config = config
        self.offset_x = 0
        self.current_text = ''
        self.current_text_length = 0
        self.color_r = 50
        self.color_g = 100
        self.color_b = 120
        self.text_display = TextDisplay(unicornhatmini, self.current_text)

        self.update_current_text()


    def display_frame(self):
        '''displays new frame of text on screen'''
        self.offset_x += 1

        if self.offset_x > self.current_text_length:
            self.offset_x = 0
            self.update_current_text()

        self.text_display.display_text(self.offset_x, self.color_r, self.color_g, self.color_b)


    def update_current_text(self):
        '''should be overridden by child classes'''
        raise NotImplementedError()


    def set_current_text(self, new_current_text):
        '''should be called by child classes to correctly set the current text (WARNING do not set text by assigning variable)'''
        self.current_text = new_current_text
        self.current_text_length = get_text_width(self.unicornhatmini, self.current_text)
        self.text_display.update_text(self.current_text)
