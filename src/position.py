from dataclasses import dataclass


@dataclass
class Position:
    # Details of the position:
    #     - collateral is in USD, with decimals = 6, ie: 1 USD=10**6 units
    #     - position is in human readable units
    amount_collateral: int = 0
    amount_position: float = 0.0

    def __str__(self):
        return f"Position(collateral = {self.amount_collateral}, size_position = {self.amount_position})"

    def get_ratio(self, quote: float) -> float:
        # NB: this method must be overwritten in subclass when ratio is calculated differently
        if self.amount_position == 0:
            raise ValueError("position = 0 ==> Ratio undefined ")
        ratio = (self.amount_collateral / 10**6) / (self.amount_position * quote)
        return ratio

    # the following methods must be overwritten in dedicated subclass file
    def add_collateral(self, amount: int) -> int:
        raise NotImplementedError("The method hasn't been implemented for subclass")

    def remove_collateral(self, amount: int) -> int:
        raise NotImplementedError("The method hasn't been implemented for subclass")
