from dataclasses import dataclass
from typing import Callable


@dataclass
class Tile:
    name: str
    icon: str
    func: Callable
