from dataclasses import dataclass, field
import requests
import time
from web3 import Web3

from .position import Position


def get_price(crypto: str) -> float:
    symbol = crypto + "USDT"
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print("Erreur in fetching price:", e)
        return 0.0


@dataclass
class Manager:
    crypto: str = "BTC"

    long: Position = field(default_factory=Position)
    short: Position = field(default_factory=Position)

    crit_ratio_long: float = 0.80
    crit_ratio_short: float = 0.80

    target_ratio_long: float = 0.75
    target_ratio_short: float = 0.75

    # --- WEB3 INTERACTION ---
    address: str = "0x"
    rpc: str = "https://arb1.arbitrum.io/rpc"

    # minimal ABI for ERC-20
    erc20_abi = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function",
        }
    ]

    def manage(self) -> None:
        try:
            price = get_price(self.crypto)
        except Exception as e:
            print(f"Error in get_price: {e}")
            return

        # GET RATIO
        ratio_long = self.long.get_ratio(price)
        ratio_short = self.short.get_ratio(price)
        print("price", price)
        print("ratio long:", ratio_long, ", ratio short", ratio_short)
        print("USDC:", self.get_balance_USDC())
        return
        # UPDATE COLLATERAL
        match (
            (ratio_long > self.crit_ratio_long),
            (ratio_short > self.crit_ratio_short),
        ):
            case (True, False):  # Long position needs collateral
                amount = self.get_amount_to_rebalance(self.long)
                self.update_collat(self.long, self.short, amount)
            case (False, True):  # Short position needs collateral
                amount = self.get_amount_to_rebalance(self.short)
                self.update_collat(self.short, self.long, amount)
            case (False, False):  # Both position are under control
                print("No change needed")
            case (
                True,
                True,
            ):  # Both positions are undercollateralized (should not happen)
                print("WARNING: Positions too high")
        return

    def get_amount_to_rebalance(self, position: Position) -> int:
        # to do
        amount = 0
        return amount

    def update_collat(
        self,
        position_add_collat: Position,
        position_remove_collat: Position,
        amount: int,
    ) -> None:
        # Fetch current balance
        try:
            balance = self.get_balance_USDC()
        except Exception as e:
            print(f"Error in get_balance_USDC: {e}")
            return
        time.sleep(5)

        # Remove collateral
        result_remove = position_remove_collat.remove_collateral(amount)
        if result_remove == 0:
            print("Error in remove_collateral")
            return

        # Wait for balance update
        up_balance = balance
        while up_balance == balance:
            time.sleep(15)
            up_balance = self.get_balance_USDC()

        # Add collateral
        result_add = position_add_collat.add_collateral(up_balance)
        if result_add == 0:
            print("Error in add_collateral")
        return

    def get_balance_USDC(self) -> int:
        token_address_USDC = "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"
        w3 = Web3(Web3.HTTPProvider(self.rpc))
        token_contract_address = w3.to_checksum_address(token_address_USDC)
        token_contract = w3.eth.contract(
            address=token_contract_address, abi=self.erc20_abi
        )
        balance_raw = token_contract.functions.balanceOf(
            w3.to_checksum_address(self.address)
        ).call()
        return int(balance_raw)
