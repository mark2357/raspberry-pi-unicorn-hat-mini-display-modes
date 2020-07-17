'''contains class that is used to display custom text'''

from PIL import ImageColor
from modes.scrolling_text_base_mode import ScrollingTextBaseMode

class CustomTextMode(ScrollingTextBaseMode):
    '''class used to display custom text on led display'''

    def __init__(self, unicornhatmini, config, custom_options=None):
        if custom_options is None:
            self.custom_text = 'insert custom text here'
        else:
            self.custom_text = custom_options['custom_text']

        super().__init__(unicornhatmini, config, custom_options)
        if custom_options is None:
            self.set_rgb(255, 255, 255)
        else:
            color = ImageColor.getcolor(custom_options['custom_color'], "RGB")
            self.set_rgb(color[0], color[1], color[2])


    def update_current_text(self):
        '''updates the current text with the current custom text'''
        self.set_current_text(self.custom_text)
