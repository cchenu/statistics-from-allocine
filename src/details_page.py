"""Create a page of the app with films of one category from a graph."""

import streamlit as st

from src.utils import list_films


def create_details_page() -> None:
    """Create the page with films of one category from a graph."""
    if "details_title" in st.session_state:
        title: str = st.session_state["details_title"]

        st.title(title)

        list_films(st.session_state["details_films"], title)


if __name__ == "__main__":
    create_details_page()
