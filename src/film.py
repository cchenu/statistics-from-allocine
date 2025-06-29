"""Module containing the Film class."""

import base64
import logging
import re

import requests
from bs4 import BeautifulSoup

from corrections import corrections

logging.basicConfig(level=logging.INFO)


class Film:
    """
    Class representing a film with Allocine data.

    ...

    Parameters
    ----------
    film_id : int
        Identifier of the film on Allocine.

    Attributes
    ----------
    __id : int
        Identifier of the film on Allocine.
    __html : str
        HTML code of the film's page.
    __title : str
        Title of the film.
    __duration : int | None
        Duration of the film in minutes.
    __genres : list[int]
        genre IDs of the film.
    __year : int | None
        Release year of the film.
    __countries : list[str]
        List of countries of the film.
    __press_rating : float
        Press rating of the film.
    __spectator_rating : float
        Audience rating of the film.
    __actors : list[int]
        List of actor IDs of the film.
    __directors : list[int]
        List of directors' id of the film.
    __poster : str
        Link to the Allocine's poster of the film.

    Public methods
    -------
    get_id() -> int
        Get the film's identifier on Allocine.
    get_html() -> str
        Get HTML code of the film's page.
    set_title()
        Set the film's title.
    get_title() -> str
        Get the film's title.
    set_duration()
        Set the film's duration.
    get_duration() -> int | None
        Get the film's duration.
    set_genres()
        Set the film's genres id.
    get_genres() -> list[int]
        Get the film's genres id.
    set_year()
        Set the film's release year.
    get_year() -> int | None
        Get the film's release year.
    set_countries()
        Set the list of countries of the film.
    get_countries() -> list[str]
        Get the list of countries of the film.
    set_press_rating()
        Set the press rating of the film.
    get_press_rating() -> float
        Get the press rating of the film.
    set_spectator_rating()
        Set the audience rating of the film.
    get_spectator_rating() -> float
        Get the audience rating of the film.
    set_actors()
        Set the film's actors id.
    get_actors() -> list[int]
        Get the film's actors id.
    set_directors()
        Set the film's directors id.
    get_directors() -> list[int]
        Get the film's directors id.
    set_poster()
        Set the film's poster.
    get_poster() -> str
        Get the film's poster.

    """

    logger = logging.getLogger(__name__)

    def __init__(self, film_id: int) -> None:
        """
        Construct an object of the Film class.

        Parameters
        ----------
        film_id : int
            Identifier of the film on Allocine.

        """
        self.__id = film_id
        self.__html: str
        self.__title: str
        self.__duration: int | None
        self.__genres: list[int]
        self.__year: int | None
        self.__countries: list[str]
        self.__press_rating: float
        self.__spectator_rating: float
        self.__actors: list[int]
        self.__directors: list[int]
        self.__poster: str

        url = f"https://www.allocine.fr/film/fichefilm-{self.__id}/casting/"
        response = requests.get(url, timeout=30)
        self.__html = str(BeautifulSoup(response.content, "html.parser"))
        self.set_title()
        self.set_duration()
        self.set_genres()
        self.set_year()
        self.set_countries()
        self.set_press_rating()
        self.set_spectator_rating()
        self.set_actors()
        self.set_directors()
        self.set_poster()

    def get_id(self) -> int:
        """
        Get the film's identifier on Allocine.

        Returns
        -------
        int
            Value of the film's identifier on Allocine.

        """
        return self.__id

    def get_html(self) -> str:
        """
        Get HTML code of the film's page.

        Returns
        -------
        str
            HTML code of the film's page.

        """
        return self.__html

    def set_title(self) -> None:
        """
        Set the film's title.

        Returns
        -------
        None.

        """
        pattern_title = (
            r'<meta content="'
            r"(?:Tout le casting du film )?"
            r"(?:Casting de )?(.*?)"
            r'" property="og:title"/>'
        )
        self.__title = re.findall(pattern_title, self.__html)[0]

    def get_title(self) -> str:
        """
        Get the film's title.

        Returns
        -------
        str
            Title of the film.

        """
        return self.__title

    def set_duration(self) -> None:
        """
        Set the film's duration.

        Returns
        -------
        None.

        """
        # Search hours and minutes
        pattern_duration = r'"duration": "PT(.*?)H(.*?)M00S"'
        duration = re.findall(pattern_duration, self.__html)

        # If data in Allocine is empty or false
        if self.__id in corrections["duration"]:
            self.__duration = corrections["duration"][self.__id]
        elif duration:
            duration = duration[0]
            self.__duration = int(duration[0]) * 60 + int(duration[1])
        else:
            self.__duration = None
            self.logger.info(
                "Duration not found for film %s (ID: %d). You can set it "
                "manually in corrections.py.",
                self.__title,
                self.__id,
            )

    def get_duration(self) -> int | None:
        """
        Get the film's duration.

        Returns
        -------
        int | None
            Duration of the film. None if the duration is not on Allocine.

        """
        return self.__duration

    def set_genres(self) -> None:
        """
        Set the film's genres id.

        Returns
        -------
        None.

        """
        pattern_genres = r'"genre":\["(.*?)"\]'
        genres = re.findall(pattern_genres, self.__html)[0].split('","')
        self.__genres = [int(genre) for genre in genres]

    def get_genres(self) -> list[int]:
        """
        Get the film's genres id.

        Returns
        -------
        list[int]
            List of genre IDs of the film.

        """
        return self.__genres

    def set_year(self) -> None:
        """
        Set the film's release year.

        Returns
        -------
        None.

        """
        pattern_year = r'"releasedate":"(.*?)-'
        year = re.findall(pattern_year, self.__html)

        # If data in Allocine is empty or false
        if self.__id in corrections["year"]:
            self.__year = corrections["year"][self.__id]
        elif year:
            self.__year = int(year[0])
        else:
            self.__year = None
            self.logger.info(
                "Year not found for film %s (ID: %d). You can set it manually "
                "in corrections.py.",
                self.__title,
                self.__id,
            )

    def get_year(self) -> int | None:
        """
        Get the film's release year.

        Returns
        -------
        int | None
            Release year of the film. None if the year is not on Allocine.

        """
        return self.__year

    def set_countries(self) -> None:
        """
        Set the list of countries of the film.

        Returns
        -------
        None.

        """
        pattern_countries = r'"localizedName":"(.*?)"'
        self.__countries = [
            c.encode().decode("unicode_escape")
            for c in re.findall(pattern_countries, self.__html)
        ]

    def get_countries(self) -> list[str]:
        """
        Get the list of countries of the film.

        Returns
        -------
        list[str]
            List of countries of the film.

        """
        return self.__countries

    def set_press_rating(self) -> None:
        """
        Set the press rating of the film.

        Returns
        -------
        None.

        """
        pattern_press_rating = r'"press_rating":"(\d+\.*\d*)"'
        rating = re.findall(pattern_press_rating, self.__html)
        if len(rating) == 1:  # If there is a rating
            self.__press_rating = float(rating[0].replace(",", "."))
        else:
            self.__press_rating = float("nan")

    def get_press_rating(self) -> float:
        """
        Get the press rating of the film.

        Returns
        -------
        float
            Press rating of the film.

        """
        return self.__press_rating

    def set_spectator_rating(self) -> None:
        """
        Set the spectator rating of the film.

        Returns
        -------
        None.

        """
        pattern_spectator_rating = r'"user_rating":"(\d+\.*\d*)"'
        rating = re.findall(pattern_spectator_rating, self.__html)
        if len(rating) == 1:  # If there is a rating
            self.__spectator_rating = float(rating[0].replace(",", "."))
        else:
            self.__spectator_rating = float("nan")

    def get_spectator_rating(self) -> float:
        """
        Get the spectator rating of the film.

        Returns
        -------
        float
            Spectator rating of the film.

        """
        return self.__spectator_rating

    def set_actors(self) -> None:
        """
        Set the film's actors id.

        Returns
        -------
        None.

        """
        # Search page section with Actors
        pattern_actors = (
            r'<h2 class="titlebar-title titlebar-title-md">Act'
            r"(.*?)"
            r'<h2 class="titlebar-title titlebar-title-md">'
        )
        find_actors = re.findall(pattern_actors, self.__html, re.DOTALL)
        text_actors: str = find_actors[0] if find_actors else ""

        # Search id of actors
        pattern_id_actor = r"/personne/fichepersonne_gen_cpersonne=(.*?).html"
        actors = re.findall(pattern_id_actor, text_actors)

        # Some actors can have the id encoded in base64
        pattern_encoded = r"ACrL3BACrl(.*?)\s"
        actors_encoded = re.findall(pattern_encoded, text_actors)

        for code in actors_encoded:
            # We decode the page
            decoded_str = base64.b64decode(code).decode(
                "utf-8", errors="ignore"
            )
            # We find the id in the decoded string
            actor_id = re.findall(r"(\d+)", decoded_str)[0]

            if actor_id not in actors:
                actors.append(actor_id)

        self.__actors = [int(actor) for actor in actors if actor != ""]

        actors_by_page = 40
        if len(actors) >= actors_by_page:  # If we have several actors pages
            # We start from nothing with new requests with json result
            page = 1
            self.__actors = []
            # While there is a new page
            while len(self.__actors) == (page - 1) * 120:
                # URL of the requests
                url = (
                    f"https://www.allocine.fr/_/casting/movie-{self.__id}"
                    f"/type-CASTING/item-per-page-120/position-ACTOR/p-{page}/"
                )
                response = requests.get(url, timeout=30).json()["persons"]
                # Add ID of actors in this page
                self.__actors += [
                    actor["actor"]["internalId"] for actor in response
                ]
                page += 1

    def get_actors(self) -> list[int]:
        """
        Get the film's actors id.

        Returns
        -------
        list[int]
            List of actor IDs of the film.

        """
        return self.__actors

    def set_directors(self) -> None:
        """
        Set the film's directors id.

        Returns
        -------
        None.

        """
        # Search the page section with Directors
        pattern_directors = (
            r'<h2 class="titlebar-title titlebar-title-md">Réalisat'
            r"(.*?)"
            r'<h2 class="titlebar-title titlebar-title-md">'
        )
        find_directors = re.findall(pattern_directors, self.__html, re.DOTALL)
        text_directors = find_directors[0] if find_directors else ""

        # Search id of directors
        pattern_id_director = (
            r"/personne/fichepersonne_gen_cpersonne=(.*?).html"
        )
        directors = re.findall(pattern_id_director, text_directors)

        self.__directors = [
            int(director) for director in directors if director != ""
        ]

        # If data in Allocine is empty or false
        if self.__id in corrections["directors"]:
            self.__directors = corrections["directors"][self.__id]

    def get_directors(self) -> list[int]:
        """
        Get the film's directors id.

        Returns
        -------
        list[int]
            Directors' id of the film.

        """
        return self.__directors

    def set_poster(self) -> None:
        """
        Set the film's poster.

        Returns
        -------
        None.

        """
        pattern_poster = (
            r'"image": {\s*"@type": "ImageObject",\s*"url": "(.*?)"'
        )
        poster = re.findall(pattern_poster, self.__html)
        if poster:
            self.__poster = poster[0]
        else:
            self.__poster = (
                "https://fr.web.img6.acsta.net/c_310_420/commons/v9/common"
                "/empty/empty_portrait.png"
            )

    def get_poster(self) -> str:
        """
        Get the film's poster.

        Returns
        -------
        str
            Link to the Allocine's poster of the film.

        """
        return self.__poster


if __name__ == "__main__":
    oss = Film(111835)
