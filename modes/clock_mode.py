'''contains class ClockMode that is used to display a clock on the led grid/screen'''
import datetime
import time
import math

from colorsys import hsv_to_rgb
from PIL import Image, ImageDraw

from helpers.get_project_path import get_project_path
from modes.base_mode import BaseMode

class ClockMode(BaseMode):
    '''a led mode that displays a clock with the current time'''

    def display_frame(self):
        '''used to display the next frame of the clock mode (should be run at least once a second)'''

        # loads config
        PLAIN_COLOR = self.config.getboolean('CLOCK_MODE', 'PLAIN_COLOR', fallback=False)
        COLOR_ROTATION_SPEED = self.config.getfloat('CLOCK_MODE', 'COLOR_ROTATION_SPEED', fallback=0.5)
        COLOR_PAN_SPEED = self.config.getfloat('CLOCK_MODE', 'COLOR_PAN_SPEED', fallback=0.5)
        COLOR_SPACING = self.config.getfloat('CLOCK_MODE', 'COLOR_SPACING', fallback=0.05)
        HOUR_12_TIME = self.config.getboolean('CLOCK_MODE', 'HOUR_12_TIME', fallback=False)


        display_width, display_height = self.unicornhatmini.get_shape()

        # Create a new PIL image big enough to fit the text
        image = Image.new('RGBA', (display_width, display_height), 0)
        draw = ImageDraw.Draw(image)

        # gets the current time
        current_time = datetime.datetime.now()

        hour = current_time.hour
        # determines if 12 hour time is needed
        if HOUR_12_TIME:
            hour = hour % 12

        # determines characters
        hour_char_1 = math.floor(hour / 10)
        hour_char_2 = hour % 10
        min_char_1 = math.floor(current_time.minute / 10)
        min_char_2 = current_time.minute % 10

        # loads the needed images
        image_pos_1 = self.get_image_for_number(hour_char_1)
        image_pos_2 = self.get_image_for_number(hour_char_2)
        image_pos_3 = self.get_image_for_number(min_char_1)
        image_pos_4 = self.get_image_for_number(min_char_2)

        # draws digits on bitmap
        draw.bitmap((0, 1), image_pos_1)
        draw.bitmap((4, 1), image_pos_2)
        draw.bitmap((10, 1), image_pos_3)
        draw.bitmap((14, 1), image_pos_4)

        # determines if : should be shown
        if current_time.second % 2 == 0:
            draw.point([(8, 2), (8, 4)])

        x_multi = math.sin(time.time() * COLOR_ROTATION_SPEED)
        y_multi = math.cos(time.time() * COLOR_ROTATION_SPEED)

        for y in range(display_height):
            for x in range(display_width):
                pixel = image.getpixel((x, y))

                # if using plain color
                if PLAIN_COLOR:
                    self.unicornhatmini.set_pixel(x, y, pixel[0], pixel[1], pixel[2])

                # uses texture for bool input, as hue is used for color
                elif pixel[0] > 0:
                    # picks hue value
                    time_offset = time.time() * COLOR_PAN_SPEED
                    x_offset = (x - display_width/2) * x_multi
                    y_offset = (y - display_height/2) * y_multi
                    hue = (time_offset + x_offset + y_offset) * COLOR_SPACING
                    r_color, g_color, b_color = [int(c * 255) for c in hsv_to_rgb(hue, 1.0, 1.0)]
                    self.unicornhatmini.set_pixel(x, y, r_color, g_color, b_color)
                # blank pixel
                else:
                    self.unicornhatmini.set_pixel(x, y, 0, 0, 0)

        self.unicornhatmini.show()

        return self.config.getint('CLOCK_MODE', 'FPS', fallback=30)


    def get_image_for_number(self, num):
        '''returns image for the given number'''
        return Image.open(get_project_path() + '/data_files/3x5_font/' + str(int(num)) + '.png')
