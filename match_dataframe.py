# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 17:03:32 2019

@author: ADMIN
Generate the Data frame for further analysis
"""

import pandas as pd
import json
# List of match IDs
match_id = pd.read_csv('match_id.csv')
match_id_list = match_id.iloc[:,1].tolist()

# Radiant lists to be inflated
obs_placed_radiant = []
obs_kill_radiant = []
sen_placed_radiant = []

#Dire list to be inflated
obs_placed_dire = []
obs_kill_dire = []
sen_placed_dire = []

# Boolean values of radiant win or lose
radiant_win = []
# Open the JSON file saved from @test_match_opendota.py
with open('match_data.json') as match_data:
    json_output = json.load(match_data)
    
# Check if the player is from radiant or dire
def isRadiant(match,player):
    if json_output[match]['players'][player]['player_slot'] < 5:
        return True
    elif json_output[match]['players'][player]['player_slot'] in range(128,133):
        return False

# Check if the match has wards data, i.e 'observer_kills', 'sen_placed', etc...
def hasWardMetrics(match,player):
    if 'observer_kills' in json_output[match]['players'][player]:
        return True
    else:
        return False

# Check if it's a legit match with 10 players
def hasTenPlayers(match):
    if json_output[match]['human_players'] == 10:
        return True
    else:
        return False
# Iterate through the list of players to get the overview of wards on both teams
for j in range(len(json_output)):
    # Wards data on the radiant
    total_obs_placed_radiant = 0
    total_obs_kill_radiant = 0
    total_sen_placed_radiant = 0
    # Wards data on the dire
    total_obs_placed_dire = 0
    total_sen_placed_dire = 0
    total_obs_kill_dire = 0
    
    # Radiant win = 1 means radiant wins
    # Radiant win = 0 means dire wins
    if json_output[j]['radiant_win'] == True:
        radiant_win.append(1)
    else:
        radiant_win.append(0)
        
    if hasTenPlayers(j):        
        for i in range(10):
            if hasWardMetrics(j,i):
                if isRadiant(j,i):
                    # total number of observers kill by the radiant
                    num_obs_kill_radiant = json_output[j]['players'][i]['observer_kills']
                    total_obs_kill_radiant += num_obs_kill_radiant
                    # total number of sentry placed by the radiant
                    num_sen_placed_radiant = json_output[j]['players'][i]['sen_placed']
                    total_sen_placed_radiant += num_sen_placed_radiant
                    # total number of observer placed by the radiant
                    num_obs_placed_radiant = json_output[j]['players'][i]['obs_placed']
                    total_obs_placed_radiant += num_obs_placed_radiant
                else:
                    # total number of observers kill by the dire
                    num_obs_kill_dire = json_output[j]['players'][i]['observer_kills']
                    total_obs_kill_dire += num_obs_kill_dire
                    # total number of sentry placed by the dire
                    num_sen_placed_dire = json_output[j]['players'][i]['sen_placed']
                    total_sen_placed_dire += num_sen_placed_dire
                    # total number of observer placed by the dire
                    num_obs_placed_dire = json_output[j]['players'][i]['obs_placed']
                    total_obs_placed_dire += num_obs_placed_dire
            else:
                # Set the metrics as None for matches without the data
                total_obs_placed_radiant = None
                total_obs_kill_radiant = None
                total_sen_placed_radiant = None
                total_obs_placed_dire = None
                total_sen_placed_dire = None
                total_obs_kill_dire = None
    else:
        # Set the metrics as None for matches without the data
        total_obs_placed_radiant = None
        total_obs_kill_radiant = None
        total_sen_placed_radiant = None
        total_obs_placed_dire = None
        total_sen_placed_dire = None
        total_obs_kill_dire = None

    obs_kill_radiant.append(total_obs_kill_radiant)
    sen_placed_radiant.append(total_sen_placed_radiant)
    obs_placed_radiant.append(total_obs_placed_radiant)
    obs_kill_dire.append(total_obs_kill_dire)
    sen_placed_dire.append(total_sen_placed_dire)
    obs_placed_dire.append(total_obs_placed_dire)


data_dict = {'ID':match_id_list,
             'obs_kill_radiant':obs_kill_radiant,
             'obs_placed_radiant':obs_placed_radiant,
             'sen_placed_radiant':sen_placed_radiant,
             'obs_kill_dire':obs_kill_dire,
             'obs_placed_dire':obs_placed_dire,
             'sen_placed_dire':sen_placed_dire,
             'radiant_win':radiant_win}

df = pd.DataFrame(data_dict)
df = df.dropna().reset_index()
df.to_pickle('test_match_database.pkl')