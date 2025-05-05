// scripts/deploy.js
const hre = require("hardhat");

async function main() {
  const [chainOwner, orgWallet, orgAdmin] = await hre.ethers.getSigners();
  const Notary = await hre.ethers.getContractFactory("Notary");
  const notary = await Notary.connect(chainOwner).deploy();
  await notary.waitForDeployment();
  console.log("✅ Notary deployed to:", await notary.getAddress());

  // 1) Org registrieren (chainOwner -> registerOrg)
  await notary.connect(chainOwner).registerOrg(orgWallet.address);
  console.log(`🏷️  Registered organization: ${orgWallet.address}`);

  // 2) Admin hinzufügen (orgWallet -> addOrgAdmin)
  await notary.connect(orgWallet).addOrgAdmin(orgWallet.address, orgAdmin.address);
  console.log(`🔒 Org admin granted:      ${orgAdmin.address}`);

  console.log("🎉 Deployment & Org setup complete");
}

main()
  .then(() => process.exit(0))
  .catch((err) => {
    console.error("❌ Deployment failed:", err);
    process.exit(1);
  });
