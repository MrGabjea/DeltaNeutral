import os
import subprocess
from dataclasses import dataclass

from ..position import Position


@dataclass
class Hyperliquid(Position):

    key: str = "0x"
    wallet_address: str = "0x"

    def add_collateral(self, amount: int) -> int:
        src_dir = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(src_dir, "blockchain_calls", "hyperliquid_deposit.js")
        print(file_path)
        if not os.path.exists(file_path):
            print(f"ERROR: {file_path} not found")
            return 0
        try:
            print(f"Adding collateral {amount}...", end="")
            result = subprocess.run(
                ["node", file_path, str(amount)],
                capture_output=True,
                text=True,
                check=True,
            )
            print(" Done")
            print("Output:", result.stdout.strip())
        except subprocess.CalledProcessError as e:
            print("Erreur lors de l'exécution JS :")
            print(e.stderr)
            return 0
        self.amount_collateral += amount
        return 1

    def remove_collateral(self, amount: int) -> int:
        units = amount // 10**6

        from hyperliquid.utils import constants
        from eth_account import Account
        from hyperliquid.exchange import Exchange

        wallet = Account.from_key(self.key)
        exchange = Exchange(wallet=wallet, base_url=constants.MAINNET_API_URL)

        print(f"Removing collateral {amount}...", end="")
        try:
            withdraw_result = exchange.withdraw_from_bridge(units, self.wallet_address)
            print("Done")
            print(withdraw_result)
        except Exception as e:
            print(f"Failed: {e}")
            return 0
        self.amount_collateral -= amount
        return 1
