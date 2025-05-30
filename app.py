"""Create a web site with streamlit."""

import pandas as pd
import plotly.express as px
import streamlit as st

from person import Person


def create_site() -> None:
    """
    Create the whole streamlit site.

    Returns
    -------
    None.

    """
    if "person" not in st.session_state:
        st.session_state["person"] = Person(5119)

    home_page = st.Page("home_page.py", title="Films stats")
    create_page = st.Page(
        "actor_page.py", title="Actor stats", url_path="actor"
    )

    pg = st.navigation([home_page, create_page])
    pg.run()


if __name__ == "__main__":
    create_site()
