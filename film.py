"""Module containing the Film class."""

import re
import requests
from bs4 import BeautifulSoup


class Film:
    """
    Class representing a film with Allocine data.

    ...

    Attributes
    ----------
    id : integer
        Identifier of the film on Allocine.
    title : string
        Title of the film.
    duration : integer
        Duration of the film in minutes.
    genres : list of string
        Genres of the film.
    year : integer
        Release year of the film.
    countries : list of string
        List of countries of the film.
    total : dictionary
        All the film's information.

    Public methods
    -------
    set_id(id: integer)
        Set the film's identifier on Allocine.
    get_id() -> int
        Get the film's identifier on Allocine.
    set_title(html_code: str)
        Set the film's title.
    get_title() -> str
        Get the film's title.
    set_duration(html_code: str)
        Set the film's duration.
    get_duration() -> int
        Get the film's duration.
    set_genres(html_code: str)
        Set the film's genres.
    get_genres() -> list of str
        Get the film's genres.
    set_year(html_code: str)
        Set the film's release year.
    get_year() -> int
        Get the film's release year.
    set_countries(html_code: str)
        Set the list of countries of the film.
    get_countries() -> list of str
        Get the list of countries of the film.
    set_total()
        Set all the film's information.
    get_total() -> dict
        Get all the film's information.
    """

    def __init__(self, film_id):
        self.set_id(film_id)
        url = f"https://www.allocine.fr/film/fichefilm_gen_cfilm" \
              f"={self.__id}.html"
        response = requests.get(url, timeout=10)
        html_code = str(BeautifulSoup(response.content, "html.parser"))
        self.set_title(html_code)
        self.set_duration(html_code)
        self.set_genres(html_code)
        self.set_year(html_code)
        self.set_countries(html_code)
        self.set_total()

    def set_id(self, film_id):
        """
        Set the film's identifier on Allocine.

        Parameters
        ----------
        id : integer
            Value of the film's identifier on Allocine.

        Returns
        -------
        None.
        """
        self.__id = film_id

    def get_id(self):
        """
        Get the film's identifier on Allocine.

        Returns
        -------
        integer
            Value of the film's identifier on Allocine.
        """
        return self.__id

    def set_title(self, html_code):
        """
        Set the film's title.

        Parameters
        ----------
        html_code : string
            HTML code of the film's page.

        Returns
        -------
        None.
        """
        pattern_title = r'<div class="titlebar-title titlebar-title-xl">' \
                        r'(.*?)</div>'
        self.__title = re.findall(pattern_title, html_code)[0]

    def get_title(self):
        """
        Get the film's title.

        Returns
        -------
        string
            Title of the film.
        """
        return self.__title

    def set_duration(self, html_code):
        """
        Set the film's duration.

        Parameters
        ----------
        html_code : string
            HTML code of the film's page.

        Returns
        -------
        None.
        """
        pattern_duration = r'<span class="spacer">\|</span>\s*(.*?)\s*' \
                           r'<span class="spacer">\|</span>'
        duration = re.findall(pattern_duration, html_code)
        if duration:
            duration = duration[0]
            self.__duration = int(duration[0]) * 60 + int(duration[3:5])
        else:
            self.__duration = None

    def get_duration(self):
        """
        Get the film's duration.

        Returns
        -------
        integer
            Duration of the film.
        """
        return self.__duration

    def set_genres(self, html_code):
        """
        Set the film's genres.

        Parameters
        ----------
        html_code : string
            HTML code of the film's page.

        Returns
        -------
        None.
        """
        pattern_genres = r'"movie_genres":"(.*?)"'
        self.__genres = re.findall(pattern_genres, html_code)[0].split('|')

    def get_genres(self):
        """
        Get the film's genres.

        Returns
        -------
        list of string
            List of genres of the film.
        """
        return self.__genres

    def set_year(self, html_code):
        """
        Set the film's year.

        Parameters
        ----------
        html_code : string
            HTML code of the film's page.

        Returns
        -------
        None.
        """
        pattern_year = r'"releasedate":"(.*?)-'
        year = re.findall(pattern_year, html_code)
        if year:
            self.__year = int(year[0])
        else:
            self.__year = None
        if self.__id == 4327:  # Error on Allocine website
            self.__year = 1963

    def get_year(self):
        """
        Get the film's year.

        Returns
        -------
        integer
            Year of the film.
        """
        return self.__year

    def set_countries(self, html_code):
        """
        Set the list of countries of the film.

        Parameters
        ----------
        html_code : string
            HTML code of the film's page.

        Returns
        -------
        None.
        """
        pattern_countries = r'= nationality">\s*(.*?)</span>'
        self.__countries = re.findall(pattern_countries, html_code)

    def get_countries(self):
        """
        Get the list of countries of the film.

        Returns
        -------
        list of string
            List of countries of the film.
        """
        return self.__countries

    def set_total(self):
        """
        Set all the film's information.

        Returns
        -------
        dictionary
            All the film's information.
        """
        self.__total = {'id': self.__id,
                        'title': self.__title,
                        'duration': self.__duration,
                        'genres': self.__genres,
                        'year': self.__year,
                        'countries': self.__countries}

    def get_total(self):
        """
        Get all the film's information.

        Returns
        -------
        dictionary
            All the film's information.
        """
        return self.__total


if __name__ == "__main__":
    oss = Film(111835)
