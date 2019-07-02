
import numpy as np
import pandas as pd
from urllib.request import Request, urlopen
import json

#The base URL to query JSON from OpenDota
BASE_OPENDOTA_URL = "https://api.opendota.com/api/"

#OpenDota API parameter for matches
OPENDOTA_MATCHES = "matches/"

#Read csv file generated from match_id_reader.py file
json_result = pd.read_csv("match_id.csv",header=None)

#Get the match_id and turn it to a list to iterate
match_id  = json_result.loc[:,1]
match_id_list = match_id.tolist()
matches_detail_json = []

#Call OpenDota API on the list of matches from match_id.csv
for i in match_id_list:
    i = str(i)
    req = Request(BASE_OPENDOTA_URL + OPENDOTA_MATCHES + i,headers={"User-agent": "Mozilla/5.0"})
    matches_detail_json.append(urlopen(req).read())
