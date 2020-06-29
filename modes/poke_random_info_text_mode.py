
from modes.scrolling_text_base_mode import ScrollingTextBaseMode
import random_pokemon_info

class PokeRandomInfoTextMode(ScrollingTextBaseMode):

    def update_current_text(self):
        self.set_current_text(random_pokemon_info.get_random_info())