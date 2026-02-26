"""Create a web site with streamlit."""

import streamlit as st

from src.film import Film
from src.person import Person
from src.utils import SRC_DIR


def create_site() -> None:
    """Create the whole streamlit site."""
    if "person" not in st.session_state:
        st.session_state["person"] = Person(5119)

    if "film" not in st.session_state:
        st.session_state["film"] = Film(9684)

    for role in ("directors", "actors"):
        if f"number_{role}" not in st.session_state:
            st.session_state[f"number_{role}"] = 9

    if "number_films" not in st.session_state:
        st.session_state["number_films"] = 3

    home_page = st.Page(SRC_DIR / "home_page.py", title="Films stats")
    actor_page = st.Page(
        SRC_DIR / "actor_page.py", title="Actor stats", url_path="actor"
    )
    film_page = st.Page(
        SRC_DIR / "film_page.py", title="Film page", url_path="film"
    )
    details_page = st.Page(
        SRC_DIR / "details_page.py", title="Details", url_path="details"
    )
    token_page = st.Page(
        SRC_DIR / "token_page.py", title="Token", url_path="token"
    )

    pg = st.navigation(
        [home_page, actor_page, film_page, details_page, token_page],
        position="hidden",
    )
    pg.run()


if __name__ == "__main__":
    create_site()
