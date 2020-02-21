# nfl_pbp_data
Script for getting new nflscrapR data. Be sure to read all the comments and change numbers as needed.

Both R scripts include cleaning, which can be removed if desired. The Jupyter Notebook will grab a season of data from github and clean it as well.

Cleaning process includes:
* Limit play types to dropbacks, runs, or no_play. This removes punts, kicks, kneels, and spikes.
* Add success field. If EPA of a play is greater than 0, the play is a success.
* Add 'rush' and 'pass' field as binary (0 or 1) variables.
* Add missing player names for who passed/rushed/received the ball.
* Change play types to match what the playcall was, even if there was a penalty. QB scrambles counted as passes.
* Update team abbreviations for uniformity over multiple years, changes JAC to JAX, STL to LA, and SD to LAC.

Credit to [@LeeSharpeNFL](https://twitter.com/LeeSharpeNFL) and [@benbbaldwin](https://twitter.com/benbbaldwin) who's code I used in part of this script for getting new data and cleaning it. 

Check out my guide for using nflscrapR in Python [here](https://gist.github.com/Deryck97/fa4abc0e66b77922634be9f51f9a1052).
