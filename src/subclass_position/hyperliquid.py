from ..position import Position


class Hyperliquid(Position):
    def __init__(self) -> None:
        # to do
        self.amount_collateral = 0
        self.amount_position = 0

    def add_collateral(self, amount: int) -> int:
        raise NotImplementedError("The method hasn't been implemented for subclass")

    def remove_collateral(self, amount: int) -> int:
        raise NotImplementedError("The method hasn't been implemented for subclass")
