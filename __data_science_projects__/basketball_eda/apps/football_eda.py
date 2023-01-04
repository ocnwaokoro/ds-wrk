import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
## Add functionality to be able to search by player & update the name or have some sort of autofill
def app():
    st.title("NFL Players Stats Explorer")

    st.markdown("""
    This app performs simple web scraping of NBA player stats data!
    * **Python libraries: streamlit, base64, pandas
    * **Data Source: [pro-football-reference.com](https://www.pro-football-reference.com/)
    """)

    selected_year = st.sidebar.selectbox('Year', list(reversed(range(1990,2023))))

    unique_stat = ['Passing','Rushing','Receiving','Scrimmage','Defense','Kicking','Punting','Kick & Punt Returns','Scoring']
    selected_stat = st.sidebar.selectbox('Stat',unique_stat)

    # Web scraping of NBA player stats
    @st.cache(suppress_st_warning=True)
    def load_data(year, selected_stat): 
        if selected_stat in 'Kick & Punt Returns':
            selected_stat = 'Returns'
        stat_ = selected_stat
        url = f"https://www.pro-football-reference.com/years/{year}/{str.lower(stat_)}.htm"
        header = 1
        if(selected_stat in ['Passing','Receiving','Scoring']):
            header = 0
        html = pd.read_html(url, header=header)
        df = html[0]
        raw = df.drop(df[df['Age'] == 'Age'].index)
        raw = df.fillna(0)
        playerstats = raw.drop(['Rk'], axis=1)
        return playerstats

    playerstats = load_data(selected_year,selected_stat)

    # Sidebar for team selection
    sorted_unique_team = sorted(playerstats['Tm'].unique())
    # label: str | options: list | default: list or None
    selected_team = st.sidebar.multiselect('Team',sorted_unique_team,sorted_unique_team)

    # Sidebar for position selection
    unique_position = ['RB', 'QB', 'TE', 'WR', 'FB', 'P', 'S', 'LB', 'OL', 'DB']
    selected_position = st.sidebar.multiselect('Position',unique_position,unique_position)

    # Filtering data
    # important for data wrangling filtration
    df_selected_team = playerstats[(playerstats['Tm'].isin(selected_team)) & (playerstats['Pos'].isin(selected_position))]

    # Add documentation for what each stat means
    # Do so in a file that can be opened in sidebar or new page
    st.header(f'Display {selected_stat} Stats of Selected Team(s)')
    st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
    st.dataframe(df_selected_team)

    # Download NBA player stats data
    def filedownload(df):
        csv = df.to_csv(index=False)
        file = base64.b64encode(csv.encode()).decode() # string <-> bytes conversions
        href = f'<a href="data:file/csv;base64,{file}" download="playerstats.csv">Download CSV File</a>'
        return href

    st.markdown(filedownload(df_selected_team),unsafe_allow_html=True)

    # Remove this
    # Heatmap
    if st.button('Intercorrelation Heatmap'):
        st.header('Intercorrelation Matrix Heatmap')
        df_selected_team.to_csv('output.csv',index=False)
        df = pd.read_csv('output.csv')

        corr = df.corr()
        mask = np.zeros_like(corr)
        mask[np.triu_indices_from(mask)] = True
        with sns.axes_style("dark"):
            f, ax = plt.subplots(figsize=(7, 5))
            ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
        st.pyplot(f)


    ## Create extension which tracks the progress of players throughout their career
    ## Easiest to just graph playoff stats
    ## Do this for football & baseball & see what the differences are