from config import config
from src.subclass_position.hyperLiquid import Hyperliquid

pos = Hyperliquid(key="0xkey", wallet_address="0xaddress")

print(config["long"])
# pos.remove_collateral(5 * 10**6)
