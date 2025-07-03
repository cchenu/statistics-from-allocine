"""Module containing corrections for films with an error on Allocine."""

from typing import Any

# Dictionary with all corrections
corrections: dict[str, dict[int, Any]] = {
    "year": {
        621: 1945,
        2025: 1945,
        6955: 1944,
        7189: 1937,
        37789: 1895,
        16126: 1946,
        27558: 1972,
        31526: 1965,
        49968: 1931,
        92174: 1929,
        93185: 1933,
        103167: 1936,
        130257: 1945,
        144713: 2008,
        174825: 1945,
        176238: 2009,
        193367: 1946,
    },
    "duration": {
        18450: 16,
        37789: 1,
        144713: 25,
        178627: 4,
        228223: 99,
    },
    "directors": {
        15886: [15886, 216401],
    },
}
