import os
import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
import datetime
import sqlite3
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Get your Token here: https://developer.spotify.com/console/get-recently-played/
TOKEN = os.environ.get("OAuthToken")  # auth token from .env file
USER_ID = os.environ.get("USER_ID")  # No need for this data

DATABASE_LOCATION = 'sqlite:///my_played_tracks.sqlite'


def is_data_valid(df: pd.DataFrame) -> bool:
    # True or false
    if df.empty:
        print("There is no data in your df - Check if you have played a song recently in your Spotify Account")
        return False
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Primary key is not unique")

    # Null values check
    if df.isnull().values.any():
        raise Exception("Null value found, please check the dataframe")

    # TimeStrap date must be from yesterday's date
    # yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    # yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    #
    # timestamps = df["timestamp"].tolist()
    # for timestamp in timestamps:
    #     if datetime.datetime.strptime(timestamp, '%Y-%m-%d') != yesterday:
    #         raise Exception("At least one of the returned songs does not have a yesterday's timestamp")

    return True


if __name__ == '__main__':
    context = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN)
    }
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)  # Getting data yesterdays value
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    r = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp),
        headers=context)
    data = r.json()
    if r.status_code != 401:
        song_name = []
        artist_name = []
        played_at_list = []
        day = []
        time = []

        for item in data['items']:
            song_name.append(item["track"]["name"])
            artist_name.append(item["track"]["album"]["artists"][0]["name"])
            played_at_list.append(item["played_at"])
            day.append(item["played_at"][0:10])
            time.append(item["played_at"][12:19])

        song_dic = {
            "song_name": song_name,
            "artist_name": artist_name,
            "played_at": played_at_list,
            "day": day,
            "time": time,
        }

        df_songs = pd.DataFrame(song_dic, columns=['song_name', 'artist_name', 'played_at', 'day', 'time'])

        # Validate date
        if is_data_valid(df_songs):
            print("Data Valid - Load stage")

            # Load Data to DB
            engine = sqlalchemy.create_engine(DATABASE_LOCATION)
            conn = sqlite3.connect('my_played_tracks.sqlite')
            cursor = conn.cursor()

            sql_query = """ 
            CREATE TABLE IF NOT EXISTS my_played_tracks(
            song_name VARCHAR(200),
            artist_name VARCHAR(200),
            played_at VARCHAR(200),
            day VARCHAR(200),
            time VARCHAR(200),            
            CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
            )
            """
            cursor.execute(sql_query)
            print("Opened database successfully")

            try:
                df_songs.to_sql("my_played_tracks", engine, index=False, if_exists='append')
            except:
                print("Data already exists in the database")

            conn.close()
            print("Close database successfully")

        else:
            print("Data was not valid, please debug")

    else:
        print(r.status_code)
        raise Exception('Error - Please check that your Token is valid')

