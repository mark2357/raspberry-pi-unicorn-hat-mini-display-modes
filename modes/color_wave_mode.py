'''contains class PixelRainMode that is used to displays coloured pixels moving down the screen grid/screen'''

import random

from PIL import Image, ImageDraw

from modes.base_mode import BaseMode

class ColorWaveMode(BaseMode):
    '''a led mode that displays colored waves from points on the screen'''
    def __init__(self, unicornhatmini, config, custom_options=None):
        super().__init__(unicornhatmini, config, custom_options)
        self.points = []
        number_of_points = self.config.getint('COLOR_WAVE_MODE', 'NUMBER_OF_POINTS', fallback=3)
        self.number_of_points = number_of_points
        self.previous_image = None

        self.add_initial_points()


    def display_frame(self):
        '''used to display the next frame of the clock mode (should be run at least once a second)'''

        self.update_point_radius()

        display_width, display_height = self.unicornhatmini.get_shape()


        if self.previous_image is None:
            # Create a new PIL image big enough to fit the pixels
            self.previous_image = Image.new('RGBA', (display_width, display_height), 0)
        else:
            image = Image.new('RGBA', (display_width, display_height), 0)
            self.previous_image = Image.blend(self.previous_image, image, 0.5)

        draw = ImageDraw.Draw(self.previous_image)

        for point in self.points:
            # draws pixels on bitmap
            p_x_min = point['x'] - point['radius']
            p_y_min = point['y'] - point['radius']
            p_x_max = point['x'] + point['radius']
            p_y_max = point['y'] + point['radius']

            draw.ellipse((p_x_min, p_y_min, p_x_max, p_y_max), outline=(point['r'], point['g'], point['b']))

        for y in range(display_height):
            for x in range(display_width):
                pixel = self.previous_image.getpixel((x, y))

                self.unicornhatmini.set_pixel(x, y, pixel[0], pixel[1], pixel[2])

        self.unicornhatmini.show()

        return self.config.getint('COLOR_WAVE_MODE', 'FPS', fallback=30)



    def update_point_radius(self):
        '''randomly creates colored pixels moving down the screen'''

        self.remove_old_points()

        self.add_new_points()

        for point in self.points:
            point['radius'] += 1


    def remove_old_points(self):
        '''removes points below the bottom of the screen'''

        # pylint: disable=unused-variable
        display_width, display_height = self.unicornhatmini.get_shape()
        points_to_remove = []

        # finds points that have expired waves
        # allows a few extra points so the bitmap can move fully offscreen
        for point in self.points:
            if point['radius'] >= random.randrange(18, 26):
                points_to_remove.append(point)

        # removes points off screen
        for points in points_to_remove:
            self.points.remove(points)


    def add_new_points(self):
        '''adds new points as some have been removed'''

        display_width, display_height = self.unicornhatmini.get_shape()

        points_to_add = self.number_of_points - len(self.points)

        # pylint: disable=unused-variable
        for x in range(0, points_to_add):
            new_point = dict()
            new_point['x'] = random.randrange(0, display_width)
            new_point['y'] = random.randrange(0, display_height)
            new_point['radius'] = 0
            new_point['r'] = random.randrange(0, 256)
            new_point['g'] = random.randrange(0, 256)
            new_point['b'] = random.randrange(0, 256)
            self.points.append(new_point)

    def add_initial_points(self):
        '''clears points and adds new points'''

        self.points = []
        display_width, display_height = self.unicornhatmini.get_shape()

        # pylint: disable=unused-variable
        for x in range(0, self.number_of_points):
            new_point = dict()
            new_point['x'] = random.randrange(0, display_width)
            new_point['y'] = random.randrange(0, display_height)
            new_point['radius'] = random.randrange(0, 10)
            new_point['r'] = random.randrange(0, 256)
            new_point['g'] = random.randrange(0, 256)
            new_point['b'] = random.randrange(0, 256)
            self.points.append(new_point)
