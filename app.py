import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from sqlalchemy.orm import sessionmaker
import sqlalchemy
import sqlite3
from matplotlib import pyplot as plt


app = dash.Dash(__name__)


#
# st.image('media/spotify.png')
# st.title('Spotify ETL & Viz project')
#
# # Use the full page instead of a narrow central column


def get_options_data():
    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("my_played_tracks.sqlite")
    df_new = pd.read_sql_query("SELECT * FROM my_played_tracks", con)
    # Verify that result of SQL query is stored in the dataframe
    print(df_new.head())
    con.close()
    return df_new


# st.markdown('Data table from db')
df_songs = get_options_data()
df_songs
# st.markdown('Artist count')
count = df_songs['artist_name'].value_counts()
new_count = count.reset_index().rename(columns={'index': 'artist', 'artist_name': 'count'})
# count_viz = count.plot.bar(x='artist_name', y='count', rot=0)
new_count.plot(kind="bar")

#
# df_songs = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

fig = px.bar(new_count, x="artist", y="count")

app.layout = html.Div(children=[
    html.H1(children='Spotify ETL & Viz project'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)