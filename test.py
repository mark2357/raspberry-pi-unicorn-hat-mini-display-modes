#!/usr/bin/env python3

# import json
# from helpers.fetch_data_from_api import fetch_data_from_api


# data_full = json.loads(fetch_data_from_api('https://api.covid19api.com/dayone/country/australia'))





# def sort_data(data_full):
#     sorted_data = dict()

#     for data in reversed(data_full):
#         if data['Province'] not in sorted_data:
#             sorted_data[data['Province']] = []

#         if len(sorted_data[data['Province']]) > 5:
#             return sorted_data

#         sorted_data[data['Province']].insert(0, data)
    
#         # print(f"Province: {data['Province']}, {data['Date']}")
#         # sorted_data[data.Province][data] = data

# def aggregate_data(sorted_data):
#     aggregated_data = dict()

#     for key, state_data in sorted_data.items():
#         aggregated_data[key] = dict()
#         for data in state_data:
#             aggregated_data[key]['Confirmed'] = data['Confirmed']
#             aggregated_data[key]['Deaths'] = data['Deaths']
#             aggregated_data[key]['Recovered'] = data['Recovered']
#             aggregated_data[key]['Active'] = data['Active']

#     return aggregated_data


# sorted_data = sort_data(data_full)
# aggregated_data = aggregate_data(sorted_data)

# print(json.dumps(sorted_data['Victoria'], indent=4))
# from modules.random_pokemon_info.library.get_random_info import get_random_info
# print(get_random_info())

# from helpers.get_config import get_config

# from bs4 import BeautifulSoup
# import requests

# def fetch_html_and_extract_data_from_url(url):
#     '''requests data from url and returns the beautiful soup object'''
#     # Make a GET request to fetch the raw HTML content
#     html_content = requests.get(url).text

#     # Parse the html content
#     soup = BeautifulSoup(html_content, "lxml")
#     return soup




# data = fetch_html_and_extract_data_from_url('https://covidlive.com.au/vic')

# table = data.find("table", class_="DAILY-CASES")
# table_rows = table.findAll('tr')
# # result.findChild("a", recursive=False).decode_contents()

# output_data = []

# for table_row in table_rows:

#     # skips the header
#     if table_row.get('class') == ['TH']:
#         continue

#     cases = table_row.find('td', class_='NET').find('span').decode_contents()
#     date = table_row.find('td', class_='DATE').decode_contents()
#     # output_data
#     # child = item.findChild("a", recursive=False)
#     # if item.getclass = 
#     print(f'{date} had {cases} cases')

from helpers.fetch_html_data_from_url import fetch_html_and_extract_data_from_url

print(fetch_html_and_extract_data_from_url('https://covidlive.com.au/vic'))

# import urllib.request

# r = urllib.request.urlopen('https://covidlive.com.au/vic')
# print(r.read())
# print(r.getcode())