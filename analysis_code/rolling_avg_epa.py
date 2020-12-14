import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

pd.options.mode.chained_assignment = None

YEARS = [2018,2019,2020]

data = pd.DataFrame()

for i in YEARS:
    #Update for your path and file name(s)
    i_data = pd.read_csv(os.getcwd()+'/nflfastr/pbp_'+str(i)+'.csv.gz',
                         compression='gzip', engine='python')
    
    data = data.append(i_data, sort=True)
    
data.reset_index(drop=True, inplace=True)

COLORS = {'ARI':'#97233F','ATL':'#A71930','BAL':'#241773','BUF':'#00338D','CAR':'#0085CA','CHI':'#00143F',
          'CIN':'#FB4F14','CLE':'#FB4F14','DAL':'#B0B7BC','DEN':'#002244','DET':'#046EB4','GB':'#24423C',
          'HOU':'#C9243F','IND':'#003D79','JAX':'#136677','KC':'#CA2430','LA':'#002147','LAC':'#2072BA',
          'LV':'#C4C9CC','MIA':'#0091A0','MIN':'#4F2E84','NE':'#0A2342','NO':'#A08A58','NYG':'#192E6C',
          'NYJ':'#203731','PHI':'#014A53','PIT':'#FFC20E','SEA':'#7AC142','SF':'#C9243F','TB':'#D40909',
          'TEN':'#4095D1','WAS':'#FFC20F'}

#Get dropbacks
data = data.loc[data.qb_epa.isna()==False]

#Abbreviated name of QB
qb = 'J.Allen'

#Get plays for that QB
qb_plays = data[['qb_epa','posteam','season']].loc[(data.passer==qb) | (data.rusher==qb)]

#Add 300 play rolling avg
qb_plays['avg'] = qb_plays.qb_epa.rolling(300).mean()

#Take play 300 forward, first 299 with have null values
qb_plays = qb_plays[300:].reset_index()

#Get average EPA per dropback
nfl_avg = data.qb_epa.loc[data['pass']==1].mean()

fig, ax = plt.subplots(figsize=(18,9))

#Add average line
#Adjust as necessary for location of "NFL Average" label
x_offset = -100

ax.axhline(y=nfl_avg, color='black', linestyle='--')
ax.text(len(qb_plays) + x_offset, nfl_avg+.007, 'NFL Average')

y = qb_plays['avg']
seasons = list(set(qb_plays.season))
seasons.sort()

ax.plot(np.arange(len(y)), y, linewidth=3, color=COLORS[qb_plays.posteam.iloc[0]], alpha=.8)

#Get indexes where season changes
x_lines = qb_plays.loc[qb_plays.season.diff() != 0].index.tolist()

#Add season marker lines
for i in x_lines:
    ax.axvline(x=i, color='black')
    
#Where label is located on y-axis, adjust as needed
label_vheight = .15

#Add final index to x_lines for label placement
x_lines.append(len(y))

#Get midpoints
label_locs = x_lines[:-1] + np.diff(x_lines)/2 - 25

#Add season labels
for j in range(len(label_locs)):
    ax.text(label_locs[j], label_vheight, seasons[j], fontsize=14)

#Add grid
ax.grid(zorder=0,alpha=.4)
ax.set_axisbelow(True)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.margins(x=0)

first_year = qb_plays.season.iloc[0]
last_year = qb_plays.season.iloc[-1]

ax.set_title(qb + ' EPA per Play - ' + str(first_year) + '-' + str(last_year) + 
             '\nRolling 300 Plays', fontsize=16, pad=10)

ax.set_xlabel('Play Number', fontsize=14, labelpad=18)

ax.set_ylabel('Rolling 300 Avg. EPA per Play', fontsize=14, labelpad=18)

plt.figtext(.83, 0.05, 'Data: nflfastR', fontsize=10)

plt.savefig('qb300.png', dpi=400)