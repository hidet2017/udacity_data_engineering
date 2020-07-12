import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_song"
songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS song"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create = ("""
            CREATE TABLE IF NOT EXISTS staging_events(\
            artist text, \
            auth text, \
            firstName text, \
            gender text, \
            itemInSession int, \
            lastName text, \
            length float4, \
            level text, \
            location text, \
            method text, \
            page text distkey, \
            registration float4, \
            sessionId bigint, \
            song text sortkey, \
            status text, \
            ts bigint, \
            userAgent text, \
            userId text
            );\
            """)

staging_songs_table_create = ("""
            CREATE TABLE IF NOT EXISTS staging_songs(\
            artist_id text, \
            artist_latitude float4, \
            artist_location text, \
            artist_longitude float4, \
            artist_name text sortkey, \
            duration float4, \
            num_songs int, \
            song_id text, \
            title text distkey, \
            year int
            );\
            """)


songplay_table_create = ("""
            CREATE TABLE IF NOT EXISTS songplay(\
            songplay_Id bigint IDENTITY(0,1), \
            start_time bigint, \
            userId text, \
            level text, \
            songid text distkey, \
            artistid text sortkey, \
            sessionId bigint, \
            location text, \
            userAgent text);\
            """)

user_table_create = ("""
            CREATE TABLE IF NOT EXISTS users(\
            userId text sortkey, \
            firstName text, \
            lastName text, \
            gender text, \
            level text            
            );\
            """)

song_table_create = ("""
            CREATE TABLE IF NOT EXISTS song(\
            song_id text sortkey, \
            title text, \
            artist_id text, \
            year int, \
            duration float4
            );\
            """)

artist_table_create = ("""
            CREATE TABLE IF NOT EXISTS artist(\
            artist_id text sortkey, \
            artist_name text, \
            artist_location text, \
            artist_latitude float4, \
            artist_longitude float4
            );\
            """)

time_table_create = ("""
            CREATE TABLE IF NOT EXISTS time(\
            start_time timestamp, \
            hour int, \
            day int, \
            week int, \
            month int, \
            year int, \
            weekday int
            );\
            """)


# STAGING TABLES

staging_events_copy = ("""
        copy staging_events from {} 
        credentials 'aws_iam_role={}'
        region 'us-west-2'
        COMPUPDATE OFF
        JSON {};
        """).format(config.get('S3','LOG_DATA'), config.get('IAM_ROLE','ARN'), config.get('S3','LOG_JSONPATH'))


staging_songs_copy = ("""
        copy staging_songs from {} 
        credentials 'aws_iam_role={}'
        region 'us-west-2'
        COMPUPDATE OFF
        JSON 'auto';
        """).format(config.get('S3','SONG_DATA'), config.get('IAM_ROLE','ARN'))


# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplay
    (start_time, userId, level, songid, artistid, sessionId, location, userAgent) \
    select e.ts, e.userId, e.level, s.song_id, s.artist_id, e.sessionId, e.location, e.userAgent \
    from staging_events e
    join staging_songs s
    on s.title = e.song and s.artist_name = e.artist
    where e.page = 'NextSong'
    """)


user_table_insert = ("""
    INSERT INTO users\
    (userId, firstName, lastName, gender, level  )\
    select DISTINCT userId, firstName, lastName, gender, level \
    from staging_events
    where userID is not NULL
    """)


song_table_insert = ("""
    INSERT INTO song\
    (song_id, title, artist_id, year, duration)\
    select DISTINCT song_id, title, artist_id, year, duration \
    from staging_songs
    """)

artist_table_insert = ("""
    INSERT INTO artist\
    (artist_id, artist_name, artist_location, artist_latitude, artist_longitude )\
    select DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude \
    from staging_songs
    """)



time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT DISTINCT a.start_time,
    EXTRACT (HOUR FROM a.start_time), EXTRACT (DAY FROM a.start_time),
    EXTRACT (WEEK FROM a.start_time), EXTRACT (MONTH FROM a.start_time),
    EXTRACT (YEAR FROM a.start_time), EXTRACT (WEEKDAY FROM a.start_time) FROM
    (SELECT TIMESTAMP 'epoch' + start_time/1000 *INTERVAL '1 second' as start_time FROM songplay) a;
    """)

# Analize Tables
analize_table = ("""
    SELECT playedresult.songid, songdata.title, playedresult.playedbypaid
    FROM(SELECT songid, count(songid) as playedbypaid \
    from songplay \
    where level = 'paid' \
    group by songid \
    order by playedbypaid desc\
    limit 5) playedresult\
    Left JOIN(SELECT song_id, title\
    FROM song\
    GROUP By song_id, title\
    ) songdata\
    on songdata.song_id=playedresult.songid\
    order by playedbypaid desc
    ;
    """)


# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [song_table_insert, songplay_table_insert, time_table_insert, artist_table_insert, user_table_insert]
copy_table_queries = [staging_events_copy, staging_songs_copy]
analize_table_queries = [analize_table]

