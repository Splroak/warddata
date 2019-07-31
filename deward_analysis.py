# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 17:56:43 2019

@author: Anh Hoang
"""
#TODO: make the scale into percentage
import pandas as pd
import matplotlib.pyplot as plt

# Main Dataframe
df = pd.read_pickle('match_database.pkl')

# Add a column of radiant deward efficiency
df['radiant_deward_efficiency'] = df.apply(lambda row: round(row['obs_kill_radiant']/row['obs_placed_dire']*100,2)\
  if row['obs_placed_dire'] != 0\
  else None,axis=1)

# Add a column of dire deward efficiency
df['dire_deward_efficiency'] = df.apply(lambda row: round(row['obs_kill_dire']/row['obs_placed_radiant']*100,2)\
  if row['obs_placed_radiant'] != 0\
  else None,axis=1)

# Drop the new NaN's from the 2 columns
df = df.dropna().reset_index(drop=True)

# Picking out certain ranks
df =df.loc[df['rank_tier'] == 'Immortal']

# function to pivot table from the initial df
def pivot_table(columns,index,values):
    df_pivoted = df.groupby([columns,index]).ID.count().reset_index().pivot(columns=columns,
               index=index,
               values=values).fillna(0)
    return df_pivoted
# (Radiant) Table of radiant observer kill and its corresponding wins.
df2 = pivot_table('obs_kill_radiant','radiant_win','ID')

# (Dire) Table of dire observer kill and its corresponding wins
df3 = pivot_table('obs_kill_dire','radiant_win','ID')

# (Radiant) Table of radiant observer placed and its corresponding wins
df4 = pivot_table('obs_placed_radiant','radiant_win','ID')

# (Dire) Table of dire observer placed and its corresponding wins
df5 = pivot_table('obs_placed_radiant','radiant_win','ID')

# (Radiant) Table of radiant dewarding efficiency and its corresponding wins
df6 = pivot_table('radiant_deward_efficiency','radiant_win','ID')

# (Dire) Table of dire dewarding efficiency and its corresponding wins
df7 = pivot_table('dire_deward_efficiency','radiant_win','ID')
# Inflate both tables with continuous numbers in range (0,16) (if they are discrete before)
for i in range(50):
    if float("{:.1f}".format(i)) not in df2.columns:
        df2[float("{:.1f}".format(i))] = 0
        
    if float("{:.1f}".format(i)) not in df3.columns:
        df3[float("{:.1f}".format(i))] = 0
        
    if float("{:.1f}".format(i)) not in df4.columns:
        df4[float("{:.1f}".format(i))] = 0
        
    if float("{:.1f}".format(i)) not in df5.columns:
        df5[float("{:.1f}".format(i))] = 0

# Re-sort the table columns, ascending
df3 = df3.reindex(columns=sorted(df3.columns))
df4 = df4.reindex(columns=sorted(df4.columns))
df5 = df5.reindex(columns=sorted(df5.columns))

# Table of radiant deward efficiency and its network
rad_nw_vs_eff = pd.DataFrame({
        'ID':df.ID,
        'dw_eff':df.radiant_deward_efficiency,
        'nw':df.networth_radiant,
        'rank_tier':df.rank_tier})
# Table of radiant deward efficiency and its network
dire_nw_vs_eff = pd.DataFrame({
        'ID':df.ID,
        'dw_eff':df.dire_deward_efficiency,
        'nw':df.networth_dire,
        'rank_tier':df.rank_tier})
overall_nw_vs_eff = pd.concat([rad_nw_vs_eff,dire_nw_vs_eff],ignore_index = True)

# Table of radiant deward efficiency and its corresponding win
rad_eff = df[df['radiant_win'] == 1]
rad_eff_dict = {
        'ID':rad_eff['ID'],
        'dw_eff':rad_eff['radiant_deward_efficiency']}
rad_eff_df = pd.DataFrame(rad_eff_dict)

# Table of dire deward efficiency and its corresponding win
dir_eff = df[df['radiant_win'] == 0]
dir_eff_dict = {
        'ID': dir_eff['ID'],
        'dw_eff':dir_eff['dire_deward_efficiency']}
dir_eff_df = pd.DataFrame(dir_eff_dict)

# Merging 2 tables to 1 table of matches and their deward efficiency of the winning team
eff_df = pd.concat([rad_eff_df,dir_eff_df],ignore_index= True)

                    ##############################################################
# Table of each deward efficiency and its corresponding matches
dir_overall_eff = df.groupby('dire_deward_efficiency').ID.count().reset_index()

#count dir_eff_df
count_dir_eff = dir_eff_df.groupby('dw_eff').ID.count().reset_index()

# Merging winning matches and total matches of dire
merged_dire = pd.merge(dir_overall_eff,count_dir_eff,how='right',left_on='dire_deward_efficiency',right_on='dw_eff')
merged_dire.dropna()

# Dropping unnecessary columns and rearranging columns
merged_dire = merged_dire.drop('dire_deward_efficiency',axis=1)
merged_dire = merged_dire.rename(index=str, columns = {'ID_x':'total_match','ID_y':'win_match'})
                    ##############################################################
                    # The following code snippet is exactly like the above one, except it's for radiant
rad_overall_eff = df.groupby('radiant_deward_efficiency').ID.count().reset_index()

count_rad_eff = rad_eff_df.groupby('dw_eff').ID.count().reset_index()

merged_rad = pd.merge(rad_overall_eff,count_rad_eff,how='right',left_on='radiant_deward_efficiency',right_on='dw_eff')
merged_rad = merged_rad.dropna()

merged_rad = merged_rad.drop('radiant_deward_efficiency',axis=1)
merged_rad = merged_rad.rename(index=str, columns = {'ID_x':'total_match','ID_y':'win_match'})
                    ##############################################################
                    
# Merge both dire and radiant to create a table of overall winrate and deward efficiency (regardless of teams)
merged_all = pd.merge(merged_rad,merged_dire,on=['dw_eff','total_match','win_match'],how='outer')
merged_all = merged_all[['dw_eff','total_match','win_match']]
merged_all['winrate'] = merged_all.apply(lambda row: row['win_match']/row['total_match']*100,axis=1)
merged_all = merged_all.sort_values(by='dw_eff').reset_index()

# Plotting
fig1 = plt.figure(figsize = (14,7))
ax1 = plt.subplot()
plt.scatter(overall_nw_vs_eff.dw_eff,overall_nw_vs_eff.nw,alpha = 0.2,color='red')
plt.ylim(0,200000)
plt.xlabel('Deward Efficiency(%)')
plt.ylabel('Net worth')
plt.show()