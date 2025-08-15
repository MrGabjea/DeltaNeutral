from ..position import Position


class Fluid(Position):

    id: int

    def __init__(self, id: int) -> None:
        self.id = id
        self.amount_collateral

    def add_collateral(self, amount: int) -> int:
        raise NotImplementedError("The method hasn't been implemented for subclass")

    def remove_collateral(self, amount: int) -> int:
        raise NotImplementedError("The method hasn't been implemented for subclass")
