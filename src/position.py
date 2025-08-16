from dataclasses import dataclass


@dataclass
class Position:
    # Details of the position:
    #     - collateral is in USD, with decimals = 6, ie: 1 USD=10**6 units
    #     - position is in human readable units
    amount_collateral: int = 0
    amount_position: float = 0.0

    def add_collateral(self, amount: int) -> int:
        raise NotImplementedError("The method hasn't been implemented for subclass")

    def remove_collateral(self, amount: int) -> int:
        raise NotImplementedError("The method hasn't been implemented for subclass")
