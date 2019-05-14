from enum import Enum


class Side(Enum):
    """
    An enumeration specifying side of an edge.

    For example, imagine the line segment P1 to P2:

    P1------->P2

    The "left"-hand side of the line segment would be anything above the line.
    The "right"-hand side of the line segment would be anything below the line.
    """
    LEFT = 'left'
    """The left-hand side"""
    RIGHT = 'right'
    """The right-hand side"""
