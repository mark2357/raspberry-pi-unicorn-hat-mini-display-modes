'''contains basic function for getting config dictionary'''
import configparser
from helpers.get_project_path import get_project_path

def get_config():
    '''returns the config object'''
    config = configparser.ConfigParser()
    config.read(get_project_path() + '/config.ini')
    return config
