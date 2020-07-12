# Project: Data Modeling with Postgres

## Summary of The Project
  - The startup company *Sparkify* has two data set.
    - Log Data : Their customer behavior log data 
    - Million Song Data : Data of well-sold songs, public data
  - We launched the database for their business analysis by combining Log-data and public song data. After this, we can understand several relationship between customer-behavior and song. For example, analyzing what type of songs will contribute their **paid** user acquisition.

## Files in Repository
File | Functions
------------ | -------------
create_tables.py | drops and creates tables.
etl.py | reads and processes files from song_data and log_data and loads them into tables.
etl.ipynb | detail steps and explanation of etl.py.
sql_queries.py  |   contains all your sql queries, and is imported into create_tables.py, etl.py and etl.ipynb.
test.ipynb | check whether table created and data inserted

## Database schema

### Fact Table
Table : songplays

column | type | notes
------------ | ------------- | -------------
songplay_Id(PRIMARY KEY) |  SERIAL | ID allocated for each song_play by usersuserId | int | set NOT NULL condition, ID of each userlevel | varchar | user contract lever(paid or free)songid | varchar | ID of each song
artistid | varchar | ID of each artist
sessionId | varchar | ID of each service usage session
location | varchar | The location where users connected
userAgent | varchar | The agent ID users use to connect this service 


### Dimension Table
Table : songs

column | type | notes
------------ | ------------- | -------------
song_id(PRIMARY KEY) | varchar | ID of each song
title | varchar | song title
artist_id | varchar | artist ID of each song
year | int | the year the song published
duration | float4 | song's duration

Tables : artists

column | type | notes
------------ | ------------- | -------------
artist_id(PRIMARY KEY) | varchar | ID of each artist
artist_name | varchar | artist's first name
artist_location | varchar | artist location 
artist_latitude | float4 | artist location's latitude
artist_longitude | float4 | artist location's longitude

Table : time

column | type | notes
:------------ | :------------- | :-------------
start_time(PRIMARY KEY) | timestamp | the time the song was played 
hour | int |  the hour the song was played 
day | int |  the hour the song was played 
week_of_year | int | the week of year the song was played 
month | int | the month of year the song was played 
year | int | year of the song was played 
weekday | varchar | weekday of the song was played 
</div>

Table : users

column | type | notes
------------ | ------------- | -------------
user_ID(PRIMARY KEY) | varchar | ID for each user
first_name | varchar | user's first name
last_name | varchar | user's last name
gender | varchar | gender of the user
level | varchar | user contract lever(paid or free)

## ETL Process

0.Create the tables/database at Postgres
  -Database name:sparkifydb
  -Tables name:songplays, songs, artists, time, users


1.Extract:Download data from "Million song database"
 (http://millionsongdataset.com/)
 
2.Transform : Normalizing the data(by song and by artist)

3.Load : Insert the data into songs table and artists table


4.Extract:Download Sparkify's behavior log-data

5.Transform:Normalizing the data(by time and by user)
  -We register several time data(hour, weekday, month, week of year,...)

6.Load : Insert the data into time table and users table


7.Transform : Combining the log-data with song data and artist data

8.Load : Insert the data into song_plays table

## How to run the python scripts

1.python create_tables.py
  - Drop database/tables if they still exist
  - Create database/tables for data-insert

2.python etl.py
  - Extract the data from "Million song database" and internal log data
  - Transform and insert those data into tables