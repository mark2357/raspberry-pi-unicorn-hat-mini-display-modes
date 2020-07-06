'''contains class PixelRainMode that is used to displays coloured pixels moving down the screen grid/screen'''

import random
import time

from colorsys import hsv_to_rgb
from PIL import Image, ImageDraw

from helpers.get_project_path import get_project_path
from modes.base_mode import BaseMode

class PixelRainMode(BaseMode):
    '''a led mode that displays coloured pixels moving down the screen'''
    def __init__(self, unicornhatmini, config):
        super().__init__(unicornhatmini, config)
        self.pixels = []
        number_of_pixels = self.config.getint('PIXEL_RAIN_MODE', 'NUMBER_OF_PIXELS', fallback=5)
        self.number_of_pixels = number_of_pixels
        self.frame_counter = 0

        self.add_initial_pixels()


    def display_frame(self):
        '''used to display the next frame of the clock mode (should be run at least once a second)'''

        UPDATE_POSITION_EVERY_X_FRAMES = self.config.getint('PIXEL_RAIN_MODE', 'UPDATE_POSITION_EVERY_X_FRAMES', fallback=2)
        COLOR_ROTATION_SPEED = self.config.getfloat('PIXEL_RAIN_MODE', 'COLOR_ROTATION_SPEED', fallback=0.5)

        self.frame_counter += 1
        if self.frame_counter % UPDATE_POSITION_EVERY_X_FRAMES == 0:
            self.update_pixel_locations()

        display_width, display_height = self.unicornhatmini.get_shape()

        pixel_sprite = Image.open(get_project_path() + '/data_files/pixel_highlight.png')

        # Create a new PIL image big enough to fit the pixels
        image = Image.new('RGBA', (display_width, display_height), 0)
        draw = ImageDraw.Draw(image)


        hue = time.time() * COLOR_ROTATION_SPEED
        r_color, g_color, b_color = [int(c * 255) for c in hsv_to_rgb(hue, 1.0, 1.0)]
        r_background, g_background, b_background = [int(c * 255) for c in hsv_to_rgb(hue, 1.0, 0.3)]


        draw.rectangle([(0, 0), (display_width, display_height)], fill=(r_background, g_background, b_background))

        for pixel in self.pixels:
            # draws pixels on bitmap
            draw.bitmap((pixel['x'], pixel['y'] - 2), pixel_sprite)
            # draw.point((pixel['x'], pixel['y']), fill=(r_color, g_color, b_color))
            # print(f"pixel at {pixel['x']}, {pixel['y']}")


        for y in range(display_height):
            for x in range(display_width):
                pixel = image.getpixel((x, y))

                self.unicornhatmini.set_pixel(x, y, pixel[0], pixel[1], pixel[2])

        self.unicornhatmini.show()

        return self.config.getint('PIXEL_RAIN_MODE', 'FPS', fallback=30)



    def update_pixel_locations(self):
        '''randomly creates colored pixels moving down the screen'''

        self.remove_old_pixels()

        self.add_new_pixels()

        for pixel in self.pixels:
            pixel['y'] += 1


    def remove_old_pixels(self):
        '''removes pixels below the bottom of the screen'''

        display_width, display_height = self.unicornhatmini.get_shape()
        pixels_to_remove = []

        # finds pixels off screen
        # allows a few extra pixels so the bitmap can move fully offscreen
        for pixel in self.pixels:
            if pixel['y'] >= display_height + 2:
                pixels_to_remove.append(pixel)

        # removes pixels off screen
        for pixel in pixels_to_remove:
            self.pixels.remove(pixel)


    def add_new_pixels(self):
        '''adds new pixels as some have alr'''

        display_width, display_height = self.unicornhatmini.get_shape()

        pixels_to_add = self.number_of_pixels - len(self.pixels)

        for x in range(0, pixels_to_add):
            new_pixel = dict()
            new_pixel['x'] = random.randrange(0, display_width)
            new_pixel['y'] = random.randrange(-3, 0)
            self.pixels.append(new_pixel)

    def add_initial_pixels(self):
        '''clears pixels and adds new pixels'''

        self.pixels = []
        display_width, display_height = self.unicornhatmini.get_shape()


        for x in range(0, self.number_of_pixels):
            new_pixel = dict()
            new_pixel['x'] = random.randrange(0, display_width)
            new_pixel['y'] = random.randrange(0, display_height)
            self.pixels.append(new_pixel)
