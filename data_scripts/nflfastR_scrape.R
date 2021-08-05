library(tidyverse)
library(nflfastR)

#Specify season
season = 2020

#Get game ids
game_ids <- fast_scraper_schedules(season) %>% 
  filter(game_type=='REG') %>% 
  pull(game_id)

#Scrape Data
pbp <- fast_scraper(game_ids, pp=TRUE)

#Apply cleaning function
cleaned_pbp <- clean_pbp(pbp)

cleaned_pbp_qbepa <- add_qb_epa(cleaned_pbp)

#Optional - Change play types to match if pass or rush == 1
cleaned_pbp_qbepa$play_type[cleaned_pbp$pass==1] <- "pass"
cleaned_pbp_qbepa$play_type[cleaned_pbp$rush==1] <- "run"

#Put file path in quotes (C:/Users/Name/Documents/pbp_2020.csv.gz)
#Use file extension .csv.gz for a compressed CSV
my_path = paste0('FILE PATH')

write.csv(cleaned_pbp_qbepa, file=gzfile(my_path), row.names=FALSE)