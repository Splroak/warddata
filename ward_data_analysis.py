# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 17:56:43 2019

@author: ADMIN
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_pickle('test_match_database.pkl')

# (Radiant) Table of each number of observer kill and its corresponding win
df2 =df.groupby(['obs_placed_radiant','radiant_win']).ID.count().reset_index().pivot(columns='obs_placed_radiant',
               index='radiant_win',
               values='ID').fillna(0)

# (Dire) Table of dire observer kill and corresponding wins
df3 =df.groupby(['obs_placed_dire','radiant_win']).ID.count().reset_index().pivot(columns='obs_placed_dire',
               index='radiant_win',
               values='ID').fillna(0)
# Inflate both tables with continuous numbers in range (0,16) (if they are discrete before)
for i in range(30):
    if float("{:.1f}".format(i)) not in df2.columns:
        df2[float("{:.1f}".format(i))] = 0
        
    if float("{:.1f}".format(i)) not in df3.columns:
        df3[float("{:.1f}".format(i))] = 0
df3 = df3.reindex(columns=sorted(df3.columns))
#df3 = df3.reindex(columns=(['opened'] + list([a for a in df3.columns if a != 'opened']) ))
win = []
for i in df2.columns:
    win.append(df2.loc[1,i] + df3.loc[0,i])
plt.plot(range(30),win)