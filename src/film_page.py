"""Create a page of the app with statistic on an actor or a director."""

import math
from typing import TYPE_CHECKING

import streamlit as st

from utils import list_persons

if TYPE_CHECKING:
    from film import Film


def print_stars(rating: float) -> str:
    """
    Create a string with stars corresponding to a rating.

    Parameters
    ----------
    rating : float
        Rating of the film.

    Returns
    -------
    stars : str
        String with corresponding stars.
    """
    if math.isnan(rating):
        return ""
    round_rating = round(rating * 2) / 2
    stars = "★" * int(round_rating)
    if not round_rating.is_integer():
        stars += "⯪"
    stars += "☆" * (5 - len(stars))
    return stars


def create_film_page() -> None:
    """Create the page with information about a film."""
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

        duration = film.get_duration()
        minutes_in_hour = 60
        if duration is None:
            duration_str = ""
        elif duration >= minutes_in_hour:
            duration_str = (
                f"{duration // minutes_in_hour} h "
                f"{duration % minutes_in_hour} min"
            )
        else:
            duration_str = f"{duration} min"

        st.markdown(
            f"""
            Release year: {film.get_year() or ""}<br>
            Duration: {duration_str}<br>
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
        list_persons(directors, f"directors_{film.get_id()}")

    st.markdown("<br>", unsafe_allow_html=True)
    if actors:
        if len(actors) > 1:
            st.header("Actors")
        else:
            st.header("Actor")
        list_persons(actors, f"actors_{film.get_id()}")


if __name__ == "__main__":
    create_film_page()
