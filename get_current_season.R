library(tidyverse)
library(dplyr)
library(na.tools)
library(nflscrapR)

#Set year to get data
YEAR = 2019

#Check this link to see the most recent week of data it contains
data_url = paste0("https://github.com/ryurko/nflscrapR-data/raw/master/play_by_play_data/regular_season/reg_pbp_",toString(YEAR),".csv")

#Read in the csv 
pbp <- read_csv(url(data_url))

#Get game ids
games <- read_csv("http://www.habitatring.com/games.csv")

#Select weeks(s) needed, to include multiple weeks separate them with |
#For example, filter(season==2019 & (week==4 | week==5)) to get both week 4 and 5
games <- games %>%
  filter(season==2019 & (week==0) & !is.na(result)) %>% 
  mutate(game_id=as.character(game_id))
games_needed <- games %>% pull(game_id)

#Empty dataframe for new plays
new_plays <- NULL

#Get data and add to new_plays for each game
for (i in games_needed)
{
  game_plays <- scrape_json_play_by_play(i)
  new_plays <- bind_rows(new_plays,game_plays)
}

#Combine new week(s) data with old data
pbp_binded <- bind_rows(mutate_all(pbp,as.character),mutate_all(new_plays,as.character))

#Optional cleaning
#Only include plays with EPA not null and no plays, passes, and runs
pbp_rp <- pbp_binded %>% 
  filter(!is_na(epa), play_type=="no_play" | play_type=="pass" | play_type=="run")

#Add columns for rush plays and pass plays as well as success
pbp_rp <- pbp_rp %>%
  mutate(
    pass = if_else(str_detect(desc, "( pass)|(sacked)|(scramble)"), 1, 0),
    rush = if_else(str_detect(desc, "(left end)|(left tackle)|(left guard)|(up the middle)|(right guard)|(right tackle)|(right end)") & pass == 0, 1, 0),
    success = ifelse(epa>0, 1 , 0),
    yards_gained=ifelse(play_type=="no_play",NA,yards_gained)
  )

#If play is marked as rush or pass, change the play_type to match that
pbp_rp$play_type[pbp_rp$pass==1] <- "pass"
pbp_rp$play_type[pbp_rp$rush==1] <- "run"

#Add missing player names 
pbp_players <- pbp_rp %>% 
  mutate(
    passer_player_name = ifelse(play_type == "no_play" & pass == 1, 
                                str_extract(desc, "(?<=\\s)[A-Z][a-z]*\\.\\s?[A-Z][A-z]+(\\s(I{2,3})|(IV))?(?=\\s((pass)|(sack)|(scramble)))"),
                                passer_player_name),
    receiver_player_name = ifelse(play_type == "no_play" & str_detect(desc, "pass"), 
                                  str_extract(desc, 
                                              "(?<=to\\s)[A-Z][a-z]*\\.\\s?[A-Z][A-z]+(\\s(I{2,3})|(IV))?"),
                                  receiver_player_name),
    rusher_player_name = ifelse(play_type == "no_play" & rush == 1, 
                                str_extract(desc, "(?<=\\s)[A-Z][a-z]*\\.\\s?[A-Z][A-z]+(\\s(I{2,3})|(IV))?(?=\\s((left end)|(left tackle)|(left guard)|		(up the middle)|(right guard)|(right tackle)|(right end)))"),
                                rusher_player_name)
  )

#Change old abbreviations to current ones
pbp_all <- pbp_players %>% 
  mutate_at(vars(home_team, away_team, posteam, defteam, penalty_team), funs(case_when(
    . %in% "JAC" ~ "JAX",
    . %in% "STL" ~ "LA",
    . %in% "SD" ~ "LAC",
    TRUE ~ .
  ))) 

#Output csv
#For example 'C:/Users/Name/Documents/play_by_play_2019.csv'
my_path = #Add your desired file path

write.csv(pbp_all,file=my_path,row.names=FALSE)
