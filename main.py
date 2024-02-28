import re
import csv
from film import Film


def films():
    """
    Creates csv files for films, countries and genres.

    Returns
    -------
    None.

    """
    f = open('watched.txt', 'r')  # Opening the document
    watched = f.read()
    '''
    Patterns : (.*?) is what we search, ({0,10}) for 0 to 10 characters,
    \\s is for a space, \\s* is for
    several spaces
    To search with characters like {, (, [, we use \\ before it
    '''
    pattern = r'cfilm=(.{0,10}).html"\stitle'
    '''re.findall(pattern, text) search the pattern in the text and give a
    list'''
    list_id = re.findall(pattern, watched)
    f.close()
    list_id = [int(id) for id in list_id]
    headers = ['id', 'title', 'duration', 'genres', 'year', 'countries']
    country_dict = {}
    genre_dict = {}
    with open('films.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Write headers
        writer.writeheader()

        # Write film data
        for id in list_id:
            film = Film(id)
            for country in film.get_countries():  # Dictionary of countries
                country_dict[country] = country_dict.get(country, 0) + 1
            for genre in film.get_genres():  # Dictionary of genres
                genre_dict[genre] = genre_dict.get(genre, 0) + 1
            writer.writerow(film.get_total())

    '''Creation of the country csv file'''
    headers = ['country', 'number']
    with open('countries.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Write headers
        writer.writeheader()

        # Write film data
        for country, occurrences in country_dict.items():
            writer.writerow({'country': country, 'number': occurrences})

    '''Creation of the genre csv file'''
    headers = ['genre', 'number']
    with open('genres.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Write headers
        writer.writeheader()

        # Write film data
        for genre, occurrences in genre_dict.items():
            writer.writerow({'genre': genre, 'number': occurrences})

    print('completed')


if __name__ == "__main__":
    films()
