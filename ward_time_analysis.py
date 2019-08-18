# -*- coding: utf-8 -*-
"""
The purpose of this file is to find the difference in warding between different ranks.
Although for now, there are no differences, it can be extended for future research
"""

import pandas as pd
from matplotlib import pyplot as plt
import json
import seaborn as sns
# List of match IDs
match_id_list = []

# Open the JSON file saved from @test_match_opendota.py
with open('match_data.json') as match_data:
    json_output_1 = json.load(match_data)
with open('match_data_2.json') as match_data_2:
    json_output_2 = json.load(match_data_2)
with open('match_data_3.json') as match_data_3:
    json_output_3 = json.load(match_data_3)
with open('match_data_4.json') as match_data_4:
    json_output_4 = json.load(match_data_4)
    
# Concatenate multiple JSON files so it's less susceptible to errors
json_output = json_output_1 + json_output_2 + json_output_3 + json_output_4

#TODO: Add rank_tier to the dataframe
    
for i in range(len(json_output)):
    match_id_list.append(json_output[i]['match_id'])
    
# Average rank name of the match
match_rank_name = []

# List of ward timestamps of the entire database
ward_timestamps_list = []

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

# Iterate through the list of players to get the overview of wards on both teams
for j in range(len(json_output)):

    # List of ward timestapms of a match
    ward_timestamps =[]
    # Radiant win = 1 means radiant wins
    # Radiant win = 0 means dire wins          
    for i in range(10):
        # Data of when were the wards placed
        if 'obs_log' in json_output[j]['players'][i]:
            obs_log = json_output[j]['players'][i]['obs_log']
            if (obs_log is not None) and (len(obs_log) > 0):
                for k in range(len(obs_log)):
                    ward_timestamps.append(obs_log[k]['time'])
                
    ward_timestamps_list.append(ward_timestamps)
    match_rank_name.append(rank_name_setter(j))

data_dict = {'ID':match_id_list,
             'ward_time':ward_timestamps_list,
             'rank_tier':match_rank_name}

df = pd.DataFrame(data_dict)
df = df.dropna().reset_index()
ward_times_legend = []
ward_times_ancient = []
ward_times_archon = []
ward_times_divine = []

# DataFrames to plot the warding time differences between the rank tiers
df1 = df[df.rank_tier == 'Archon']
for i in range(len(df1)):
    ward_times_archon += df1.iloc[i,2]
    
df2 = df[df.rank_tier == 'Legend']
for i in range(len(df2)):
    ward_times_legend += df2.iloc[i,2]
    
df3 = df[df.rank_tier == 'Ancient']
for i in range(len(df3)):
    ward_times_ancient += df3.iloc[i,2]
    
df4 = df[df.rank_tier == 'Divine']
for i in range(len(df4)):
    ward_times_divine += df4.iloc[i,2]
# Setting styles:
sns.set_style("darkgrid")
sns.set_palette("pastel")

sns.kdeplot(ward_times_archon,shade=True)
sns.kdeplot(ward_times_legend,shade=True)
sns.kdeplot(ward_times_ancient,shade=True)
sns.kdeplot(ward_times_divine,shade=True)
plt.show()
