"""Utility functions to display films and persons in Streamlit."""

import multiprocessing

import pandas as pd
import streamlit as st

from film import Film
from person import Person


def list_films(
    films: list[int] | pd.DataFrame,
    source: str,
) -> None:
    """
    List the films with their Allocine's id, title and poster.

    Parameters
    ----------
    films : list[int] | pd.DataFrame
        List of Allocine's id of the films or a DataFrame with the films.
        Required columns: id, title, press rating, spectator rating, poster.
    source : str
        Source of the call, used as key in session state and in button.

    Returns
    -------
    None.

    """
    if isinstance(films, list):
        if source not in st.session_state:
            df_films = pd.DataFrame(films, columns=["id"])
            with multiprocessing.Pool() as pool:
                df_films["Film"] = pool.map(Film, df_films["id"])

            df_films["title"] = df_films["Film"].apply(Film.get_title)
            df_films["press rating"] = df_films["Film"].apply(
                Film.get_press_rating,
            )
            df_films["spectator rating"] = df_films["Film"].apply(
                Film.get_spectator_rating,
            )
            df_films["poster"] = df_films["Film"].apply(Film.get_poster)
            df_films = df_films.sort_values(
                by=["spectator rating", "press rating"],
                ascending=[False, False],
            )
            st.session_state[source] = df_films
        else:
            df_films = st.session_state[source]
    else:
        df_films = films

    cols_per_row = 3

    for i in range(0, len(df_films), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(df_films):
                with cols[j]:
                    _, col2, _ = st.columns([0.05, 0.9, 0.05])
                    with col2:
                        button = st.button(
                            df_films["title"].iloc[i + j],
                            type="secondary",
                            use_container_width=True,
                            key=(f"{source}_{df_films['id'].iloc[i + j]}"),
                        )
                    st.markdown(
                        (
                            "<p style='text-align: center;'><img src='"
                            + df_films["poster"].iloc[i + j]
                            + "' height='200'></p>"
                        ),
                        unsafe_allow_html=True,
                    )

                    if button:
                        st.session_state["film"] = Film(
                            df_films["id"].iloc[i + j],
                        )
                        st.switch_page("src/film_page.py")


def list_persons(
    persons: list[int] | pd.DataFrame,
    source: str,
) -> None:
    """
    List the actors or directors of a film.

    Parameters
    ----------
    persons : list[int] | pd.DataFrame
        List of Allocine's id of the persons or a DataFrame with the persons.
        Required columns: id, name, image. Column number is required if home is
        in source.
    source : str
        Source of the call, used as key in session state and in button.

    Returns
    -------
    None.

    """
    df_persons: pd.DataFrame
    if "home" in source or source not in st.session_state:
        if isinstance(persons, list):
            df_persons = pd.DataFrame(persons, columns=["id"])
        else:
            df_persons = persons.copy()
            if source in st.session_state:
                df_persons = df_persons.merge(
                    st.session_state[source][["id", "Person"]],
                    on="id",
                    how="left",
                )
        if "Person" not in df_persons:
            with multiprocessing.Pool() as pool:
                df_persons["Person"] = pool.map(Person, df_persons["id"])
        elif len(df_persons[df_persons["Person"].isna()]) > 0:
            with multiprocessing.Pool() as pool:
                df_persons.loc[df_persons["Person"].isna(), "Person"] = (
                    pool.map(
                        Person,
                        df_persons.loc[df_persons["Person"].isna(), "id"],
                    )
                )

        df_persons["name"] = df_persons["Person"].apply(Person.get_name)
        df_persons["image"] = df_persons["Person"].apply(Person.get_image)
        if source in st.session_state and (
            len(df_persons) > len(st.session_state[source])
            or source not in st.session_state
        ):
            st.session_state[source] = df_persons
    else:
        df_persons = st.session_state[source]
    cols_per_row = 3
    for i in range(0, len(df_persons), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(df_persons):
                with cols[j]:
                    _, col2, _ = st.columns([0.05, 0.9, 0.05])
                    with col2:
                        button = st.button(
                            df_persons["name"].iloc[i + j],
                            type="secondary",
                            use_container_width=True,
                            key=(f"{source}_{df_persons['id'].iloc[i + j]}"),
                        )

                    tag = "div" if "home" in source else "p"
                    st.markdown(
                        (
                            f"<{tag} style='text-align: center;'><img src='"
                            + df_persons["image"].iloc[i + j]
                            + f"' height='200'></{tag}>"
                        ),
                        unsafe_allow_html=True,
                    )
                    if "home" in source:
                        st.markdown(
                            (
                                "<p style='text-align: center;'>"
                                + str(df_persons["number"].iloc[i + j])
                                + " films</p>"
                            ),
                            unsafe_allow_html=True,
                        )

                    if button:
                        st.session_state["person"] = Person(
                            df_persons["id"].iloc[i + j],
                        )
                        st.switch_page("src/actor_page.py")
