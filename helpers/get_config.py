'''contains basic function for getting config dictionary'''
import configparser

def get_config():
    '''returns the config object'''
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config
