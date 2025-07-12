"""Unit tests for the Film class."""

import ast
import math
import sys
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

import pandas as pd
import pytest

from src import film
from src.corrections import corrections
from src.film import Film
from src.utils import CSV_DIR

CORRECTIONS_LIST = [
    (param, id_, value)
    for param, param_dict in corrections.items()
    for id_, value in param_dict.items()
]

CONVERTERS: Mapping[str, Callable[[str], Any]] = {
    "genres": ast.literal_eval,
    "countries": ast.literal_eval,
    "actors": ast.literal_eval,
    "directors": ast.literal_eval,
    "duration": int,
    "year": int,
}
DF_FILMS = pd.read_csv(CSV_DIR / "films.csv", converters=CONVERTERS)


def test_film_oss() -> None:
    """
    Test that Film(111835) returns correct data for OSS 117.

    A test is done on `OSS 117 : Rio ne répond plus` because it can respresent
    films with many data.
    """
    oss = Film(111835)
    assert oss.get_id() == 111835
    assert oss.get_title() == "OSS 117 : Rio ne répond plus"
    assert oss.get_duration() == 100
    assert oss.get_genres() == [13005, 13022]
    assert oss.get_year() == 2009
    assert oss.get_countries() == ["France"]
    assert not math.isnan(oss.get_press_rating())
    assert not math.isnan(oss.get_spectator_rating())
    assert len(oss.get_actors()) >= 46
    assert isinstance(oss.get_actors()[0], int)
    assert oss.get_directors() == [5079]
    assert oss.get_poster() == (
        "https://fr.web.img4.acsta.net/medias/nmedia/18/67/41/85/19057747.jpg"
    )


def test_film_panda() -> None:
    """
    Test that Film(144713) returns correct data for Kung Fu Panda.

    A test is done on `Kung Fu Panda : Les Secrets des Cinq Cyclones` because
    it can respresent films with few data.
    """
    panda = Film(144713)
    assert panda.get_id() == 144713
    assert panda.get_title() == "Kung Fu Panda : Les Secrets des Cinq Cyclones"
    assert panda.get_duration() == 25
    assert panda.get_genres() == [13026]
    assert panda.get_year() == 2008
    assert panda.get_countries() == ["U.S.A."]
    assert math.isnan(panda.get_press_rating())
    assert not math.isnan(panda.get_spectator_rating())
    assert len(panda.get_actors()) >= 3
    assert isinstance(panda.get_actors()[0], int)
    assert panda.get_directors() == [62924]
    assert panda.get_poster() == (
        "https://fr.web.img6.acsta.net/c_310_420/commons/v9/common/empty/"
        "empty_portrait.png"
    )


def assert_equal_or_nan(csv_value: float, new_value: float) -> None:
    """
    Compare two values which can be NaN.

    Parameters
    ----------
    csv_value : float
        Value in `csv/films.csv`.
    new_value : float
        Value finds with the Film class.
    """
    if math.isnan(new_value):
        assert math.isnan(csv_value)
    else:
        assert csv_value == new_value


@pytest.mark.parametrize("id_", DF_FILMS["id"].sample(n=10).tolist())
def test_film_random(id_: int) -> None:
    """
    Test that a random film returns data as in `csv/films.csv`.

    Parameters
    ----------
    id_ : int
        Identifier of the film on Allocine.
    """
    film_series = DF_FILMS[DF_FILMS["id"] == id_].iloc[0]
    film_object = Film(film_series["id"])

    assert film_object.get_id() == film_series["id"]
    assert film_object.get_title() == film_series["title"]
    assert film_object.get_duration() == film_series["duration"]
    assert sorted(film_object.get_genres()) == sorted(film_series["genres"])
    assert film_object.get_year() == film_series["year"]
    assert film_object.get_countries() == film_series["countries"]
    assert_equal_or_nan(
        film_object.get_press_rating(), film_series["press rating"]
    )
    assert_equal_or_nan(
        film_object.get_spectator_rating(), film_series["spectator rating"]
    )
    assert sorted(film_object.get_actors()) == sorted(film_series["actors"])
    assert sorted(film_object.get_directors()) == sorted(
        film_series["directors"]
    )
    assert film_object.get_poster() == film_series["poster"]


@pytest.mark.parametrize(("param", "id_", "value"), CORRECTIONS_LIST)
@pytest.mark.xfail(reason="Wrong data in Allocine")
def test_corrections(
    param: str,
    id_: int,
    value: int | list[int],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Test if values set in `corrections.py` are still needed.

    Parameters
    ----------
    param : str
        Parameter tested, could be `year`, `duration` or `directors`.
    id_ : int
        Identifier of the film on Allocine.
    value : int | list[int]
        Value set in `corrections.py`.
    monkeypatch : pytest.MonkeyPatch
        Patch to empty `corrections.corrections`.
    """
    monkeypatch.setattr(
        film, "corrections", {"year": {}, "duration": {}, "directors": {}}
    )
    film_test = Film(id_)
    if param == "year":
        assert film_test.get_year() == value
    elif param == "duration":
        assert film_test.get_duration() == value
    elif param == "directors":
        assert film_test.get_directors() == value
