const path = require("path");
require("dotenv").config({ path: path.resolve(__dirname, "../../.env"), quiet: true });
const { ethers } = require("ethers");

// --- ENV VARIABLES ---
const PRIVATE_KEY = process.env.PRIVATE_KEY;
const WALLET_ADDRESS = process.env.WALLET_ADDRESS;
const RPC_URL = process.env.RPC_URL;
const HYPERLIQUID_BRIDGE_ADDRESS = "0x2Df1c51E09aECF9cacB7bc98cB1742757f163dF7";
const USDC_ADDRESS = "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"

if (!PRIVATE_KEY || !WALLET_ADDRESS || !RPC_URL) {
  throw new Error("Check your .env file: all variables are required.");
}
// --- PROVIDER / WALLET ---
const provider = new ethers.JsonRpcProvider(RPC_URL);
const wallet = new ethers.Wallet(PRIVATE_KEY, provider);

// --- GET ARGUMENT ---
const args = process.argv.slice(2);
if (args.length < 1) {
    console.error("Usage: node deposit.js <borrowAmount>");
    process.exit(1);
}
const depositAmount = ethers.parseUnits(args[0], 0); // (amount in wei)

const ERC20_ABI = [
  "function transfer(address to, uint256 amount) external returns (bool)",
  "function balanceOf(address owner) view returns (uint256)"
];

async function main() {
  const usdc = new ethers.Contract(USDC_ADDRESS, ERC20_ABI, wallet);

  const balance = await usdc.balanceOf(WALLET_ADDRESS);
  if (balance < depositAmount) {
    throw new Error("Not enough USDC in wallet.");
  }

  // Transfer directly to Hyperliquid Bridge
  const tx = await usdc.transfer(HYPERLIQUID_BRIDGE_ADDRESS, depositAmount);
  await tx.wait();
  console.log("Transaction sent to deposit:", tx.hash)
  console.log("Deposit confirmed");
}

main().catch((err) => {
  console.error("Error:", err);
  process.exit(1);
});
