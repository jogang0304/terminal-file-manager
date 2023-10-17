from dataclasses import dataclass


@dataclass
class WindowGeometry():
    height: int
    width: int
    top: int
    left: int