from position import Position


class Manager:
    long: Position
    short: Position

    def __init__(self, long: Position, short: Position, rpc: str) -> None:
        self.long = long
        self.short = short

        self.rpc = rpc
