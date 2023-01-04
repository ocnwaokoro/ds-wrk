import streamlit as st
from multiapp import MultiApp
from apps import basketball_eda, football_eda # import your app modules here

app = MultiApp()

st.markdown("""
## Sports Data
This multi-page app displays sports data for any selected sport.
""")

# Add all your application here
app.add_app("Basketball", basketball_eda.app)
app.add_app("Football", football_eda.app)
# The main app
app.run()


# hockey: {skaters: https://www.hockey-reference.com/leagues/NHL_2023_skaters.html, goalies: https://www.hockey-reference.com/leagues/NHL_2023_goalies.html}
# baseball (not worth it): https://www.baseball-reference.com/leagues/majors/2022-standard-fielding.shtml