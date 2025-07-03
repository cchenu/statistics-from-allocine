"""Create CSV files containing data for a collection of films from Allociné."""

import ast
import multiprocessing
import os
from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

from film import Film
from watched import watched_list

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping


def update_awards() -> None:
    """Update csv about Cesars, Oscars and Palmes d'Or films."""
    oscars_id = "VXNlckNvbGxlY3Rpb246NDQ5NzM="
    cesars_id = "VXNlckNvbGxlY3Rpb246NDQ5NzQ="
    palmes_id = "VXNlckNvbGxlY3Rpb246NDQ5NzY="
    create_csv(oscars_id, name_file="oscars", other_csv=False)
    create_csv(cesars_id, name_file="cesars", other_csv=False)
    create_csv(palmes_id, name_file="palmes", other_csv=False)


def create_csv(
    collection_id: str | None = None,
    name_file: str = "films",
    other_csv: bool = True,
) -> str:
    """
    Create csv files for films, countries and genres.

    Parameters
    ----------
    collection_id : str, optional
        ID of the Allocine collection.
        The default is None, and become ID value of .env.
    name_file : str, optional
        Name of the file with film information. The default is "films".
    other_csv : bool, optional
        True if you want countries.csv and genres.csv. The default is True.

    Returns
    -------
    str
        String which says if some updates had been done or not.
    """
    load_dotenv(override=True)
    collection_id = collection_id or os.getenv("ID")
    token = os.getenv("TOKEN")
    if collection_id is None or token is None:
        msg = "Verify your ID and your token in your .env file!"
        raise ValueError(msg)
    try:
        list_id = watched_list(collection_id, token)
    except IndexError as exc:
        msg = "Verify your ID in your .env file!"
        raise ValueError(msg) from exc
    except KeyError as exc:
        msg = "Verify your TOKEN in your .env file!"
        raise ValueError(msg) from exc
    df_films = pd.DataFrame(list_id, columns=["id"])

    csv_exist = Path(f"csv/{name_file}.csv").exists()
    if csv_exist:
        converters: Mapping[str, Callable[[str], Any]] = {
            "genres": ast.literal_eval,
            "countries": ast.literal_eval,
            "actors": ast.literal_eval,
            "directors": ast.literal_eval,
            "duration": int,
            "year": int,
        }

        df_file = pd.read_csv(f"csv/{name_file}.csv", converters=converters)
        df_films = df_films[~df_films["id"].isin(df_file["id"])]

    if len(df_films) == 0:
        return "No file updates."

    with multiprocessing.Pool() as pool:
        df_films["Film"] = tqdm(
            pool.imap(Film, df_films["id"]), total=len(df_films)
        )

    df_films["title"] = df_films["Film"].apply(Film.get_title)
    df_films["duration"] = df_films["Film"].apply(Film.get_duration)
    df_films["genres"] = df_films["Film"].apply(Film.get_genres)
    df_films["year"] = df_films["Film"].apply(Film.get_year)
    df_films["countries"] = df_films["Film"].apply(Film.get_countries)
    df_films["press rating"] = df_films["Film"].apply(Film.get_press_rating)
    df_films["spectator rating"] = df_films["Film"].apply(
        Film.get_spectator_rating
    )
    df_films["actors"] = df_films["Film"].apply(Film.get_actors)
    df_films["directors"] = df_films["Film"].apply(Film.get_directors)
    df_films["poster"] = df_films["Film"].apply(Film.get_poster)

    df_films = df_films.drop(["Film"], axis=1)  # Remove Film column
    if csv_exist:
        df_films = pd.concat([df_films, df_file], ignore_index=True)
    df_films.to_csv(f"csv/{name_file}.csv", index=False)

    if other_csv:
        # Count the number of films for each genre
        df_genres = pd.read_csv("csv/genres.csv")
        df_genres["number"] = df_genres["id"].apply(
            lambda genre: df_films[
                df_films["genres"].apply(lambda genres: genre in genres)
            ].shape[0]
        )
        df_genres.to_csv("csv/genres.csv", index=False)

        # Count the number of films for each country
        df_countries = pd.read_csv("csv/countries.csv")
        df_countries["number"] = df_countries["country"].apply(
            lambda country: df_films[
                df_films["countries"].apply(
                    lambda countries: country in countries,
                )
            ].shape[0]
        )
        df_countries.to_csv("csv/countries.csv", index=False)

        # CSV actors and directors
        for persons in ("actors", "directors"):
            all_persons = df_films[persons].sum()
            df_persons = pd.DataFrame(
                list(Counter(all_persons).items()), columns=["id", "number"]
            )
            df_persons.to_csv(f"csv/{persons}.csv", index=False)

    return f"The file {name_file} has been updated!"


if __name__ == "__main__":
    update_awards()
    create_csv()
