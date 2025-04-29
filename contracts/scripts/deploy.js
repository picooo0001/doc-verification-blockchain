// scripts/deploy.js
async function main() {
    const Notary = await ethers.getContractFactory("Notary");
    const notary = await Notary.deploy();
    await notary.waitForDeployment();
    console.log("Notary deployed to:", notary.target);
  }
  
  main().catch((err) => {
    console.error(err);
    process.exitCode = 1;
  });
  