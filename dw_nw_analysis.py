# -*- coding: utf-8 -*-
"""
Deward Efficiency vs. Networth.
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

# Filter out certain ranks
df1 = df.drop(df[df['rank_tier'] == ('Herald')].index)
df1 = df1.drop(df[df['rank_tier'] == ('Guardian')].index)
df1 = df1.drop(df[df['rank_tier'] == ('Crusader')].index)
df1 = df1.drop(df[df['rank_tier'] == ('Archon')].index)
df1 = df1.drop(df[df['rank_tier'] == ('Legend')].index)

# Table of radiant deward efficiency and its networth
rad_nw_vs_eff_all = pd.DataFrame({
        'ID':df.ID,
        'dw_eff':df.radiant_deward_efficiency,
        'nw':df.networth_radiant,
        'rank_tier':df.rank_tier})
# Table of radiant deward efficiency and its networth
dire_nw_vs_eff_all = pd.DataFrame({
        'ID':df.ID,
        'dw_eff':df.dire_deward_efficiency,
        'nw':df.networth_dire,
        'rank_tier':df.rank_tier})
nw_vs_eff = pd.concat([rad_nw_vs_eff_all,dire_nw_vs_eff_all], ignore_index = True)

# Table of radiant deward efficiency and its networth
rad_nw_vs_eff_lgd_imt = pd.DataFrame({
        'ID':df1.ID,
        'dw_eff':df1.radiant_deward_efficiency,
        'nw':df1.networth_radiant,
        'rank_tier':df1.rank_tier})
# Table of radiant deward efficiency and its networth
dire_nw_vs_eff_lgd_imt = pd.DataFrame({
        'ID':df1.ID,
        'dw_eff':df1.dire_deward_efficiency,
        'nw':df1.networth_dire,
        'rank_tier':df1.rank_tier})
nw_vs_eff_lgd_imt = pd.concat([rad_nw_vs_eff_lgd_imt,dire_nw_vs_eff_lgd_imt], ignore_index = True)

# Plotting
fig1 = plt.figure(figsize = (16,7))

ax1 = plt.subplot(1,2,1)
plt.scatter(nw_vs_eff.dw_eff,nw_vs_eff.nw,alpha=0.05,color='blue')
plt.title('Deward Efficiency vs. Net-worth', fontsize = 20)
plt.xlabel('Deward Efficiency(%)', fontsize = 15)
plt.ylabel('Networth', fontsize = 15)
plt.ylim(0,170000)

ax2 = plt.subplot(1,2,2)
plt.scatter(nw_vs_eff_lgd_imt.dw_eff,nw_vs_eff_lgd_imt.nw,alpha=0.05,color='blue')
plt.title('Deward Efficiency vs. Net-worth (Ancient-Immortal)', fontsize = 20)
plt.xlabel('Deward Efficiency(%)', fontsize = 15)
plt.ylabel('Networth', fontsize = 15)
plt.ylim(0,170000)
plt.savefig('dw_vs_nw_overview.png')