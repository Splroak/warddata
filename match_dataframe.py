# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 17:03:32 2019

@author: Anh Hoang
Generate the Dataframe for further analysis
"""

import pandas as pd
import json

# List of match IDs
match_id_list = []

# Open the JSON file saved from @test_match_opendota.py
with open('match_data.json') as match_data:
    json_output_1 = json.load(match_data)
with open('match_data_2.json') as match_data_2:
    json_output_2 = json.load(match_data_2)
with open('match_data_3.json') as match_data_3:
    json_output_3 = json.load(match_data_3)
    
# Concatenate multiple JSON files so it's less susceptible to errors
json_output = json_output_1 + json_output_2 + json_output_3

#TODO: Add rank_tier to the dataframe
    
for i in range(len(json_output)):
    match_id_list.append(json_output[i]['match_id'])
    
# Radiant lists to be inflated
obs_placed_radiant = []
obs_kill_radiant = []
sen_placed_radiant = []
networth_radiant = []

# Dire list to be inflated
obs_placed_dire = []
obs_kill_dire = []
sen_placed_dire = []
networth_dire = []

# Average rank name of the match
match_rank_name = []

# List of ward timestamps of the entire database
ward_timestamps_list = []

# Boolean values of radiant win or lose
radiant_win = []

# Function to set the rank tier for a match
def rank_name_setter(match):
    sum_tier = 0
    avg_tier = 0
    j = 0
    for i in range(10):
        if json_output[match]['players'][i]['rank_tier'] != None:
            sum_tier += json_output[match]['players'][i]['rank_tier']
            j += 1
    avg_tier = sum_tier/j
    # The first letter must be capitalized
    if 0 <= avg_tier < 20:
        rank_name = "Herald"
    elif 20 <= avg_tier < 30:
        rank_name = "Guardian"
    elif 30 <= avg_tier < 40:
        rank_name = "Crusader"
    elif 40 <= avg_tier < 50:
        rank_name = "Archon"
    elif 50 <= avg_tier < 60:
        rank_name = "Legend"
    elif 60 <= avg_tier < 70:
        rank_name = "Ancient"
    elif 70 <= avg_tier < 80:
        rank_name = "Divine"
    elif 80 <= avg_tier:
        rank_name = "Immortal"
        
    return rank_name

# Function to extract data under 'players' dict
def ward_data_extractor(match,player,key):
    ward_data = json_output[match]['players'][player][key]
    return ward_data

# Check if the player is from radiant or dire
def isRadiant(match,player):
    if json_output[match]['players'][player]['player_slot'] < 5:
        return True
    elif json_output[match]['players'][player]['player_slot'] in range(128,133):
        return False

# Iterate through the list of players to get the overview of wards on both teams
for j in range(len(json_output)):
    # Wards data on the radiant
    total_obs_placed_radiant = 0
    total_obs_kill_radiant = 0
    total_sen_placed_radiant = 0
    total_networth_radiant = 0
    # Wards data on the dire
    total_obs_placed_dire = 0
    total_sen_placed_dire = 0
    total_obs_kill_dire = 0
    total_networth_dire = 0
    # List of ward timestapms of a match
    ward_timestamps =[]
    # Radiant win = 1 means radiant wins
    # Radiant win = 0 means dire wins
    if json_output[j]['radiant_win'] == True:
        radiant_win.append(1)
    else:
        radiant_win.append(0)
              
    for i in range(10):
        if isRadiant(j,i):
            # total number of observers kill by the radiant
            total_obs_kill_radiant += ward_data_extractor(j,i,'observer_kills')
            # total number of sentry placed by the radiant
            total_sen_placed_radiant += ward_data_extractor(j,i,'sen_placed')
            # total number of observer placed by the radiant
            total_obs_placed_radiant += ward_data_extractor(j,i,'obs_placed')
            # net worth of radiant team
            total_networth_radiant += ward_data_extractor(j,i,'total_gold')
        else:
            # total number of observers kill by the dire
            total_obs_kill_dire += ward_data_extractor(j,i,'observer_kills')
            # total number of sentry placed by the dire
            total_sen_placed_dire += ward_data_extractor(j,i,'sen_placed')
            # total number of observer placed by the dire
            total_obs_placed_dire += ward_data_extractor(j,i,'obs_placed')
            # net worth of radiant team
            total_networth_dire += ward_data_extractor(j,i,'total_gold')
        
        # Data of when were the wards placed
        obs_log = json_output[j]['players'][i]['obs_log']
        for k in range(len(obs_log)):
            if len(obs_log) > 0:
                ward_timestamps.append(obs_log[k]['time'])
        
    obs_kill_radiant.append(total_obs_kill_radiant)
    sen_placed_radiant.append(total_sen_placed_radiant)
    obs_placed_radiant.append(total_obs_placed_radiant)
    networth_radiant.append(total_networth_radiant)
    obs_kill_dire.append(total_obs_kill_dire)
    sen_placed_dire.append(total_sen_placed_dire)
    obs_placed_dire.append(total_obs_placed_dire)
    networth_dire.append(total_networth_dire)
    ward_timestamps_list.append(ward_timestamps)
    match_rank_name.append(rank_name_setter(j))

data_dict = {'ID':match_id_list,
             'obs_kill_radiant':obs_kill_radiant,
             'obs_placed_radiant':obs_placed_radiant,
             'sen_placed_radiant':sen_placed_radiant,
             'networth_radiant':networth_radiant,
             'obs_kill_dire':obs_kill_dire,
             'obs_placed_dire':obs_placed_dire,
             'sen_placed_dire':sen_placed_dire,
             'networth_dire':networth_dire,
             'radiant_win':radiant_win,
             'ward_time':ward_timestamps_list,
             'rank_tier':match_rank_name}

df = pd.DataFrame(data_dict)
df = df.dropna().reset_index()
df.to_pickle('match_database.pkl')