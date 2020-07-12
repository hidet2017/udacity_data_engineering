import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, conn, filepath):
    """
    - Read the song data file downloaded from Million Song Data
      (http://millionsongdataset.com/index.html)
    - Extract song data and artist data
    - Insert those data into song/artist table
    """
    
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']]
    songs_data_loc = song_data.loc[:,['song_id','title','artist_id','year','duration']].values.tolist()
    cur.execute(song_table_insert, songs_data_loc[0])
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']]
    artist_data_loc = artist_data.values.tolist()
    cur.execute(artist_table_insert, artist_data_loc[0])


def process_log_file(cur, conn, filepath):
    """
    - Read the user behavior log data file 
    - Extract timestamp and transform it into hour, day, week of year, month, year, weekday data
    - Insert those data into time table
    - Extract user data
    - Insert those data into users table
    - Combine the log data with song/artist data
    - Insert the data into songplays table
    """
    
    
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    df['timestamp'] = pd.to_datetime(df['ts'],unit='ms')
    df['hour']=df['timestamp'].dt.hour
    df['day']=df['timestamp'].dt.day
    df['week_of_year']=df['timestamp'].dt.week
    df['month']=df['timestamp'].dt.month
    df['year']=df['timestamp'].dt.year
    df['weekday']=df['timestamp'].dt.weekday_name
    
    # insert time data records 
    time_df = df[['timestamp','hour','day','week_of_year','month','year','weekday']]

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]
    user_df = user_df.drop_duplicates(subset='userId')

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record

        songplay_data = (row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)
        

def process_data(cur, conn, filepath, func):
    """
    - Read the json files from identified path
    """
    
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, conn, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()