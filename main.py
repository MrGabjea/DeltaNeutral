from dotenv import load_dotenv
from typing import Any
import os
from config import config
from src.position import Position
from src.riskManager import Manager
from src.subclass_position.hyperLiquid import Hyperliquid
from src.subclass_position.fluid import Fluid
from src.subclass_position.morpho import Morpho


def main() -> None:

    # --- LOAD ENV ---
    load_dotenv()
    private_key: str = os.getenv("PRIVATE_KEY", "")
    rpc: str = os.getenv("RPC_URL", "")
    wallet_address: str = os.getenv("WALLET_ADDRESS", "")
    if "" in [private_key, rpc, wallet_address]:
        raise ValueError("Problem in load_dotenv")

    # --- CREATE POSITION ---
    def match_position(side: str) -> Position:
        if side not in config:
            raise KeyError(f"Key '{side}' does not exist in config")
        position_config: dict[str, Any] = config[side]
        match position_config["type"]:
            case "fluid":
                return Fluid(
                    amount_collateral=position_config["amount_collateral"],
                    amount_position=position_config["amount_position"],
                    id=position_config["additional"]["id"],
                )
            case "morpho":
                return Morpho(
                    amount_collateral=position_config["amount_collateral"],
                    amount_position=position_config["amount_position"],
                )
            case "hyperliquid":
                return Hyperliquid(
                    amount_collateral=position_config["amount_collateral"],
                    amount_position=position_config["amount_position"],
                    key=private_key,
                    wallet_address=wallet_address,
                    liquidation_price=position_config["additional"][
                        "liquidation_price"
                    ],
                )
        raise KeyError("Position in config not found")

    long_pos = match_position("long")
    short_pos = match_position("short")

    risk_manager = Manager(
        crypto=config["crypto"],
        long=long_pos,
        short=short_pos,
        crit_ratio_long=config["crit_ratio_long"],
        crit_ratio_short=config["crit_ratio_short"],
        target_ratio_long=config["traget_ratio_long"],
        target_ratio_short=config["target_ratio_short"],
        rpc=rpc,
        address=wallet_address,
    )
    risk_manager.manage()


if __name__ == "__main__":
    main()
