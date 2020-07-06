'''contains basic function for getting data from API endpoint'''
import requests

def fetch_data_from_api(url):
    '''returns data from API endpoint'''
    # Make a GET request to fetch the raw HTML content
    response = requests.get(url)

    if response.status_code != 200:
        print(f"error status code is not 200 it's {response.status_code} from url {url}")

    content = response.text
    return content
