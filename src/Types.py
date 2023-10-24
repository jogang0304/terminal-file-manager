from dataclasses import dataclass


# The code is defining a data class called `WindowGeometry`. The `@dataclass` decorator is used to
# automatically generate special methods such as `__init__`, `__repr__`, and `__eq__` for the class
# based on the defined attributes.
@dataclass
class WindowGeometry:
    height: int
    width: int
    top: int
    left: int
