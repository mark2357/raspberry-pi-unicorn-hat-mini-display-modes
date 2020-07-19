'''contains functions used to get mode data, contains get_mode_data() and get_valid_mode_ids()'''

from helpers.get_config import get_config

from modes.asx_stock_text_mode import ASXStockTextMode
from modes.clock_mode import ClockMode
from modes.color_wave_mode import ColorWaveMode
from modes.covid_19_new_cases_text_mode import Covid19NewCasesTextMode
from modes.custom_text_mode import CustomTextMode
from modes.numbers_fact_text_mode import NumbersFactTextMode
from modes.pixel_rain_mode import PixelRainMode
from modes.poke_random_info_text_mode import PokeRandomInfoTextMode

def get_mode_data():
    '''returns all the information about all the modes'''

    config = get_config()

    return {
        'asx_stock_text_mode': {
            'name': 'ASX Stocks',
            'class_constructor': ASXStockTextMode,
            'enabled': config.getboolean('ASX_STOCK_TEXT_MODE', 'ENABLED', fallback=True)
        },
        'clock_mode': {
            'name': 'Clock',
            'class_constructor': ClockMode,
            'enabled': config.getboolean('CLOCK_MODE', 'ENABLED', fallback=True)
        },
        'color_wave_mode': {
            'name': 'Color Wave',
            'class_constructor': ColorWaveMode,
            'enabled': config.getboolean('COLOR_WAVE_MODE', 'ENABLED', fallback=True)
        },
        'covid_19_new_cases_text_mode': {
            'name': 'Covid 19 New Cases',
            'class_constructor': Covid19NewCasesTextMode,
            'enabled': config.getboolean('COVID_VIC_NEW_CASES_MODE', 'ENABLED', fallback=True)
        },
        'custom_text_mode': {
            'name': 'Custom Text',
            'class_constructor': CustomTextMode,
            'enabled': config.getboolean('CUSTOM_TEXT_MODE', 'ENABLED', fallback=True)
        },
        'numbers_fact_text_mode': {
            'name': 'Numbers Facts',
            'class_constructor': NumbersFactTextMode,
            'enabled': config.getboolean('NUMBERS_FACT_TEXT_MODE', 'ENABLED', fallback=True)
        },
        'pixel_rain_mode': {
            'name': 'Pixel Rain',
            'class_constructor': PixelRainMode,
            'enabled': config.getboolean('PIXEL_RAIN_MODE', 'ENABLED', fallback=True)
        },
        'poke_random_info_text_mode': {
            'name': 'Random Pokemon Info',
            'class_constructor': PokeRandomInfoTextMode,
            'enabled': config.getboolean('POKE_RANDOM_INFO_TEXT_MODE', 'ENABLED', fallback=True)
        },
    }

def get_valid_mode_ids():
    '''returns array of valid mode ids'''
    modes_data = get_mode_data()
    valid_ids = []

    for mode_id, mode_data in modes_data.items():
        if mode_data['enabled']:
            valid_ids.append(mode_id)
    return valid_ids