import os
import sys
import re
from ytmusicapi import YTMusic
import json
import pandas as pd

CONF_PATH = 'PATH_TO_CREDENTIALS'

def get_playlists():
    '''
    Retrieve information regarding all custom playlists
    made by the user. Necessary configuration to get access into my account's music data
    are all provided in `conf/headers_auth.json`

    This function is implemented with a purpose to use within Apache Airflow's
    DAG data processing
    '''
    # Global variable / field names
    CONTENT = 'contents'
    TITLE = 'title'
    COUNT = 'count'
    ID = 'playlistId'
    AUTHOR = 'author'
    NAME = 'name'

    # Authentication
    ytmusic = YTMusic(auth=CONF_PATH)

    t = ytmusic.get_library_playlists(limit=30)
    data = {x:[] for x in ['ID', 'Name', 'Num Songs', 'Owner']}

    for playlist in t:
        temp = list()
        try:
            data['Name'].append(playlist[TITLE])
            temp.append('Name')
            data['ID'].append(playlist[ID])
            temp.append('ID')
            data['Num Songs'].append(playlist[COUNT])
            temp.append('Num Songs')
            data['Owner'].append(playlist[AUTHOR].pop()[NAME])
            temp.append('Owner')
        except KeyError:
            for key in temp:
                data[key].pop();
            
            continue;

    track = 1
    alias = 'Playlist: {}'
    for i in range(len(data['Name'])):
        name = data['Name'][i]

        # Check non-ascii characters very first
        if re.search(r'[^\u0000-\u007F]+', name) is not None:
            data['Name'][i] = alias.format(track)
            track+=1
        # Non words/speical characters/whitespace strings
        elif re.search(r'[^\w\s\$,.\'! ]', name) is None:
            continue;
        else:
            data['Name'][i] = alias.format(track)
            track+=1

    df_playlist = pd.DataFrame(data)
    print(df_playlist.head())

    # Operations to load dataset into my database
    return 
