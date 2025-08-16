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
        if not os.path.exists(file_path):
            print(f"ERROR: {file_path} not found")
            return 0
        try:
            subprocess.run(
                [
                    "node",
                    file_path,
                    str(amount),
                ],
                capture_output=True,
                text=True,
                check=True,
            )
        except Exception as e:
            print(f"ERROR: {e}")
            return 0
        return 1

    def remove_collateral(self, amount: int) -> int:
        src_dir = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(src_dir, "blockchain_calls", "fluid_borrow.js")
        if not os.path.exists(file_path):
            print(f"ERROR: {file_path} not found")
            return 0
        try:
            subprocess.run(
                [
                    "node",
                    file_path,
                    str(amount),
                ],
                capture_output=True,
                text=True,
                check=True,
            )
        except Exception as e:
            print(f"ERROR: {e}")
            return 0
        return 1
