import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.image as image
import seaborn as sns

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 300)
pd.options.mode.chained_assignment = None

#Read in data
data = pd.DataFrame('regular_season_2019', engine='python')

#Fix naming issue on some passes
data.passer_player_name.loc[data.passer_player_name=='G.Minshew II'] = 'G.Minshew'

#Dictionary of team colors
COLORS = {'ARI':'#97233F','ATL':'#A71930','BAL':'#241773','BUF':'#00338D','CAR':'#0085CA','CHI':'#00143F',
          'CIN':'#FB4F14','CLE':'#FB4F14','DAL':'#B0B7BC','DEN':'#002244','DET':'#046EB4','GB':'#24423C',
          'HOU':'#C9243F','IND':'#003D79','JAX':'#136677','KC':'#CA2430','LA':'#002147','LAC':'#2072BA',
          'LV':'#C4C9CC','MIA':'#0091A0','MIN':'#4F2E84','NE':'#0A2342','NO':'#A08A58','NYG':'#192E6C',
          'NYJ':'#203731','PHI':'#014A53','PIT':'#FFC20E','SEA':'#7AC142','SF':'#C9243F','TB':'#D40909',
          'TEN':'#4095D1','WAS':'#FFC20F'}

#Get list of logo images
logos = os.listdir(os.getcwd() + '/logos')

logo_paths = []

#Get full path for each logo 
for i in logos:
    logo_paths.append(os.getcwd() + '/logos/' + str(i))

#Make dataframe for color and logo path
teams = pd.Series(COLORS).to_frame(name='color')

#Create column for logo path
teams['logo'] = logo_paths

#Get list of players and count pass attempts
qbs = data.groupby('passer_player_name')[['play_id']].count()

#Sort in order of most pass attempts
qbs.sort_values('play_id', ascending=False, inplace=True)

#Limit to top 30 QBs and sort alphabetically 
qbs = qbs[:30].sort_index()

#Get CPOE data for each QB, grouped by air yards
#Filter between -10 and 40 air yards
cpoe_data = data.loc[(data.passer_player_name.isin(qbs.index)) &
                (data.air_yards>=-10) & 
                (data.air_yards<=40)].groupby(
    ['passer_player_name','posteam','air_yards']).agg(
    {'cpoe':'mean', 'play_id':'count'}).reset_index()

#Drop null values
cpoe_data = cpoe_data.dropna()

#Get NFL average CPOE
nfl_avg = data.loc[(data.air_yards>=-10) & (data.air_yards<=40)].groupby(
    'air_yards', as_index=False)[['cpoe']].mean()

#Create plot figure with 5 rows and 6 columns
fig, axs = plt.subplots(nrows=5, ncols=6, sharex=True, sharey=True, figsize=(20,20))

#Flatten subplot array into one dimension, easier to index
axs = axs.ravel()

for i in range(len(qbs)):
    current_qb = qbs.index[i]
    current_team = cpoe_data.posteam.loc[cpoe_data.passer_player_name==current_qb].values[0]
    current_color = teams.color.loc[current_team]
    
    #Add QB CPOE with lowess smooth
    sns.regplot(cpoe_data.air_yards.loc[cpoe_data.passer_player_name==current_qb],
                cpoe_data.cpoe.loc[cpoe_data.passer_player_name==current_qb],
                color=current_color, lowess=True, scatter_kws={'alpha':.6}, ax=axs[i])
    
    #Add average line
    sns.regplot(nfl_avg.air_yards,
                nfl_avg.cpoe,
                color='red', lowess=True, scatter=False, line_kws={'linestyle':'--'}, ax=axs[i])
    
    #Put name of each QB above plot
    axs[i].set_title(current_qb)
    
    #Add grid lines
    axs[i].grid(zorder=0,alpha=.4)
    axs[i].set_axisbelow(True)
    
    #Hide axes titles on subplots
    axs[i].xaxis.label.set_visible(False)
    axs[i].yaxis.label.set_visible(False)
    
    #Add axes tick labels
    axs[i].xaxis.set_tick_params(labelbottom=True)
    axs[i].yaxis.set_tick_params(labelleft=True)
    
    #Add team logo
    axs[i].imshow(image.imread(teams.logo.loc[current_team]), extent=(23,29,18,24))
    
#Adjust ranges
axs[0].set_xlim(-5,30)
axs[0].set_ylim(-25,25)

#Add titles and source label
plt.suptitle('CPOE 2019', y=.92, fontsize=24, va='center', ha='center')
plt.figtext(.5,.09, 'Air Yards', fontsize=20, va='center', ha='center')
plt.figtext(.09,.5, 'Completion % Over Expected', fontsize=20, va='center', ha='center', rotation='vertical')
plt.figtext(.82,.06, 'Data:nflfastR', fontsize=14)

#Save plot as png
plt.savefig('cpoe.png', dpi=300)