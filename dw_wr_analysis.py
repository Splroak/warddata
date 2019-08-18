# -*- coding: utf-8 -*-
"""
Deward Efficiency vs. Winrate.
"""
import pandas as pd
import matplotlib.pyplot as plt
# Main Dataframe
df = pd.read_pickle('match_database.pkl')

# Add a column of radiant deward efficiency
df['radiant_deward_efficiency'] = df.apply(lambda row: round(row['obs_kill_radiant']/row['obs_placed_dire']*100,0)\
  if row['obs_placed_dire'] != 0\
  else None,axis=1)

# Add a column of dire deward efficiency
df['dire_deward_efficiency'] = df.apply(lambda row: round(row['obs_kill_dire']/row['obs_placed_radiant']*100,0)\
  if row['obs_placed_radiant'] != 0\
  else None,axis=1)

# Drop the new NaN's from the 2 columns
df = df.dropna().reset_index(drop=True)

# Picking out certain ranks
#df = df.loc[df['rank_tier'] == 'Ancient']
df1 = df.drop(df[df['rank_tier'] == ('Herald')].index)
df1 = df1.drop(df[df['rank_tier'] == ('Guardian')].index)
df1 = df1.drop(df[df['rank_tier'] == ('Crusader')].index)
df1 = df1.drop(df[df['rank_tier'] == ('Archon')].index)
df1 = df1.drop(df[df['rank_tier'] == ('Legend')].index)
# function to pivot table from the initial df
def pivot_table(columns,index,values):
    df_pivoted = df.groupby([columns,index]).ID.count().reset_index().pivot(columns=columns,
               index=index,
               values=values).fillna(0)
    return df_pivoted
# (Radiant) Table of radiant observer kills and its corresponding wins.
df2 = pivot_table('obs_kill_radiant','radiant_win','ID')

# (Dire) Table of dire observer kills and its corresponding wins
df3 = pivot_table('obs_kill_dire','radiant_win','ID')

# (Radiant) Table of radiant observer placed and its corresponding wins
df4 = pivot_table('obs_placed_radiant','radiant_win','ID')

# (Dire) Table of dire observer placed and its corresponding wins
df5 = pivot_table('obs_placed_radiant','radiant_win','ID')

# (Radiant) Table of radiant dewarding efficiency and its corresponding wins
df6 = pivot_table('radiant_deward_efficiency','radiant_win','ID')

# (Dire) Table of dire dewarding efficiency and its corresponding wins
df7 = pivot_table('dire_deward_efficiency','radiant_win','ID')
# Inflate both tables with continuous numbers in range (0,49) (in case they are discrete before)
for i in range(50):
    # The names of the columns are re-formatted to float type to match Python default type (with decimal places)
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

# Table of radiant deward efficiency when they win
rad_eff = df[df['radiant_win'] == 1]
rad_eff_dict = {
        'ID':rad_eff['ID'],
        'dw_eff':rad_eff['radiant_deward_efficiency']}
rad_eff_df = pd.DataFrame(rad_eff_dict)

# Table of dire deward efficiency when they win
dir_eff = df[df['radiant_win'] == 0]
dir_eff_dict = {
        'ID': dir_eff['ID'],
        'dw_eff':dir_eff['dire_deward_efficiency']}
dir_eff_df = pd.DataFrame(dir_eff_dict)

# Merging rad_eff and dir_eff to 1 table of matches and their deward efficiency of the winning team
eff_df_win = pd.concat([rad_eff_df,dir_eff_df],ignore_index = True)

# Overall list of efficiencies and their frequencies
eff_list = df['dire_deward_efficiency'].tolist()+df['radiant_deward_efficiency'].tolist()
eff_overall_dict = {
        'ID':range(len(eff_list)),
        'dw_eff':eff_list}
eff_freq_all = pd.DataFrame(eff_overall_dict)
eff_freq_all = eff_freq_all.groupby('dw_eff').ID.count().reset_index()

# List of efficiencies and their frequencies in winning matches
eff_freq_win = eff_df_win.groupby('dw_eff').ID.count().reset_index()

# Merge to get both Overall frequency and Win frequency of each efficiency
merge_df = pd.merge(eff_freq_all,eff_freq_win,on='dw_eff',how='left').rename(\
                   index=str, columns={'ID_x':'total_match','ID_y':'win_match'})
merge_df['winrate'] = merge_df.apply(lambda row: row.win_match/row.total_match*100,axis = 1).fillna(0)

# Plotting
fig1 = plt.figure(figsize = (12,6))

ax1 = plt.subplot()
plt.scatter(merge_df.dw_eff,merge_df.winrate,alpha=0.3,color='blue')
plt.title('Deward Efficiency vs. Winrate', fontsize = 20)
plt.xlabel('Deward Efficiency(%)', fontsize = 15)
plt.ylabel('Winrate(%)', fontsize = 15)
plt.savefig('dw_vs_winrate.png')
