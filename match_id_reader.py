# -*- coding: utf-8 -*-
"""
Created on Mon May 20 12:18:31 2019

@author: Anh Hoang

Generate a batch of IDs to work with

There are 4 json files. The reason there are 4 separated files (instead of 1) was to avoid 502 error, I figured out how to bypass the error,
but the project works fine with 4 files so I don't call the API again (also it costs money and I'm broke)
"""
from ratelimiter import RateLimiter
from urllib.request import Request,urlopen
from urllib.error import HTTPError
import json

#FIXME: 'observer_kills' in json_result['players'][0]) and (
# save this one for api call

OPENDOTA_API_KEY = "api_key=6fb4346f-3d4f-4ef8-9254-39a1e0370967"

# The base URL to get match_id from official Dota API
BASE_MATCH_ID_URL = "https://api.opendota.com/api/publicMatches"

# Parameter indicating the call starts from a specified ID, descending
START_ID_PARAMETER ="?less_than_match_id="



# List of IDs
valid_match_id_response = []

#List of valid matches data in JSON format
json_output = []

# API call function to get a list of matches
@RateLimiter(max_calls = 1 ,period = 10)
def match_list_api_call(base_url,api_key,concatenator='',start_id_param='',start_id=''): 
    #Querying the data from the completed URL
    request = Request(base_url + start_id_param + start_id + concatenator + api_key, headers={"User-agent": "Mozilla/5.0"})
    response = urlopen(request).read()
    return json.loads(response)

#   API call function to get the detail of each match retrieved from the list
@RateLimiter(max_calls = 15, period = 1)
def match_detail_api_call(url):
    request = Request(url,headers={"User-agent": "Mozilla/5.0"}) 
    response = urlopen(request).read()
    return json.loads(response.decode('utf-8'))

# Iterate thru multiple API calls until we get 300 valid matches with ward metrics and 10 human players
def super_api_call():
    try:
        while len(json_output) < 500:
            if len(json_output) == 0:
                json_response = match_list_api_call(BASE_MATCH_ID_URL, OPENDOTA_API_KEY,'?')         
            else:
                last_id = str(valid_match_id_response[-1])
                json_response = match_list_api_call(BASE_MATCH_ID_URL, OPENDOTA_API_KEY,'&',START_ID_PARAMETER,last_id)
                
            for j in range(len(json_response)):
                valid_match_id_response.append(json_response[j]["match_id"])
            print(len(valid_match_id_response))
        
            for match in valid_match_id_response:
                # JSON response of a match
                json_result = match_detail_api_call("https://api.opendota.com/api/matches/" + str(match) + '?' + OPENDOTA_API_KEY)
                if ('observer_kills' in json_result['players'][0]) and (json_result['human_players'] == 10):
                    json_output.append(json_result)
            print('valid matches = ' + str(len(json_output)))
    except HTTPError as e:
        if e.code == 502:
            print(str(e.code) + ' ' + str(e.reason))
            super_api_call()
        else:
            print(str(e.code) + ' ' + str(e.reason))
super_api_call()
with open('match_data_4.json','w') as match_data:
    json.dump(json_output,match_data)