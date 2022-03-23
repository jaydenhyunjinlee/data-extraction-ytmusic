from datetime import datetime
import string
import json
import os
import sys
import psycopg2
import re

def load_songs():
    '''
    This function loads and stores extracted YTMusic listening history data
    as a relation, or entity set, in PostgreSQL server
    Newly retrieved data will get stored in new tables structured at every time 
    the data is generated from YTMusic API
    '''
    today = datetime.now()
    year = str(today.year)
    month = str(today.month).rjust(2, '0')
    day = str(today.day).rjust(2, '0')
    with open(f'data/ytmusic_listening_history[{year}-{month}-{day}].json', 'r') as f:
        content = json.load(f)
        N = len(list(content.values())[0])

    conn = psycopg2.connect( # Postgres database access credentials
        dbname=...,
        user=...,
        password=...,
        host=...,
        port=...
    )
    # conn.autocommit = True
    cursor = conn.cursor()
    print(conn.closed) # Prints 0 if connection established

    # That case, I wouldn't want the relation to reset at every run over the dady
    # We want to check if the table exists in database already and if so, update the table with new values
    # Use bool(cursor.execute(<query>).rowcount) for checking
    tbl_name = f'songs_{year}_{month}_{day}' # Name of relation in which to store today's listening history
    tbl_name = "'" + tbl_name + "'" # Syntax purpose
    # Check if the table already exists
    check_table = f"SELECT * FROM information_schema.tables WHERE table_name={tbl_name}"
    cursor.execute(check_table);
    present = cursor.rowcount # If table exists, command returns non-zero integer, or 1

    if not (present > 0): # If table doesn't exist, create a table for today first
        tbl_name = tbl_name.strip("'")
        drop_table = f'DROP TABLE IF EXISTS {tbl_name} CASCADE'
        create_table = '''CREATE TABLE IF NOT EXISTS {tbl_name} (\
        row_number SERIAL, \
        song_id VARCHAR(100), \
        song_name VARCHAR(100), \
        artist_name VARCHAR(100), \
        album_name VARCHAR(100), \
        duration VARCHAR(10), \
        played_on VARCHAR(20) \
        )
        '''.format(tbl_name=tbl_name)

        cursor.execute(drop_table);
        cursor.execute(create_table);

    pattern_matcher = '[' + string.punctuation + ']'
    insert_values = '''
    INSERT INTO {table} (song_id, song_name, artist_name, album_name, duration, played_on) \
    VALUES {sql}
    '''
    for i in range(N):
        song_id = content['ID'][i]
        song_name = content['Title'][i]
        song_name = re.sub(pattern_matcher, '', song_name) # Get rid of characters incompatible with PostgreSQL

        artist_name = content['Artist'][i]
        artist_name = re.sub(pattern_matcher, '', artist_name)

        album_name = content['Album'][i]
        album_name = re.sub(pattern_matcher, '', album_name)

        duration = content['Duration'][i]
        played_on = content['Played on'][i]
        vals = (song_id, song_name, artist_name, album_name, duration, played_on)

        statement = insert_values.format(table=tbl_name, sql=vals)
        try:
            cursor.execute(statement)
        except:
            print('Not Good')
            continue;

    conn.commit();
    conn.close();
