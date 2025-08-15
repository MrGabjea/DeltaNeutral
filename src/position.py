class Position:
    # Details of the position:
    #     - collateral is in USD, with decimals = 6, ie: 1 USD=10**6 units
    #     - position is in human readable units
    amount_collateral: int
    amount_position: float

    def __init__(self, amount_collateral: int, amount_position: float) -> None:
        self.amount_collateral = amount_collateral
        self.amount_position = amount_position

    def add_collateral(self, amount: int) -> int:
        raise NotImplementedError("The method hasn't been implemented for subclass")

    def remove_collateral(self, amount: int) -> int:
        raise NotImplementedError("The method hasn't been implemented for subclass")
