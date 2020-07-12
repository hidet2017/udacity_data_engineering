import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries, analize_table_queries


def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()

        
def analize_tables(cur, conn):
    for query in analize_table_queries:
        cur.execute(query)
        results = cur.fetchmany(5)
        
        print('=============TOP 5 songs played by Paid User==============')
        print('=====SongID   /    SongTitle   /   PlayedTimes============')
        
        for result in results:
            print(result)
        
        
        conn.commit()
        
def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)
    analize_tables(cur, conn)
    
    conn.close()


if __name__ == "__main__":
    main()