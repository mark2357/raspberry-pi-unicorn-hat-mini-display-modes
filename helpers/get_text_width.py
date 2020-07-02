'''contains function to get pixel width for the given text plus padding at start and end of text'''

from PIL import ImageFont
from helpers.get_project_path import get_project_path

def get_text_width(unicornhatmini, text):
    '''returns the pixel width for the given text plus padding at start and end of text'''
    font = ImageFont.truetype(get_project_path() + '/data_files/5x7.ttf', 8)

    # pylint: disable=unused-variable
    display_width, display_height = unicornhatmini.get_shape()

    # Measure the size of our text, we only really care about the width for the moment
    # pylint: disable=unused-variable
    text_width, text_height = font.getsize(text)
    return text_width + display_width + display_width
