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

const morphoRepayAbi = [
  "function morphoRepay((address loanToken,address collateralToken,address oracle,address irm,uint256 lltv) marketParams,uint256 assets,uint256 shares,uint256 maxSharePriceE27,address onBehalf,bytes data)"
];

const adapterAbi = [
  "function erc20TransferFrom(address token, address receiver, uint256 amount)"
];

async function repayToMorpho(repayAmount) {
  try {
    const morphoInterface = new ethers.Interface(morphoRepayAbi);
    const adapterInterface = new ethers.Interface(adapterAbi);

    // 1. Premier appel : erc20TransferFrom - Pull USDC depuis votre wallet vers l'adapter
    const erc20TransferFromData = adapterInterface.encodeFunctionData("erc20TransferFrom", [
      marketParams.loanToken, // token: USDC address
      MORPHO_ADAPTER_ADDRESS,  // receiver: l'adapter lui-même
      repayAmount             // amount: montant à transférer
    ]);

    // 2. Deuxième appel : morphoRepay - L'adapter utilise les USDC pour rembourser
    const morphoRepayData = morphoInterface.encodeFunctionData("morphoRepay", [
      [
        marketParams.loanToken,
        marketParams.collateralToken,
        marketParams.oracle,
        marketParams.irm,
        marketParams.lltv
      ],
      repayAmount, // assets - montant exact à rembourser
      0, // shares - 0 car on spécifie assets
      ethers.MaxUint256, // maxSharePriceE27 - pas de limite (accepte n'importe quel prix)
      WALLET_ADDRESS, // onBehalf - votre adresse
      "0x" // data - empty
    ]);

    // Bundle avec les 2 appels vers l'adapter
    const bundle = [
      {
        to: MORPHO_ADAPTER_ADDRESS, // erc20TransferFrom sur l'adapter
        data: erc20TransferFromData,
        value: 0,
        skipRevert: false,
        callbackHash: "0x0000000000000000000000000000000000000000000000000000000000000000"
      },
      {
        to: MORPHO_ADAPTER_ADDRESS, // morphoRepay sur l'adapter
        data: morphoRepayData,
        value: 0,
        skipRevert: false,
        callbackHash: "0x0000000000000000000000000000000000000000000000000000000000000000"
      }
    ];

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
    console.error("Error during repay:", error);
    return {
      success: false,
      error: error.message
    };
  }
}

// Get argument for repay
const args = process.argv.slice(2);
if (args.length < 1) {
  console.error("Usage: node repay.js <repayAmount>");
  process.exit(1);
}

// --- MAIN FONCTION ---
async function main() {
  const repayAmountUSDC = ethers.parseUnits(args[0], 0);

  const result = await repayToMorpho(repayAmountUSDC);

  if (result.success) {
    console.log("Transaction sent to repay:", result.txHash);
    console.log("Transaction confirmed - Debt repaid successfully");
  } else {
    console.log(`Error: ${result.error}`);
  }
}

main().catch(console.error);
