"""Create a page of the app with statistic on an actor or a director."""

from typing import TYPE_CHECKING

import streamlit as st

from src.utils import list_films

if TYPE_CHECKING:
    import pandas as pd

    from person import Person


def create_person_page() -> None:
    """Create the page with statistics on an actor or a director."""
    person: Person = st.session_state["person"]
    df_films: pd.DataFrame = st.session_state["df_films"]

    st.title(person.get_name())
    col1, col2 = st.columns([0.3, 0.7])
    with col1:
        st.markdown(
            (
                "<div style='text-align: left;'><img src='"
                + person.get_image()
                + "' height='200'></div>"
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
                    f"directed films watched ({progression * 100:2.1f}%)"
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
                    f"acted-in films watched ({progression * 100:2.1f}%)"
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
            list_films(directed_watched, f"director_{person.get_id()}")
        if len(directed_watched) != len(directed_films):
            directed_not_watched = [
                film
                for film in directed_films
                if film not in directed_watched["id"].astype(int).tolist()
            ]
            st.subheader("Not Watched")
            list_films(directed_not_watched, f"director_{person.get_id()}")

    st.markdown("<br>", unsafe_allow_html=True)
    if played_films:
        if len(played_films) > 1:
            st.header("Acted-in films")
        else:
            st.header("Acted-in film")
        if len(played_watched) > 0:
            st.subheader("Watched")
            list_films(played_watched, f"actor_{person.get_id()}")
        if len(played_watched) != len(played_films):
            played_not_watched = [
                film
                for film in played_films
                if film not in played_watched["id"].astype(int).tolist()
            ]
            st.subheader("Not Watched")
            list_films(played_not_watched, f"actor_{person.get_id()}")


if __name__ == "__main__":
    create_person_page()
