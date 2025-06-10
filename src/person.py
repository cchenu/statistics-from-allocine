"""Module containing the Person class."""

import re

import requests
from bs4 import BeautifulSoup


class Person:
    """
    Class representing a person, actor or director, with Allocine data.

    ...

    Parameters
    ----------
    person_id : int
        Identifier of the person on Allocine.

    Attributes
    ----------
    __id : int
        Identifier of the person on Allocine.
    __html : str
        HTML code of the person's page.
    __name : str
        Full name of the person.
    __image : str
        Link to the Allocine's image for the person.
    __directed_films : list[int]
        List of Allocine's id of films directed by the person.
    __played_films : list[int]
        List of Allocine's id of films with the person as actor.

    Public methods
    -------
    get_id() -> int
        Get the person's identifier on Allocine.
    get_html() -> str
        Get HTML code of the person's page.
    set_name()
        Set the full name of the person.
    get_name() -> str
        Get the full name of the person.
    set_image()
        Set the link to an image of the person.
    get_image() -> str
        Get the link to an image of the person.
    find_films(role: str) -> list[int]
        Find films where the person have the indicated role.
    set_directed_films()
        Set list of films directed by the person.
    get_directed_films() -> list[int]
        Get list of films directed by the person.
    set_played_films()
        Set list of films with the person as actor.
    get_played_films() -> list[int]
        Get list of films with the person as actor.
    """

    def __init__(self, person_id: int):
        """Construct an object of the Person class.

        Parameters
        ----------
        person_id : int
            Identifier of the person on Allocine.
        """
        self.__id = person_id
        self.__name: str
        self.__image: str
        self.__directed_films: list[int]
        self.__played_films: list[int]

        url = (
            f"https://www.allocine.fr/personne/fichepersonne-{self.__id}"
            "/filmographie/"
        )
        response = requests.get(url, timeout=30)
        self.__html = str(BeautifulSoup(response.content, "html.parser"))

        self.set_name()
        self.set_image()
        self.set_directed_films()
        self.set_played_films()

    def get_id(self) -> int:
        """
        Get the person's identifier on Allocine.

        Returns
        -------
        int
            Value of the person's identifier on Allocine.
        """
        return self.__id

    def get_html(self) -> str:
        """
        Get HTML code of the person's page.

        Returns
        -------
        str
            HTML code of the person's page.
        """
        return self.__html

    def set_name(self) -> None:
        """
        Set the full name of the person.

        Returns
        -------
        None.

        """
        pattern_name = r"<title>(.*?)(?: : Filmographie)* - AlloCiné</title>"
        self.__name = re.findall(pattern_name, self.__html)[0]

    def get_name(self) -> str:
        """
        Get the full name of the person.

        Returns
        -------
        str
            Full name of the person.

        """
        return self.__name

    def set_image(self) -> None:
        """
        Set the link to an image of the person.

        Returns
        -------
        None.

        """
        pattern_image = r"<meta content=\"https://(.*?)\""
        self.__image = "https://" + re.findall(pattern_image, self.__html)[0]

    def get_image(self) -> str:
        """
        Get the link to an image of the person.

        Returns
        -------
        str
            Link to an image of the person.

        """
        return self.__image

    def find_films(self, role: str) -> list[int]:
        """
        Find films where the person have the indicated role.

        Parameters
        ----------
        role : str
            Role of the person. For example (?:Réalisateur|Réalisatrice) to
            find results for men and women.

        Returns
        -------
        list[int]
            List of films where the person have the indicated role.

        """
        # Pattern to keep only films with the selected role
        pattern_role = (
            rf'<h2 class="titlebar-title titlebar-title-md">{role}</h2>'
            r"(.*?)"
            r'(?:<h2 class="titlebar-title titlebar-title-md">|$)'
        )
        # re.DOTALL allow a result on several lines
        html = re.findall(pattern_role, self.__html, re.DOTALL)

        if not html:  # If we have not a section with this role
            return []

        # We search film titles, because ID are not necessarly in this section
        pattern_title = r'title="(.*?)">'
        titles = re.findall(pattern_title, html[0])
        films: list[int] = []
        for title in titles:
            # Change regex caracters
            title = re.escape(title)
            # We search the id of the film
            pattern_film = (
                rf'/film/fichefilm_gen_cfilm=(.*?).html" title="{title}">'
            )
            result = re.findall(pattern_film, self.__html)
            if result:
                films.extend(
                    [int(film) for film in result if int(film) not in films]
                )
        return films

    def set_directed_films(self) -> None:
        """
        Set list of films directed by the person.

        Returns
        -------
        None.

        """
        self.__directed_films = self.find_films("(?:Réalisateur|Réalisatrice)")

    def get_directed_films(self) -> list[int]:
        """
        Get list of films directed by the person.

        Returns
        -------
        list[int]
            List of Allocine's id of films directed by the person.

        """
        return self.__directed_films

    def set_played_films(self) -> None:
        """
        Set list of films with the person as actor.

        Returns
        -------
        None.

        """
        self.__played_films = self.find_films("(?:Acteur|Actrice)")

    def get_played_films(self) -> list[int]:
        """
        Get list of films with the person as actor.

        Returns
        -------
        list[int]
            List of Allocine's id of films with the person as actor.

        """
        return self.__played_films


if __name__ == "__main__":
    eastwood = Person(1146)
    hancock = Person(523154)
