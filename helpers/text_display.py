'''contains class used to display text on led grid/screen'''
# import sys

from PIL import Image, ImageDraw, ImageFont
# from unicornhatmini import UnicornHATMini

class TextDisplay:
    '''used to easily display text on grid/screen'''
    def __init__(self, unicornhatmini, text):
        self.unicornhatmini = unicornhatmini
        self.text = ''

        # Load a nice 5x7 pixel font
        # Granted it's actually 5x8 for some reason :| but that doesn't matter
        self.font = ImageFont.truetype('data_files/5x7.ttf', 8)

        self.update_text(text)


    def display_text(self, offset_x, r_color, g_color, b_color):
        '''displays the currently set text with a given offset and colour'''
        # function doesn't take the text as most of the time the text is going to be the same
        display_width, display_height = self.unicornhatmini.get_shape()

        # used to prevent offset_x from being to large and causing an error
        x_offset_local = offset_x
        if x_offset_local + display_width > self.image.size[0]:
            x_offset_local = self.image.size[0] - display_width

        for y in range(display_height):
            for x in range(display_width):
                if self.image.getpixel((x + x_offset_local, y)) == 255:
                    self.unicornhatmini.set_pixel(x, y, r_color, g_color, b_color)
                else:
                    self.unicornhatmini.set_pixel(x, y, 0, 0, 0)
        self.unicornhatmini.show()


    def update_text(self, text):
        '''updates the text that is displayed'''
        self.text = text

        display_width, display_height = self.unicornhatmini.get_shape()

        # Measure the size of our text, we only really care about the width for the moment
        # but we could do line-by-line scroll if we used the height
        self.text_width, self.text_height = self.font.getsize(text)

        # Create a new PIL image big enough to fit the text
        self.image = Image.new('P', (self.text_width + display_width + display_width, display_height), 0)
        self.draw = ImageDraw.Draw(self.image)

        # Draw the text into the image
        self.draw.text((display_width, -1), text, font=self.font, fill=255)
