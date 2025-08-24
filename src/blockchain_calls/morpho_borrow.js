const path = require("path");
require("dotenv").config({ path: path.resolve(__dirname, "../../.env"), quiet: true });
const { ethers } = require("ethers");

// --- ENV VARIABLES ---
const PRIVATE_KEY = process.env.PRIVATE_KEY;
const WALLET_ADDRESS = process.env.WALLET_ADDRESS;
const RPC_URL = process.env.RPC_URL;
const BUNDLER_V3_ADDRESS = "0x1FA4431bC113D308beE1d46B0e98Cb805FB48C13";
const MORPHO_ADAPTER_ADDRESS = "0x9954aFB60BB5A222714c478ac86990F221788B88";

if (!PRIVATE_KEY || !WALLET_ADDRESS || !RPC_URL) {
  throw new Error("Check your .env file: all variables are required.");
}

// --- MARKET PARAMS ---
const marketParams = {
  loanToken: "0xaf88d065e77c8cc2239327c5edb3a432268e5831", // USDC
  collateralToken: "0x2f2a2543b76a4166549f7aab2e75bef0aefc5b0f", // WBTC
  oracle: "0x88193fcb705d29724a40bb818ecaa47dd5f014d9",
  irm: "0x66f30587fb8d4206918deb78eca7d5ebbafd06da",
  lltv: "860000000000000000" // LLTV
};

// --- PROVIDER / WALLET ---
const provider = new ethers.JsonRpcProvider(RPC_URL);
const wallet = new ethers.Wallet(PRIVATE_KEY, provider);

// --- CONTRACT ABI ---
const bundlerAbi = [
  "function multicall((address to,bytes data,uint256 value,bool skipRevert,bytes32 callbackHash)[] bundle) payable"
];
const morphoBorrowAbi = [
  "function morphoBorrow((address loanToken,address collateralToken,address oracle,address irm,uint256 lltv) marketParams,uint256 assets,uint256 shares,uint256 minSharePriceE27,address receiver)"
];

async function borrowFromMorpho(borrowAmount) {
  try {
    const morphoInterface = new ethers.Interface(morphoBorrowAbi);

    // Encoding morphoBorrow Call
    const morphoBorrowData = morphoInterface.encodeFunctionData("morphoBorrow", [
      [
        marketParams.loanToken,
        marketParams.collateralToken,
        marketParams.oracle,
        marketParams.irm,
        marketParams.lltv
      ],
      borrowAmount,    // assets (amount to borrow)
      0,              // shares (0 pour borrower en assets)
      0,              // minSharePriceE27 (0 = pas de protection slippage)
      WALLET_ADDRESS  // receiver
    ]);

    // Create bundle for Bundler
    const bundle = [{
      to: MORPHO_ADAPTER_ADDRESS,
      data: morphoBorrowData,
      value: 0,
      skipRevert: false,
      callbackHash: "0x0000000000000000000000000000000000000000000000000000000000000000"
    }];

    // Create Bundler
    const bundlerContract = new ethers.Contract(BUNDLER_V3_ADDRESS, bundlerAbi, wallet);

    // Execute transaction
    const tx = await bundlerContract.multicall(bundle);
    const receipt = await tx.wait();

    return {
      success: true,
      txHash: tx.hash,
      blockNumber: receipt.blockNumber
    };

  } catch (error) {
    console.error("Error during borrow:", error);
    return {
      success: false,
      error: error.message
    };
  }
}

// Get argument for borrow
const args = process.argv.slice(2);
if (args.length < 1) {
    console.error("Usage: node borrow.js <borrowAmount>");
    process.exit(1);
}
// --- MAIN FONCTION ---
async function main() {
  const borrowAmountUSDC = ethers.parseUnits(args[0], 0);
  const result = await borrowFromMorpho(borrowAmountUSDC);

  if (result.success) {
    console.log("Transaction sent to borrow:", result.txHash);
    console.log("Transaction confirmed");
  } else {
    console.log(`Error: ${result.error}`);
  }
}

main().catch(console.error);
