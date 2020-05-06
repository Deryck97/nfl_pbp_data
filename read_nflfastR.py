import pandas as pd 

#Enter desired years of data
YEARS = [2019,2018,2017]

data = pd.DataFrame()

for i in YEARS:  
    #low_memory=False eliminates a warning
    i_data = pd.read_csv('https://github.com/guga31bb/nflfastR-data/blob/compressed_csvs/' \
                         'data/play_by_play_' + str(i) + '.csv.gz?raw=true',
                         compression='gzip', low_memory=False)

    #sort=True eliminates a warning and alphabetically sorts columns
    data = data.append(i_data, sort=True)