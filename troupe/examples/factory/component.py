"""Component."""

from enum import IntEnum
from pygame import Color


class Component:
    """
    A component used to assemble products the factory.
    """

    class Kind(IntEnum):
        """Component enumeration."""

        SPARKPLUGS = 0
        VALVES = 1
        CRANKSHAFT = 2
        PISTONS = 3
        CARBURETOR = 4

    # Component colors.
    color = {
        Kind.SPARKPLUGS: Color(223, 15, 255),
        Kind.VALVES: Color(15, 223, 15),
        Kind.CRANKSHAFT: Color(127, 127, 223),
        Kind.PISTONS: Color(223, 223, 15),
        Kind.CARBURETOR: Color(15, 223, 223),
    }
