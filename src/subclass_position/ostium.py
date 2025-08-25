from dataclasses import dataclass

from ..position import Position


@dataclass
class Ostium(Position):

    def add_collateral(self, amount: int) -> int:
        raise NotImplementedError("The method hasn't been implemented for subclass")

    def remove_collateral(self, amount: int) -> int:
        raise NotImplementedError("The method hasn't been implemented for subclass")
