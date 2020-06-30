'''contains class that is used to display random text about pokemon'''

import random_pokemon_info
from modes.scrolling_text_base_mode import ScrollingTextBaseMode

class PokeRandomInfoTextMode(ScrollingTextBaseMode):
    '''displays random text about pokemon'''
    def update_current_text(self):
        self.set_current_text(random_pokemon_info.get_random_info())
