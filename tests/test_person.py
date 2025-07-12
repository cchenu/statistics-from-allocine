"""Unit tests for the Person class."""

import sys
from pathlib import Path

sys.path.append(str((Path(__file__).parent.parent / "src").resolve()))

from src.person import Person


def test_eastwood() -> None:
    """
    Test that Person(1146) returns correct data for Clint Eastwood.

    A test is done on Clint Eastwood because it can represent persons with many
    data and who are actors and directors.
    """
    eastwood = Person(1146)
    assert eastwood.get_id() == 1146
    assert eastwood.get_name() == "Clint Eastwood"
    assert (
        eastwood.get_image()
        == "https://fr.web.img2.acsta.net/pictures/15/10/15/16/51/136406.jpg"
    )
    assert len(eastwood.get_directed_films()) >= 41
    assert len(eastwood.get_played_films()) >= 82


def test_hancock() -> None:
    """
    Test that Person(523154) returns correct data for Drew Hancock.

    A test is done on Drew Hancock because it can reprend persons with many
    data but who are only actors or directors.
    """
    hancock = Person(523154)
    assert hancock.get_id() == 523154
    assert hancock.get_name() == "Drew Hancock"
    assert hancock.get_image() == (
        "https://fr.web.img3.acsta.net/commons/v9/common/empty/"
        "empty_portrait.png"
    )
    assert len(hancock.get_directed_films()) >= 2
    assert len(hancock.get_played_films()) == 0


def test_whitney() -> None:
    """
    Test that Person(151947) returns correct data for Ryan Whitney.

    A test is done on Ryan Whitney because it can reprend persons with few
    data, without a filmography page.
    """
    whitney = Person(151947)
    assert whitney.get_id() == 151947
    assert whitney.get_name() == "Ryan Whitney"
    assert len(whitney.get_played_films()) >= 4
