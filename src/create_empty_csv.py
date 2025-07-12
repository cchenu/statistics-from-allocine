"""Create an empty list of countries and genres with films in Allocine."""

import multiprocessing
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from tqdm import tqdm

from src.utils import CSV_DIR


def get_name(type_: str, id_: int) -> str | None:
    """
    Get the country or the genre with its Allocine's id.

    Parameters
    ----------
    type_ : str
        Type of entity to retrieve, either "pays" (country) or "genre".
    id_ : int
        Allocine ID of the country or genre.

    Returns
    -------
    str
        Name of the country or the genre with the given ID.
        None if no result is found.
    """
    response = requests.get(
        f"https://www.allocine.fr/films/{type_}-{id_}", timeout=10
    )
    html_page = str(BeautifulSoup(response.content, "html.parser"))
    pattern = r'class="filter-entity-on-txt" data-name="(.*?)">'
    results: list[str] = re.findall(pattern, html_page)
    if len(results) == 0:
        return None
    return results[0]


def get_country(id_country: int) -> str | None:
    """
    Get the country with its Allocine's ID.

    Parameters
    ----------
    id_country : int
        Allocine ID of the country.

    Returns
    -------
    country : str
        Name of the country corresponding to the given ID.
        None if no result is found.
    """
    return get_name("pays", id_country)


def get_genre(id_genre: int) -> str | None:
    """
    Get the genre with its Allocine's ID.

    Parameters
    ----------
    id_genre : int
        Allocine ID of the genre.

    Returns
    -------
    genre : str
        Name of the genre corresponding to the given ID.
        None if no result is found.
    """
    return get_name("genre", id_genre)


def run() -> None:
    """
    Generate CSV files for countries and genres available on Allocine.

    This function creates two CSV files:
    - countries.csv with country names in french and english and their
    respective IDs.
    - genres.csv with french genre names and their respective IDs.
    """
    df_countries = pd.DataFrame()
    df_countries["id"] = range(5000, 8000)
    df_genres = pd.DataFrame()
    df_genres["id"] = range(13000, 14000)
    with multiprocessing.Pool() as pool:
        df_countries["country"] = tqdm(
            pool.imap(get_country, df_countries["id"]), total=len(df_countries)
        )
        df_genres["genre"] = tqdm(
            pool.imap(get_genre, df_genres["id"]), total=len(df_genres)
        )
    df_countries = df_countries.dropna()
    # Add english names
    translator = GoogleTranslator(source="fr", target="en")
    df_countries["country_en"] = df_countries["country"].apply(
        lambda country: (
            translator.translate(country) if country != "Suède" else "Sweden"
        )
    )
    df_countries.to_csv(CSV_DIR / "countries.csv", index=False)
    df_genres = df_genres.dropna()
    df_genres.to_csv(CSV_DIR / "genres.csv", index=False)


if __name__ == "__main__":
    run()
