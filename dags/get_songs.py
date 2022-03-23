import os
import sys
import re
from ytmusicapi import YTMusic
import json
import pandas as pd
from datetime import datetime

ROOT = ...
CONF_PATH = ...

def get_songs():
    '''
    Retrieve the songs most recently played on my YoutubeMusic account
    Necessary configuration to get access into my account's music data
    are all provided in `conf/headers_auth.json`

    With provided configurations, the function access into YTMusic APIs
    retrieving my recent music listening history

    This function is implemented with a purpose to use within Apache Airflow's
    DAG data processing
    '''
    # Authorization into my YTMusic account
    ytmusic = YTMusic(auth=CONF_PATH)

    song_history = ytmusic.get_history()
    keys = [
        'ID',
        'Title',
        'Artist',
        'Album',
        'Duration',
        'Played on'
    ]
    data =  {key:[] for key in keys}

    # Retrieve information of only those songs with formal description
    for song in song_history:
        temp = list()
        try:
            data['ID'].append(song['videoId'])
            temp.append('ID')
            data['Title'].append(song['title'])
            temp.append('Title')
            if isinstance(song['artists'], list):
                data['Artist'].append(song['artists'].pop()['name'])
            else:
                data['Arist'].append(song['artists']['name'])
            temp.append('Artist')

            if isinstance(song['album'], list):
                data['Album'].append(song['album'].pop()['name'])
            else:
                data['Album'].append(song['album']['name'])
            temp.append('Album')

            data['Duration'].append(song['duration'])
            temp.append('Duration')
            data['Played on'].append(song['played'])
            temp.append('Played on')
        except:
            for key in temp:
                if len(data[key]) == 0:
                    continue;
                data[key].pop();
            
            continue;
    
    assert len(set([len(x[1]) for x in data.items()])) == 1, 'Inconsistent retrieval of data from YTMusic API'
    t = datetime.now()
    date = (
        str(t.year),
        str(t.month).rjust(2, '0'),
        str(t.day).rjust(2, '0')
    )
    file_name = f'data/ytmusic_listening_history[{date[0]}-{date[1]}-{date[-1]}].json'
    fp = os.path.join(ROOT, file_name)

    with open(fp, 'w') as f:
        json.dump(data, f, indent=4);
    print(fp)

    return