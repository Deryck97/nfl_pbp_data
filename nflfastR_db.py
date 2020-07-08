import pandas as pd
import sqlite3

pd.options.mode.chained_assignment = None

#Create new database or connect to existing db
con = sqlite3.connect('nflfastR.db')

def create_db():
    """
    Creates a sqlite database for nflfastR play by play data.
    
        Parameters:
            No parameters
            
        Returns:
            No return value
    """

    for i in range(1999,2020):
        link = 'https://github.com/guga31bb/nflfastR-data/blob/master/data/play_by_play_' + \
            str(i) + '.csv.gz?raw=true'

        #Get single season data
        data = pd.read_csv(link, compression='gzip', low_memory=False)

        #Optional cleaning, feel free to remove
        #Filter to regular season
        data = data.loc[data.season_type=='REG']

        #Filter to runs, passes, and plays with penalties
        data = data.loc[(data.play_type.isin(['no_play','pass','run'])) & 
                        (data.epa.isna()==False)]

        #Rename play_type description to match 'pass' and 'rush' column values
        data.play_type.loc[data['pass']==1] = 'pass'
        data.play_type.loc[data.rush==1] = 'run'
        #End of cleaning

        data.reset_index(drop=True, inplace=True)

        #For first season, drop the table if it exists
        if i == 1999:
            data.to_sql(name='plays', con=con, if_exists='replace', index=False)

        else:
            data.to_sql(name='plays', con=con, if_exists='append', index=False)

        print(str(i) + ' data added.')

def update_db(current_season=2019):
    """
    Updates sqlite database by adding games in a specified year that are not 
    currently in the database.
    
    Parameters:
        current_season (int): The season for which data is missing from the database
        
    Returns:
        No reutrn value
    """
    
    #Get game_ids in the db for current year
    query = '''
        SELECT DISTINCT game_id
        FROM plays
        WHERE season=''' + str(current_season)
    
    current_ids = pd.read_sql(query, con)
    
    #Get current year data
    link = 'https://github.com/guga31bb/nflfastR-data/blob/master/data/play_by_play_' + \
                str(current_season) + '.csv.gz?raw=true'

    #Get single season data
    data = pd.read_csv(link, compression='gzip', low_memory=False)

    #Optional cleaning, feel free to remove
    #Filter to regular season
    data = data.loc[data.season_type=='REG']

    #Filter to runs, passes, and plays with penalties
    data = data.loc[(data.play_type.isin(['no_play','pass','run'])) & 
                    (data.epa.isna()==False)]

    #Rename play_type description to match 'pass' and 'rush' column values
    data.play_type.loc[data['pass']==1] = 'pass'
    data.play_type.loc[data.rush==1] = 'run'
    #End of cleaning

    data.reset_index(drop=True, inplace=True)
    
    #Filter out games already in database
    data = data.loc[data.game_id.isin(current_ids.game_id)==False]
    
    if len(data) == 0:
        print('No new games to add.')

    else:
        data.to_sql(name='plays', con=con, if_exists='append', index=False)

        print('New games added.')