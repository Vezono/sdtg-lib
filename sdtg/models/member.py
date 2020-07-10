from dataclasses import dataclass


@dataclass
class Member:
    id: int
    icon: str
    inventory: list
    pos: str
