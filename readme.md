# Spotify ETL

The aim of this project is to create a date-pipeline (ETL data) from the spotify's API to a SQLite db 
The script has to be executed manually but feel free to host it and make it run every day to get more data

Get your Spotify API token here: https://developer.spotify.com/console/get-recently-played/

Note that this token has to be reactivated every 1h
## How to run it
- You must have python installed
- Use the "cd" command to go to the route of this project
- Install pipenv: 
```
pip install pipenv
```
- Create a virtual environment: 
```
pipenv shell
```
- Install the project dependencies: 
```
pipenv install
```
- Run the project: 
```
python3 main.py
```


