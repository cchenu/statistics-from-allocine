"""Create a page of the app with statistic on an actor or a director."""

import dotenv
import streamlit as st

from src.utils import SRC_DIR


def submit() -> None:
    """Submit new tokens."""


def create_token_page() -> None:
    """Create the page to update Allocine tokens."""
    st.title("Token update")
    error: str = st.session_state["token_error"]
    id_input, token_input = "", ""
    if "ID" in error:
        id_input = st.text_input("Enter the collection ID:", key="id")
    if "token" in error:
        token_input = st.text_input("Enter your token:", key="token")

    button = st.button("Submit")

    if id_input or token_input or button:
        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)

        if "id" in st.session_state:
            dotenv.set_key(dotenv_file, "ID", st.session_state["id"], "never")

        if "token" in st.session_state:
            dotenv.set_key(
                dotenv_file, "TOKEN", st.session_state["token"], "never"
            )

        st.switch_page(SRC_DIR / "home_page.py")()


if __name__ == "__main__":
    create_token_page()
