import csv
import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import base64 as bs64
import matplotlib.pyplot as plt
import base64
from PIL import Image

image = Image.open("nba.jpeg")

st.title("""
 NBA Player and Team stats Analysis
""")

st.sidebar.header("User input features")

select_year = st.sidebar.selectbox("Year", list(reversed(range(1960, 2024))))

@st.cache

def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url,header=0)
    df = html[0]
    raw = df.drop(df[df.Age=="Age"].index)
    # raw = df
    raw = raw.fillna(0)

    player_stats = raw
    
    return player_stats

player_stats = load_data(select_year)


unique_team = sorted(map(str, player_stats.Tm.unique()))

select_team = st.sidebar.multiselect("Team",unique_team)

unique_position = ["C","PF","SF","PG","SG"]

selected_position = st.sidebar.selectbox("Position", unique_position)

st.header("Display player stats of the selected team(s)")

df_selected_team = player_stats[
    (player_stats["Tm"].isin(select_team)) & (player_stats["Pos"].isin([selected_position]) )
]

st.write("Data dimension: " + str(df_selected_team.shape[0]) + " rows and " + str(df_selected_team.shape[1]) + " columns")

st.dataframe(df_selected_team)


def Download_data(df):
    csv = df.to_csv(index = False)
    bs64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data;file/csv/base64,{bs64}" download="playerstarts.csv">Download CSV file </a>'
    return href

st.markdown(Download_data(df_selected_team),unsafe_allow_html=True)

if st.button('Leaderboard Analysis Click !'):

    st.header('Yearly Team Performance Bar')
    df_selected_team.to_csv('output.csv', index=False)
    df = pd.read_csv('output.csv')

    yearly_performance = df.groupby('Tm')['PTS'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Tm', y='PTS', data=yearly_performance, ax=ax)
    ax.set(xlabel='Team', ylabel='PTS')
    ax.set_title('Team Performance from 2000 to 2023')
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.markdown("George Ngure")



