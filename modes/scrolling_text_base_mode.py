'''contains base class that is used to display scrolling text'''


from helpers.text_display import TextDisplay
from helpers.get_text_width import get_text_width
from modes.base_mode import BaseMode

class ScrollingTextBaseMode(BaseMode):
    '''a base class for displaying scrolling text'''

    def __init__(self, unicornhatmini, config):
        super().__init__(unicornhatmini, config)
        self.offset_x = 0
        self.current_text = ''
        self.current_text_length = 0
        self.color_r = 255
        self.color_g = 255
        self.color_b = 255
        self.text_display = TextDisplay(unicornhatmini, self.current_text)
        self.mode_config_name = 'SCROLLING_TEXT_BASE_MODE'

        self.update_current_text()


    def display_frame(self):
        '''displays new frame of text on screen'''
        self.offset_x += 1

        if self.offset_x > self.current_text_length:
            self.offset_x = 0
            self.update_current_text()

        self.text_display.display_text(self.offset_x, self.color_r, self.color_g, self.color_b)

        return self.config.getint(self.mode_config_name, 'FPS', fallback=30)


    def update_current_text(self):
        '''should be overridden by child classes'''
        raise NotImplementedError()


    def set_current_text(self, new_current_text):
        '''should be called by child classes to correctly set the current text (WARNING do not set text by assigning variable)'''
        self.current_text = new_current_text
        self.current_text_length = get_text_width(self.unicornhatmini, self.current_text)
        self.text_display.update_text(self.current_text)

    def set_rgb(self, r_color, g_color, b_color):
        'sets the rgb color of the text'
        self.color_r = r_color
        self.color_g = g_color
        self.color_b = b_color
