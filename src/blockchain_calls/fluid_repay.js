const path = require('path');
require('dotenv').config({ path: path.resolve(__dirname, '../../.env'), quiet: true });

const { ethers } = require('ethers');

// --- ENVIRONMENT VARIABLES ---
const PRIVATE_KEY = process.env.PRIVATE_KEY;
const WALLET_ADDRESS = process.env.WALLET_ADDRESS;
const RPC_URL = process.env.RPC_URL;
const VAULT_MANAGER_ADDRESS = "0xeAbBfca72F8a8bf14C4ac59e69ECB2eB69F0811C";

if (!PRIVATE_KEY || !WALLET_ADDRESS || !RPC_URL || !VAULT_MANAGER_ADDRESS) {
    throw new Error("Check your .env file: all variables are required.");
}

// --- PROVIDER / WALLET SETUP ---
const provider = new ethers.JsonRpcProvider(RPC_URL);
const wallet = new ethers.Wallet(PRIVATE_KEY, provider);

// --- MINIMAL ABI FOR operate() ---
const vaultManagerAbi = [
    "function operate(uint256 nftId_, int256 newCol_, int256 newDebt_, address to_) external returns (uint256, int256, int256)"
];

// --- CONTRACT ---
const vaultManager = new ethers.Contract(VAULT_MANAGER_ADDRESS, vaultManagerAbi, wallet);

// --- COMMAND LINE ARGUMENTS ---
// Usage: node repay.js <repayAmount> <nftId>
const args = process.argv.slice(2);
if (args.length < 1) {
    console.error("Usage: node repay.js <borrowAmount> <nftId>");
    process.exit(1);
}

const repayAmount = -1n * ethers.parseUnits(args[0], 0);// amount to repay
const nftId = parseInt(args[1]);       // 0 = create new position
const toAddress = WALLET_ADDRESS;

// --- MAIN FUNCTION ---
async function repayPosition() {

    const tx = await vaultManager.operate(
        nftId,
        0,             // newCol_ = 0, no collateral added
        repayAmount,  // < 0, means repay
        toAddress
    );

    console.log("Transaction sent to repay:", tx.hash);
    const receipt = await tx.wait();
    console.log("Transaction confirmed");
}

// --- EXECUTION ---
repayPosition().catch(console.error);
