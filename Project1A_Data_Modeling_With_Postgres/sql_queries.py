# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
            CREATE TABLE IF NOT EXISTS songplays (\
            songplay_Id SERIAL PRIMARY KEY, \
            userId int NOT NULL, \
            level text, \
            songid text, \
            artistid text, \
            sessionId text, \
            location text, \
            userAgent text);\
                    """)

user_table_create = ("""
            CREATE TABLE IF NOT EXISTS users(\
            user_ID int PRIMARY KEY, \
            first_name text, \
            last_name text, \
            gender text, \
            level text);\
""")

song_table_create = ("""
            CREATE TABLE IF NOT EXISTS songs(\
            song_id text PRIMARY KEY, \
            title text, \
            artist_id text, \
            year int, \
            duration float4);\
            """)

artist_table_create = ("""\
            CREATE TABLE IF NOT EXISTS artists(\
            artist_id text PRIMARY KEY, \
            artist_name text, \
            artist_location text, \
            artist_latitude float4, \
            artist_longitude float4);\
            """)

time_table_create = ("""\
            CREATE TABLE IF NOT EXISTS time(\
            start_time timestamp PRIMARY KEY, \
            hour int, \
            day int, \
            week_of_year int, \
            month int, \
            year int, \
            weekday text);\
            """)

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays\
            (userId, level, songid, artistid, sessionId, location, userAgent) \
            VALUES (%s, %s, %s, %s, %s, %s, %s);\
            """)

user_table_insert = ("""INSERT INTO users\
            (user_ID, first_name, last_name, gender, level) \
            VALUES (%s, %s, %s, %s, %s) \
            ON CONFLICT (user_ID) \
            DO UPDATE SET level = excluded.level;\
            """)

song_table_insert = ("""INSERT INTO songs\
            (song_id, title, artist_id, year, duration) \
            VALUES \
            (%s, %s, %s, %s, %s) \
            ON CONFLICT (song_id) \
            DO NOTHING;""")

artist_table_insert = ("""\
            INSERT INTO artists\
            (artist_id, artist_name, artist_location, artist_latitude, artist_longitude) \
            VALUES (%s, %s, %s, %s, %s) \
            ON CONFLICT (artist_id) \
            DO NOTHING;\
            """)


time_table_insert = ("""\
            INSERT INTO time\
            (start_time, hour, day, week_of_year, month, year, weekday) \
            VALUES (%s, %s, %s, %s, %s, %s, %s) \
            ON CONFLICT (start_time) \
            DO NOTHING;\
            """)

# FIND SONGS

song_select = ("""\
        SELECT song_id, artists.artist_id \
        FROM songs \
        JOIN artists ON songs.artist_id = artists.artist_id \
        WHERE songs.title = %s AND artists.artist_name = %s AND songs.duration = %s\
        """)

# QUERY LISTS

create_table_queries = [song_table_create, artist_table_create, time_table_create, user_table_create, songplay_table_create]
drop_table_queries = [song_table_drop, artist_table_drop, time_table_drop, user_table_drop, songplay_table_drop]
