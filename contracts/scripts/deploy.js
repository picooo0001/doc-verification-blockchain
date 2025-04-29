// scripts/deploy.js
const hre = require("hardhat");

async function main() {
  const Notary = await hre.ethers.getContractFactory("Notary");
  const notary = await Notary.deploy();
  await notary.waitForDeployment();                  
  console.log("✅ Notary deployed to:", await notary.getAddress());
}

main()
  .then(() => process.exit(0))
  .catch((err) => {
    console.error("❌ Deployment failed:", err);
    process.exit(1);
  });
