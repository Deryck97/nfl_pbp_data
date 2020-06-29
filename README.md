# nfl_pbp_data
Due to API changes made by the NFL, nflscrapR is now broken. nflfastR is the new package for getting NFL play by play data.   

The python script `read_nflfastR.py` will pull in data from nflfastR's data repository, clean in, and output a compressed CSV. 

Cleaning process includes:
* Filtering to only regular season data
* Limit play types to dropbacks, runs, or no_play. This removes punts, kicks, kneels, and spikes.
* Change play types to match what the playcall was, even if there was a penalty. QB scrambles counted as passes.

Any of these cleaning steps can be changed as you see fit.

Check out my guide for using nflfastR in Python [here](https://gist.github.com/Deryck97/dff8d33e9f841568201a2a0d5519ac5e).
