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

from helpers.get_config import get_config
