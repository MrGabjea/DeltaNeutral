import os
import subprocess
from dataclasses import dataclass

from ..position import Position


@dataclass
class Fluid(Position):
    id: int = 0  # nftId of the Vault

    def add_collateral(self, amount: int) -> int:
        src_dir = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(src_dir, "blockchain_calls", "fluid_repay.js")
        print(file_path)
        if not os.path.exists(file_path):
            print(f"ERROR: {file_path} not found")
            return 0
        try:
            print(f"Adding collateral {amount}...", end="")
            result = subprocess.run(
                ["node", file_path, str(amount), str(self.id)],
                capture_output=True,
                text=True,
                check=True,
            )
            print(" Done")
            print("Output:", result.stdout.strip())
        except subprocess.CalledProcessError as e:
            # print("Erreur lors de l'exécution JS :")
            print(e.stderr)
        self.amount_collateral += amount
        return 1

    def remove_collateral(self, amount: int) -> int:
        src_dir = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(src_dir, "blockchain_calls", "fluid_borrow.js")
        print(file_path)
        if not os.path.exists(file_path):
            print(f"ERROR: {file_path} not found")
            return 0
        try:
            print(f"Removing collateral {amount}...", end="")
            result = subprocess.run(
                ["node", file_path, str(amount), str(self.id)],
                capture_output=True,
                text=True,
                check=True,
            )
            print(" Done")
            print("Output:", result.stdout.strip())
        except subprocess.CalledProcessError as e:
            # print("Erreur lors de l'exécution JS :")
            print(e.stderr)
        self.amount_collateral -= amount
        return 1
