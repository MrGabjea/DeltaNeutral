from typing import Any

config: dict[str, Any] = {
    "crypto": "BTC",
    "crit_ratio_long": 0,
    "crit_ratio_short": 0,
    "long": {
        "type": "subclass_type",
        "amount_collateral": 0,
        "amount_position": 0.0,
        "additional": {},
    },
    "short": {
        "type": "subclass_type",
        "amount_collateral": 0,
        "amount_position": 0.0,
        "additional": {},
    },
}

# USAGE depending on the subclass type
#
# "morpho" --> "additionnal" : {},
#
# "fluid" --> "additionnal": {"id": id_of_fluid_vault},   # type: int, found on the GUI or fluid contract
#
# "hyperliquid" --> "additionnal" : {"liquidation_price": price_when_pos_liquidated}, # type: float, found on GUI
