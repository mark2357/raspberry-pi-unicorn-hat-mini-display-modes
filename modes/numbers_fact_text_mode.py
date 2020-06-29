'''contains class that is used to display text about random numbers'''
from helpers.fetch_data_from_api import fetch_data_from_api
from modes.scrolling_text_base_mode import ScrollingTextBaseMode

class NumbersFactTextMode(ScrollingTextBaseMode):
    '''class used to display text on led that shows random infomation about numbers'''

    def update_current_text(self):
        '''updates the current text with data from web API'''
        self.set_current_text(fetch_data_from_api('http://numbersapi.com/random'))
