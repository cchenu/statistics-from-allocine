"""Create a page of the app with statistic on an actor or a director."""

import multiprocessing
import random
import string

import pandas as pd
import streamlit as st

from film import Film
from person import Person


def list_films(
    films: list[int] | pd.DataFrame,
    role: str,
) -> None:
    """
    List the films with their Allocine's id, title and poster.

    Parameters
    ----------
    films : list[int] | pd.DataFrame
        List of Allocine's id of the films or a DataFrame with the films.
        Required columns: id, title, press rating, spectator rating, poster.
    role : str
        Role of the persons in the film, for example actor or director.

    Returns
    -------
    None.

    """
    if isinstance(films, list):
        key = f"actor_{role}_{st.session_state["person"].get_id()}"
        if not key in st.session_state:
            df_films = pd.DataFrame(films, columns=["id"])
            with multiprocessing.Pool() as pool:
                df_films["Film"] = pool.map(Film, df_films["id"])

            df_films["title"] = df_films["Film"].apply(Film.get_title)
            df_films["press rating"] = df_films["Film"].apply(
                Film.get_press_rating
            )
            df_films["spectator rating"] = df_films["Film"].apply(
                Film.get_spectator_rating
            )
            df_films["poster"] = df_films["Film"].apply(Film.get_poster)
            df_films = df_films.sort_values(
                by=["spectator rating", "press rating"],
                ascending=[False, False],
            )
            st.session_state[key] = df_films
        else:
            df_films = st.session_state[key]
    else:
        df_films = films

    cols_per_row = 3
    for i in range(0, len(films), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(films):
                with cols[j]:
                    _col1, col2, _col3 = st.columns([0.05, 0.9, 0.05])
                    with col2:
                        button = st.button(
                            df_films["title"].iloc[i + j],
                            type="secondary",
                            use_container_width=True,
                            key=(
                                f"{role}_{st.session_state["person"].get_id()}"
                                f"_{df_films['id'].iloc[i + j]}"
                            ),
                        )
                    st.markdown(
                        (
                            "<p style='text-align: center;'><img src='"
                            + df_films["poster"].iloc[i + j]
                            + "' width='150'></p>"
                        ),
                        unsafe_allow_html=True,
                    )

                    if button:
                        st.session_state["film"] = Film(
                            df_films["id"].iloc[i + j]
                        )
                        st.switch_page("film_page.py")


def create_person_page() -> None:
    """
    Create the page with statistics on an actor or a director.

    Returns
    -------
    None.

    """
    person: Person = st.session_state["person"]
    df_films: pd.DataFrame = st.session_state["df_films"]

    st.title(person.get_name())
    col1, col2 = st.columns([0.3, 0.7])
    with col1:
        st.markdown(
            (
                "<div style='text-align: left;'><img src='"
                + person.get_image()
                + "' width='150'></div>"
            ),
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            (
                '<div style="display: flex; flex-direction: column; '
                'justify-content: center; height: 50px;">'
            ),
            unsafe_allow_html=True,
        )
        directed_films = person.get_directed_films()
        if directed_films:
            directed_watched = df_films[df_films["id"].isin(directed_films)]
            progression = len(directed_watched) / len(directed_films)
            st.progress(
                progression,
                text=(
                    f"{len(directed_watched)} out of {len(directed_films)} "
                    f"directed films watched ({progression*100:2.1f}%)"
                ),
            )

        played_films = person.get_played_films()
        if played_films:
            played_watched = df_films[df_films["id"].isin(played_films)]
            progression = len(played_watched) / len(played_films)
            st.progress(
                progression,
                text=(
                    f"{len(played_watched)} out of {len(played_films)} "
                    f"acted-in films watched ({progression*100:2.1f}%)"
                ),
            )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if directed_films:
        if len(directed_films) > 1:
            st.header("Directed films")
        else:
            st.header("Directed film")
        if len(directed_watched) > 0:
            st.subheader("Watched")
            list_films(directed_watched, "director")
        if len(directed_watched) != len(directed_films):
            directed_not_watched = [
                film
                for film in directed_films
                if film not in directed_watched["id"].astype(int).tolist()
            ]
            st.subheader("Not Watched")
            list_films(directed_not_watched, "director")

    st.markdown("<br>", unsafe_allow_html=True)
    if played_films:
        if len(played_films) > 1:
            st.header("Acted-in films")
        else:
            st.header("Acted-in film")
        if len(played_watched) > 0:
            st.subheader("Watched")
            list_films(played_watched, "actor")
        if len(played_watched) != len(played_films):
            played_not_watched = [
                film
                for film in played_films
                if film not in played_watched["id"].astype(int).tolist()
            ]
            st.subheader("Not Watched")
            list_films(played_not_watched, "actor")


if __name__ == "__main__":
    create_person_page()
