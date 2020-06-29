import pandas as pd 

pd.options.mode.chained_assignment = None

#Enter desired years of data
YEARS = [1999, 2000, 2001, 2002, 2003,
         2004, 2005, 2006, 2007, 2008,
         2009, 2010, 2011, 2012, 2013,
         2014, 2015, 2016, 2017, 2018,
         2019]

for i in YEARS: 
    #Link to data repo 
    link = 'https://github.com/guga31bb/nflfastR-data/blob/master/data/play_by_play_' + str(i) + '.csv.gz?raw=true'
    
    #Read in CSV
    data = pd.read_csv(link, compression='gzip', low_memory=False)

    #Filter to regular season data only
    data = data.loc[data.season_type=='REG']
    
    #Filter to remove kickoffs, punts, field goals, kneels, etc.
    data = data.loc[(data.play_type.isin(['no_play','pass','run'])) & 
                (data.epa.isna()==False)]
    
    #Change play type description to match pass and rush columns
    #QB Scrambles labeled as pass
    data.play_type.loc[data['pass']==1] = 'pass'
    data.play_type.loc[data.rush==1] = 'run'
    
    #Output cleaned, compressed CSV to current directory
    data.to_csv('pbp_' + str(i) + '.csv.gz', index=False, compression='gzip')
    
    print(str(i) + ' data complete.')