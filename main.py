import os
import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TOKEN = os.environ.get("OAuthToken")  # auth token from .env file

DATABASE_LOCATION = 'sqlite:///my_played_tracks.sqlite'
USER_ID = '11144361045'

# print(TOKEN)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    context = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN)
    }
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=-1)  # Getting data yesterdays value
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 100

    r = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp),
        headers=context)
    data = r.json()
    if r.status_code != 401:
        song_name = []
        artist_name = []
        played_at_list = []
        timestamps = []

        for item in data['items']:
            song_name.append(item["track"]["name"])
            artist_name.append(item["track"]["album"]["artists"][0]["name"])
            played_at_list.append(item["played_at"])
            timestamps.append(item["played_at"][0:10])

        song_dic = {
            "song_name": song_name,
            "artist_name": artist_name,
            "played_at": played_at_list,
            "timestamp": timestamps,
        }

        df_songs = pd.DataFrame(song_dic, columns=['song_name', 'artist_name', 'played_at', 'timestamp'])
        print(df_songs)
    else:
        print(r.status_code)
        print("Error - Please check that your Token is valid")
