"""Create an empty list of countries and genres with films in Allocine."""

import re
import multiprocessing
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import pandas as pd


def get_name(type_, id_):
    """
    Get the country or the genre with its Allocine's id.

    Parameters
    ----------
    type_ : string
        "pays" or "genre".
    id_ : integer
        ID of the country or the genre in allocine.

    Returns
    -------
    string
        Name of the country or the genre with this id.

    """
    response = requests.get(f"https://www.allocine.fr/films/{type_}-{id_}",
                            timeout=10)
    html_page = str(BeautifulSoup(response.content, "html.parser"))
    pattern = r'class="filter-entity-on-txt" data-name="(.*?)">'
    results = re.findall(pattern, html_page)
    if len(results) == 0:
        return None
    return results[0]


def get_country(id_country):
    """
    Get the country with its Allocine's id.

    Parameters
    ----------
    id_country : integer
        ID of the country in allocine.

    Returns
    -------
    country : string
        Name of the country with this id.

    """
    country = get_name("pays", id_country)
    return country


def get_genre(id_genre):
    """
    Get the genre with its Allocine's id.

    Parameters
    ----------
    id_genre : integer
        ID of the genre in allocine.

    Returns
    -------
    genre : string
        Name of the genre with this id.

    """
    genre = get_name("genre", id_genre)
    return genre


def run():
    """
    Create a csv file with all countries in Allocine.

    Returns
    -------
    None.

    """
    df_countries = pd.DataFrame()
    df_countries['id'] = range(0, 20000)
    df_genres = pd.DataFrame()
    df_genres['id'] = range(0, 20000)
    with multiprocessing.Pool() as pool:
        df_countries['country'] = tqdm(pool.imap(get_country,
                                                 df_countries['id']),
                                       total=len(df_countries))
        df_genres['genre'] = tqdm(pool.imap(get_genre,
                                            df_genres['id']),
                                  total=len(df_genres))
    df_countries = df_countries.dropna()
    df_countries.to_csv('csv/countries.csv', index=False)
    df_genres = df_genres.dropna()
    df_genres.to_csv('csv/genres.csv', index=False)


if __name__ == '__main__':
    run()
