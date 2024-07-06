"""Create csv files for films data of a Allocine films collection."""

import multiprocessing
from tqdm import tqdm
import pandas as pd
from film import Film
from watched import watched_list


def update_awards(token):
    """
    Update csv about Cesars, Oscars and Palmes d'Or films.

    Parameters
    ----------
    token : string
        Token to be connected to Allocine.

    Returns
    -------
    None.

    """
    oscars_id = "VXNlckNvbGxlY3Rpb246NDQ5NzM="
    cesars_id = "VXNlckNvbGxlY3Rpb246NDQ5NzQ="
    palmes_id = "VXNlckNvbGxlY3Rpb246NDQ5NzY="
    films(oscars_id, token, name_file="oscars", other_csv=False)
    films(cesars_id, token, name_file="cesars", other_csv=False)
    films(palmes_id, token, name_file="palmes", other_csv=False)


def films(collection_id, token, name_file="films", other_csv=True):
    """
    Create csv files for films, countries and genres.

    Parameters
    ----------
    collection_id : string
        ID of the Allocine collection.
    token : string
        Token to be connected to Allocine.
    name_file : string
        Name of the file with film information. The default is "films".
    other_csv : boolean, optional
        True if you want countries.csv and genres.csv. The default is True.

    Returns
    -------
    None.

    """
    list_id = watched_list(collection_id, token)
    df_films = pd.DataFrame(list_id, columns=["id"])

    with multiprocessing.Pool() as pool:
        df_films["Film"] = tqdm(
            pool.imap(Film, df_films["id"]), total=len(df_films)
        )

    df_films["title"] = df_films["Film"].apply(lambda f: f.get_title())
    df_films["duration"] = df_films["Film"].apply(lambda f: f.get_duration())
    df_films["genres"] = df_films["Film"].apply(lambda f: f.get_genres())
    df_films["year"] = df_films["Film"].apply(lambda f: f.get_year())
    df_films["countries"] = df_films["Film"].apply(lambda f: f.get_countries())
    df_films["press rating"] = df_films["Film"].apply(
        lambda f: f.get_press_rating()
    )
    df_films["spectator rating"] = df_films["Film"].apply(
        lambda f: f.get_spectator_rating()
    )
    df_films = df_films.drop(["Film"], axis=1)  # Remove Film column
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
                    lambda countries: country in countries
                )
            ].shape[0]
        )
        df_countries.to_csv("csv/countries.csv", index=False)

    print("\nCompleted!")


if __name__ == "__main__":
    ID = ""
    TOKEN = ""
    # update_awards(TOKEN)
    films(ID, TOKEN)
