"""Create a page of the app with statistic on an actor or a director."""

import multiprocessing

import pandas as pd
import streamlit as st

from film import Film
from person import Person


def list_persons(
    persons: list[int],
    role: str,
) -> None:
    """
    List the actors or directors of a film.

    Parameters
    ----------
    persons : list[int]
        List of Allocine's id of the films or a DataFrame with the films.
    role : str
        Role of the persons, for example actors or directors.

    Returns
    -------
    None.

    """
    key = f"film_{role}_{st.session_state["film"].get_id()}"
    if not key in st.session_state:
        df_persons = pd.DataFrame(persons, columns=["id"])
        with multiprocessing.Pool() as pool:
            df_persons["Person"] = pool.map(Person, df_persons["id"])

        df_persons["name"] = df_persons["Person"].apply(Person.get_name)
        df_persons["image"] = df_persons["Person"].apply(Person.get_image)
        st.session_state[key] = df_persons
    df_persons = st.session_state[key]
    cols_per_row = 3
    for i in range(0, len(persons), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(persons):
                with cols[j]:
                    _col1, col2, _col3 = st.columns([0.05, 0.9, 0.05])
                    with col2:
                        button = st.button(
                            df_persons["name"].iloc[i + j],
                            type="secondary",
                            use_container_width=True,
                            key=(
                                f"{role}_{st.session_state["film"].get_id()}"
                                f"_{df_persons['id'].iloc[i + j]}"
                            ),
                        )
                    st.markdown(
                        (
                            "<p style='text-align: center;'><img src='"
                            + df_persons["image"].iloc[i + j]
                            + "' height='200'></p>"
                        ),
                        unsafe_allow_html=True,
                    )

                    if button:
                        st.session_state["person"] = Person(
                            df_persons["id"].iloc[i + j]
                        )
                        st.switch_page("actor_page.py")


def print_stars(rating: float) -> str:
    """Create a string with stars corresponding to a rating.

    Parameters
    ----------
    rating : float
        Rating of the film.

    Returns
    -------
    stars : str
        String with corresponding stars.
    """
    round_rating = round(rating * 2) / 2
    stars = "★" * int(round_rating)
    if not round_rating.is_integer():
        stars += "⯪"
    stars += "☆" * (5 - len(stars))
    return stars


def create_film_page() -> None:
    """
    Create the page with information about a film.

    Returns
    -------
    None.

    """
    film: Film = st.session_state["film"]

    st.title(film.get_title())
    col1, col2 = st.columns([0.3, 0.7])
    with col1:
        st.markdown(
            (
                "<div style='text-align: left;'><img src='"
                + film.get_poster()
                + "' height='200'></div>"
            ),
            unsafe_allow_html=True,
        )

    with col2:
        if len(film.get_countries()) == 1:
            countries_label = "Country"
        else:
            countries_label = "Countries"

        st.markdown(
            f"""
            Release year: {film.get_year()}<br>
            Duration: {film.get_duration()}<br>
            {countries_label}: {", ".join(film.get_countries())}<br>
            Press rating: <span style='color:#FFD700;'>
            {print_stars(film.get_press_rating())}</span><br>
            Spectator rating: <span style='color:#FFD700;'>
            {print_stars(film.get_spectator_rating())}</span>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    directors = film.get_directors()
    actors = film.get_actors()
    if directors:
        if len(directors) > 1:
            st.header("Directors")
        else:
            st.header("Director")
        list_persons(directors, "directors")

    st.markdown("<br>", unsafe_allow_html=True)
    if actors:
        if len(actors) > 1:
            st.header("Actors")
        else:
            st.header("Actor")
        list_persons(actors, "actors")


if __name__ == "__page__":
    create_film_page()
