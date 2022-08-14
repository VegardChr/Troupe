"""Gemstone"""

from enum import IntEnum

from pygame import Color


class Gemstone:
    """
    Gemstones found in mines.
    """

    class Kind(IntEnum):
        """
        Gemstone enumeration.
        """

        RUBY = 0
        EMERALD = 1
        SAPPHIRE = 2

    color = {
        Kind.RUBY: Color(255, 0, 0),
        Kind.EMERALD: Color(0, 255, 0),
        Kind.SAPPHIRE: Color(0, 0, 255),
    }

    value = {
        Kind.RUBY: 9,
        Kind.EMERALD: 6,
        Kind.SAPPHIRE: 7,
    }
