# -*- coding: utf-8 -*-
"""
Created on Mon May 20 12:18:31 2019

@author: Anh Hoang

This file is to generate a stationary match_id file (instead of calling new
ones everytime it runs). This is due to OpenDota API is currently behind (i.e delayed)
compared to the official Dota API, resulting non-existent API if we take the newest
matches from Dota API and feed it into OpenDota API.
"""
import pandas as pd
from urllib.request import urlopen
import json



# The base URL to get match_id from official Dota API
BASE_MATCH_ID_URL = "https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?"

# Dota API key
API_KEY = "&key=C21845FDC3305FFC4E91B73A003BEDC6"

# Parameter to retrieve multiple match_id in one call; default is 25
NUM_MATCHES_PARAMETER = "matches_requested="

# Parameter indicating the call starts from a specified ID, descending
START_ID_PARAMETER ="&start_at_match_id="
# Number of matches
NUM_MATCHES = "100"

json_result = []
def api_call(base_url,num_match,api_key,start_id_param = "",start_id = ""): 
    #Querying the data from the completed URL
    matches_history_json = urlopen(base_url + NUM_MATCHES_PARAMETER + num_match + start_id_param + start_id + api_key).read()
    return json.loads(matches_history_json)

# The last ID from the last batch of matches, used to get the next batch of matches that occured before it
last_id = ""
for i in range(3):
    if i == 0:
        json_output = api_call(BASE_MATCH_ID_URL,NUM_MATCHES,API_KEY)
    else:
        json_output = api_call(BASE_MATCH_ID_URL,NUM_MATCHES,API_KEY,START_ID_PARAMETER,str(last_id))
    last_id = json_output["result"]["matches"][-1]["match_id"]
    for j in range(len(json_output["result"]["matches"])):
        json_result.append(json_output["result"]["matches"][j]["match_id"])
    

df = pd.DataFrame(json_result)
df.to_csv("match_id.csv")
