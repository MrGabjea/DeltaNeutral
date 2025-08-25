import os
import subprocess
from dataclasses import dataclass

from ..position import Position


@dataclass
class Morpho(Position):
    """
    This class represents a morpho position,
    The  market parameters are hard-coded in the files `morpho_borrow.js` and morpho_repay.js`
    and need to be changed depending on the position represented
    """

    def add_collateral(self, amount: int) -> int:
        src_dir = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(src_dir, "blockchain_calls", "morpho_repay.js")
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
            return 1
        except subprocess.CalledProcessError as e:
            print("Erreur lors de l'exécution JS :")
            print(e.stderr)
            return 0
        self.amount_collateral += amount
        return 1

    def remove_collateral(self, amount: int) -> int:
        src_dir = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(src_dir, "blockchain_calls", "morpho_borrow.js")
        print(file_path)
        if not os.path.exists(file_path):
            print(f"ERROR: {file_path} not found")
            return 0
        try:
            print(f"Removing collateral {amount}...", end="")
            result = subprocess.run(
                ["node", file_path, str(amount)],
                capture_output=True,
                text=True,
                check=True,
            )
            print(" Done")
            print("Output:", result.stdout.strip())
            return 1
        except subprocess.CalledProcessError as e:
            print("Erreur lors de l'exécution JS :")
            print(e.stderr)
            return 0
        self.amount_collateral -= amount
        return 1
