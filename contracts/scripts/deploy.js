// scripts/deploy.js
const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  // 1) Signer holen (deployer + Organisations-Wallets + Admins)
  const [deployer, orgA, adminA1, orgB, adminB1] = await hre.ethers.getSigners();

  // 2) Contract-Factory erstellen
  const Notary = await hre.ethers.getContractFactory("Notary");

  // 3) Notary-Instanz für Org A deployen
  const notaryA = await Notary.connect(deployer).deploy(orgA.address);
  await notaryA.waitForDeployment();
  const addrA = await notaryA.getAddress();
  console.log("✅ Notary A deployed:", addrA);

  // 4) Org A-Admin setzen
  await notaryA.connect(orgA).addOrgAdmin(adminA1.address);
  console.log("🔒 OrgA Admin hinzugefügt:", adminA1.address);

  // 5) Notary-Instanz für Org B deployen
  const notaryB = await Notary.connect(deployer).deploy(orgB.address);
  await notaryB.waitForDeployment();
  const addrB = await notaryB.getAddress();
  console.log("✅ Notary B deployed:", addrB);

  // 6) Org B-Admin setzen
  await notaryB.connect(orgB).addOrgAdmin(adminB1.address);
  console.log("🔒 OrgB Admin hinzugefügt:", adminB1.address);

  // 7) Adressen in eine Datei schreiben (zum Einpflegen in die DB)
  const out = { orgA: addrA, orgB: addrB };
  const file = path.join(__dirname, "../deployed-contracts.json");
  fs.writeFileSync(file, JSON.stringify(out, null, 2));
  console.log("📄 Adressen gesichert in:", file);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
