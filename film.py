"""Module containing the Film class."""

import re
import requests
from bs4 import BeautifulSoup
from corrections import corrections


class Film:
    """
    Class representing a film with Allocine data.

    ...

    Attributes
    ----------
    __id : integer
        Identifier of the film on Allocine.
    __title : string
        Title of the film.
    __duration : integer
        Duration of the film in minutes.
    __genres : list of integers
        Genres' id of the film.
    __year : integer
        Release year of the film.
    __countries : list of string
        List of countries of the film.
    __press_rating : float
        Press rating of the film.
    __spectator_rating : float
        Spectator rating of the film.

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
        Set the film's genres id.
    get_genres() -> list of int
        Get the film's genres id.
    set_year(html_code: str)
        Set the film's release year.
    get_year() -> int
        Get the film's release year.
    set_countries(html_code: str)
        Set the list of countries of the film.
    get_countries() -> list of str
        Get the list of countries of the film.
    set_press_rating(html_code: str)
        Set the press rating of the film.
    get_press_rating() -> float
        Get the press rating of the film.
    set_spectator_rating(html_code: str)
        Set the spectator rating of the film.
    get_spectator_rating() -> float
        Get the spectator rating of the film.
    """

    # pylint: disable=R0902

    def __init__(self, film_id):
        self.__id = film_id
        self.__title = None
        self.__duration = None
        self.__genres = None
        self.__year = None
        self.__countries = None
        self.__press_rating = None
        self.__spectator_rating = None

        url = (
            f"https://www.allocine.fr/film/fichefilm_gen_cfilm={self.__id}.htm"
            f"l"
        )
        response = requests.get(url, timeout=10)
        html_code = str(BeautifulSoup(response.content, "html.parser"))
        self.set_title(html_code)
        self.set_duration(html_code)
        self.set_genres(html_code)
        self.set_year(html_code)
        self.set_countries(html_code)
        self.set_press_rating(html_code)
        self.set_spectator_rating(html_code)

    def set_id(self, film_id):
        """
        Set the film's identifier on Allocine.

        Parameters
        ----------
        film_id : integer
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
        pattern_title = (
            r'<div class="titlebar-title titlebar-title-xl">(.*?)</div>'
        )
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
        pattern_duration = (
            r'<span class="spacer">\|</span>\s*(.*?)\s*<span class="spacer">\|'
            r"</span>"
        )
        duration = re.findall(pattern_duration, html_code)
        if duration:
            duration = duration[0]
            self.__duration = int(duration[0]) * 60 + int(duration[3:5])

        # If data in Allocine is empty or false
        if self.__id in corrections["year"]:
            self.__year = corrections["year"][self.__id]

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
        Set the film's genres id.

        Parameters
        ----------
        html_code : string
            HTML code of the film's page.

        Returns
        -------
        None.
        """
        pattern_genres = r'"genre":\["(.*?)"\]'
        genres = re.findall(pattern_genres, html_code)[0].split('","')
        self.__genres = [int(genre) for genre in genres]

    def get_genres(self):
        """
        Get the film's genres id.

        Returns
        -------
        list of int
            List of genres' id of the film.
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

        # If data in Allocine is empty or false
        if self.__id in corrections["year"]:
            self.__year = corrections["year"][self.__id]

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

    def set_press_rating(self, html_code):
        """
        Set the press rating of the film.

        Parameters
        ----------
        html_code : string
            HTML code of the film's page.

        Returns
        -------
        None.
        """
        pattern_press_rating = (
            r"Presse </span>.*?<span class=\"stareval-note\">(.*?)</span>"
        )
        rating = re.findall(pattern_press_rating, html_code, re.DOTALL)
        if len(rating) == 1:  # If there is a rating
            self.__press_rating = float(rating[0].replace(",", "."))
        else:
            self.__press_rating = float("nan")

    def get_press_rating(self):
        """
        Get the press rating of the film.

        Returns
        -------
        float
            Press rating of the film.
        """
        return self.__press_rating

    def set_spectator_rating(self, html_code):
        """
        Set the spectator rating of the film.

        Parameters
        ----------
        html_code : string
            HTML code of the film's page.

        Returns
        -------
        None.
        """
        pattern_spectator_rating = (
            r"Spectateurs </span>.*?<span class=\"stareval-note\">(.*?)</span>"
        )
        rating = re.findall(pattern_spectator_rating, html_code, re.DOTALL)
        if len(rating) == 1:  # If there is a rating
            self.__spectator_rating = float(rating[0].replace(",", "."))
        else:
            self.__spectator_rating = float("nan")

    def get_spectator_rating(self):
        """
        Get the spectator rating of the film.

        Returns
        -------
        float
            Spectator rating of the film.
        """
        return self.__spectator_rating


if __name__ == "__main__":
    oss = Film(111835)
