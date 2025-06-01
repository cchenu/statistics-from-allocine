"""Create a web site with streamlit."""

import pandas as pd
import streamlit as st

from create_csv import create_csv
from person import Person


def create_site() -> None:
    """
    Create the whole streamlit site.

    Returns
    -------
    None.

    """
    if "df_films" not in st.session_state:
        create_csv()
        df_films = pd.read_csv("csv/films.csv")
        st.session_state["df_films"] = df_films

    if "person" not in st.session_state:
        st.session_state["person"] = Person(5119)

    home_page = st.Page("home_page.py", title="Films stats")
    actor_page = st.Page(
        "actor_page.py", title="Actor stats", url_path="actor"
    )

    pg = st.navigation([home_page, actor_page], position="hidden")
    pg.run()


if __name__ == "__main__":
    create_site()
