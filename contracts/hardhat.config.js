require("dotenv").config({ path: __dirname + "/../.env" });
require("@nomicfoundation/hardhat-toolbox");
require("@nomicfoundation/hardhat-verify");

module.exports = {
  solidity: '0.8.28',
  networks: {
    sepolia: {
      url: process.env.RPC_URL,         // z.B. https://sepolia.infura.io/v3/...
      accounts: [process.env.DEPLOYER_KEY], // Dein privater Key des Owner-Accounts
    },
  },
  etherscan: {
    apiKey: process.env.ETHERSCAN_API_KEY,
  },
  sourcify: {
    enabled: true
  }
};