from enum import Enum


class Side(Enum):
    """
    An enumeration specifying side of an edge.

    For example, imagine the horizontal line segment P1 to P2:

    P1------->P2

    The "left"-hand side of the line segment would be anything above the line.
    The "right"-hand side of the line segment would be anything below the line.
    """
    LEFT = 'left'
    """The left-hand side"""
    RIGHT = 'right'
    """The right-hand side"""

    @property
    def flipped(self) -> 'Side':
        """
        This might be helpful in situations where the y-axis has been flipped,
        which is a common issue between UI Coordinate systems and "maths"
        coordinate systems.

        :return:
            The inverse value for the current Side
        """
        if self == Side.LEFT:
            return Side.RIGHT
        return Side.LEFT
