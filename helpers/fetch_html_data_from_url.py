'''contains function to retrieve html using beautiful soup'''

import urllib.request
from bs4 import BeautifulSoup


def fetch_html_and_extract_data_from_url(url):
    '''requests data from url and returns the beautiful soup object'''

    # uses urllib as there was some issues with using requests
    # (specifically getting 418 when running on raspberry pi) 

    # Make a GET request to fetch the raw HTML content
    response = urllib.request.urlopen(url)

    if response.getcode() != 200:
        print(f"error status code is not 200 it's {response.getcode()}")

    html_content = response.read()

    # Parse the html content
    soup = BeautifulSoup(html_content, "lxml")
    return soup
