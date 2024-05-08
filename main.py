"""Create csv files for films data of a Allocine films collection."""

import csv
from tqdm import tqdm
from film import Film
from watched import watched_list


def films(collection_id, token):
    """
    Create csv files for films, countries and genres.

    Parameters
    ----------
    collection_id : string
        ID of the Allocine collection.
    token : TYPE
        Token to be connected to Allocine.

    Returns
    -------
    None.

    """
    list_id = watched_list(collection_id, token)
    headers = ['id', 'title', 'duration', 'genres', 'year', 'countries']
    country_dict = {}
    genre_dict = {}
    progress_bar = tqdm(total=len(list_id), desc="Progression")
    with open('films.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Write headers
        writer.writeheader()

        # Write film data
        for id_ in list_id:
            film = Film(id_)
            for country in film.get_countries():  # Dictionary of countries
                country_dict[country] = country_dict.get(country, 0) + 1
            for genre in film.get_genres():  # Dictionary of genres
                genre_dict[genre] = genre_dict.get(genre, 0) + 1
            writer.writerow(film.get_total())
            progress_bar.update(1)
    progress_bar.close()

    # Creation of the country csv file
    headers = ['country', 'number']
    with open('countries.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Write headers
        writer.writeheader()

        # Write film data
        for country, occurrences in country_dict.items():
            writer.writerow({'country': country, 'number': occurrences})

    # Creation of the genre csv file
    headers = ['genre', 'number']
    with open('genres.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Write headers
        writer.writeheader()

        # Write film data
        for genre, occurrences in genre_dict.items():
            writer.writerow({'genre': genre, 'number': occurrences})

    print('\nCompleted!')


if __name__ == "__main__":
    ID = ""
    TOKEN = ""
    films(ID, TOKEN)
