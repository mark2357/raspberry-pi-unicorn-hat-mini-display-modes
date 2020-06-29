'''contains basic function for getting data from API endpoint'''
import requests

def fetch_data_from_api(url):
    '''returns data from API endpoint'''
    # Make a GET request to fetch the raw HTML content
    request = requests.get(url)

    content = request.text
    return content
