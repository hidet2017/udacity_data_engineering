# Project: Data Warehouse

## Summary of The Project
  - The startup company *Sparkify* has two data set.
    - Log Data : Their customer behavior log data 
    - Song Data : Data of well-sold songs, public data
  - We will set star-scheme database for analyzing their business.
  - We will set up database in AWS Redshift and will be able to analyze by postgreSQL.

## Files in Repository
File | Functions
------------ | -------------
AWS_Setup.ipynb | Create clients for IAM, EC2, S3 and Redshift / Create an IAM Role that makes Redshift able to access S3 bucket (ReadOnly) /Create a RedShift Cluster
create_tables.py | drops and creates tables.
sql_queries.py  |   contains all your sql queries, and is imported into create_tables.py, and etl.py.
etl.py | reads and processes files from song_data and log_data and loads them into tables.



## ETL Process

##### 1.AWS
  - 1a.Aquire AWS secret and access key
  - 1b.Create clients for IAM, EC2, S3 and Redshift
  - 1c.Create an IAM Role that makes Redshift able to access S3 bucket (ReadOnly)
  - 1d.Create a RedShift Cluster

##### 2.Create Tables
  - 2a.Create staging tabes to copy data from s3 to Redshift
  - 2b.Create fact and dimension tables

##### 3.Extract, Transfer, Load the data
  - 3a.Copy the data from s3 to staging tables(staging_events / staging_songs)
  - 3b.Extract the data from stating tables
  - 3c.Transfer/load the extracted data for the fact/demension tables

#####  (Option)4.Analyze the data
  - 4a.Counting the plaeyd times by paid user for each song_ID
  - 4b.Match the song_title for song_ID
  - 4c.Show the top 5 of played songs


## How to run the python scripts

#####  1.python create_tables.py
  - Drop database/tables if they still exist
  - Create database/tables for data-insert

#####  2.python etl.py
  - Copy the data from s3(song data and log data) to staging tables
  - Transform and insert those data into fact/dimension tables
  - Analyze the songplay data and identyfy the song which contributes sales


## Database schema

### Staging Table

Table : staging_events


column | type | notes
------------ | ------------- | -------------
artist(sortkey) | text | ID of each artist
auth | text | auther of each song
firstName | text | user's first name
gender | text | gender of the user
iteminsession | bigint | orders of the played song in the session
level | text | user contract level(paid or free)
lastName | text | user's last name
length | float4 | length of the played song
location | text | location of the user
method | text | the method user played
page | text | the page of song
registration | float4 | the period of registration
sessionid | bigint | ID of session
song(distkey) | text | the title of played song
status | text | the status of playing song
ts | bigint | time the song played
useragent | text | agent the user connected to the service
userid | text | ID of each user



Table : staging_songs

column | type | notes
------------ | ------------- | -------------
artist_id| text | ID of each artist
artist_location | text | artist location 
artist_latitude | float4 | artist location's latitude
artist_longitude | float4 | artist location's longitude
artist_name(sortkey) | text | artist's name
duration | float4 | the duration of the song 
num_songs | bigint | the number of song it contains
song_id | text | ID of each song 
title(distkey) | text | the song name 
year  | int | the year the song published


### Fact Table

Table : songplay

column | type | notes
------------ | ------------- | -------------
songplay_Id | bigint IDENTITY(0,1) | ID of each playing song session
userId | text | ID of each user
level | text | user contract level(paid or free)
songid(distkey) | text | ID of each song
artistid(sortkey)  | text | ID of each artist
sessionId | bigint | ID of session
location | text | location of the user
userAgent | text | agent the user connected to the service


### Dimention Table

Table : users

column | type | notes
------------ | ------------- | -------------
userId(sortkey) | text | ID of each user
firstName | text | user's first name
lastName | text | user's last name
gender | text | gender of the user
level | text | user contract level(paid or free)


Table : song

column | type | notes
------------ | ------------- | -------------
song_id(sortkey) | text | ID of each song
title | text | the song name
artist_id | text | ID of each artist
year | int | artist the year the song published
duration | float4 | the duration of the song


Table : artist

column | type | notes
------------ | ------------- | -------------
artist_id | text | ID of each artist
artist_name | text | artist's name
artist_location | text | artist location
artist_latitude | float4 | artist location's latitude
artist_longitude | float4 | artist location's longitude


Table : time

column | type | notes
------------ | ------------- | -------------
start_time | timestamp | the time song started to play
hour | int | the hour song started to play
day | int | the day song started to play
week | int | the week song started to play
month | int | the month song started to play
year | int | the year song started to play
weekday | int | the weekday song started to play
