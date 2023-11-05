"""
This file has some custom structs
"""

from dataclasses import dataclass


@dataclass
class WindowGeometry:
    """
    The class `WindowGeometry` represents the geometry (height, width, top, and left position)
    of a window.
    """

    height: int
    width: int
    top: int
    left: int
