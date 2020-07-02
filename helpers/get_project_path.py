'''contains function that return the project path'''
import os

def get_project_path():
    '''returns the project path'''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    project_dir_path = os.path.dirname(dir_path)
    return project_dir_path
