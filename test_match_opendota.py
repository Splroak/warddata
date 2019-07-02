# -*- coding: utf-8 -*-
"""
Created on Sat May 25 17:31:51 2019

@author: ADMIN
Used to get the OpenDota JSON only
"""

import pandas as pd
from urllib.request import Request, urlopen
import json

#List of JSON
json_output = []
         
# Matches IDs
match_id = pd.read_csv('match_id.csv')
match_id_list = match_id.iloc[:,1].tolist()

OPENDOTA_API_KEY = "?api_key=6fb4346f-3d4f-4ef8-9254-39a1e0370967"
# Period used in the rate limiter decorator
CALL_PERIOD = 1
# Function to call OpenDota API, the decorator is to limit the call rate
#@RateLimiter(max_calls = 5, period = CALL_PERIOD)
#TODO:
#    2. actually call the fucking API man tired of your shit, maybe try to clean the data at Dota API stage
#    like filtering out bot matches, incompleted matches, etc,...

# API calls on all the matches
for match in match_id_list:
    request = Request("https://api.opendota.com/api/matches/" + str(match) + OPENDOTA_API_KEY,headers={"User-agent": "Mozilla/5.0"}) 
    response = urlopen(request).read()
    json_result = json.loads(response.decode('utf-8'))
    json_output.append(json_result)
with open('match_data.json','w') as match_data:
    json.dump(json_output,match_data)
