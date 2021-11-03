import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 2000)
pd.set_option('display.max_columns', 400)

#Prediction data CSV
data = pd.read_csv('https://raw.githubusercontent.com/nflverse/nfldata/master/data/predictions.csv')

#Game results CSV
full_games_data = pd.read_csv('https://raw.githubusercontent.com/nflverse/nfldata/master/data/games.csv')

#Get median prediction for each game (not including Market)
#Some people also choose to exclude picks that are at 50% (not shown here)
pred_sum = data.loc[(data.screen_name!='Market')].groupby('game_id')[['prediction']].median()

#Market prediction for each game
pred_sum['market'] = data.loc[data.screen_name=='Market'].groupby('game_id')[['prediction']].sum()

#Full games data with results for this season
week_games_sum = full_games_data.loc[full_games_data.season==2021]

#Only keep select columns
week_games_sum = week_games_sum[['game_id','away_team','home_team','result']]

#If result column is > 0 then home team won
week_games_sum['winner'] = week_games_sum['result']
week_games_sum.loc[week_games_sum.result > 0, 'winner'] = week_games_sum.home_team
week_games_sum.loc[week_games_sum.result < 0, 'winner'] = week_games_sum.away_team

#Join to pred_sum
week_games_sum = week_games_sum.merge(pred_sum, left_on='game_id', right_index=True)

#Column for what the median user predicted winner was
week_games_sum['pred_winner'] = np.nan
week_games_sum.loc[week_games_sum.prediction > 50, 'pred_winner'] = week_games_sum.home_team
week_games_sum.loc[week_games_sum.prediction <= 50, 'pred_winner'] = week_games_sum.away_team

#Dataframe with every prediction as a row and the game result
points = data.merge(full_games_data[['game_id','home_team','away_team','week','season','result']],
                    left_on='game_id', right_on='game_id')

#Calculate points result for each prediction
points['pts'] = np.nan

#Formula for points
#M * (25 - (100 * (P/100 - R)^2))

#Neutral pick 50% gets 0 points
points.loc[points.prediction == 50, 'pts'] = 0

#Predicts Home Win, Actual Home Win
points.loc[(points.prediction > 50) & (points.result > 0), 'pts'] = 1 * (25 - (100 * (points.prediction/100 - 1)**2))

#Predicts Home Win, Actual Home Loss
points.loc[(points.prediction > 50) & (points.result < 0), 'pts'] = 1 * (25 - (100 * (points.prediction/100 - 0)**2))

#Create new column for away prediction
points['away_pred'] = np.nan

#Flip away predictions to the other side of 50 (i.e. 30 becomes 70)
points.loc[points.prediction < 50, 'away_pred'] = 100 - points.prediction 

#Predicts Away Win, Actual Away Win
points.loc[(points.away_pred > 50) & (points.result < 0), 'pts'] = 1 * (25 - (100 * (points.away_pred/100 - 1)**2))

#Predicts Away Win, Actual Away Loss
points.loc[(points.away_pred > 50) & (points.result > 0), 'pts'] = 1 * (25 - (100 * (points.away_pred/100 - 0)**2))

#Get each user's points
points.groupby('screen_name')[['pts']].sum().sort_values('pts')

#Get each game's aggregate points won/lost
points.groupby(['game_id','result','home_team','away_team'], as_index=False)[['pts']].sum()