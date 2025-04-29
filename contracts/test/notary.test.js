// test/notary.test.js

const { expect } = require("chai");
const { ethers } = require("hardhat");
// Import anyValue aus dem withArgs-Subpaket
const { anyValue } = require("@nomicfoundation/hardhat-chai-matchers/withArgs");

describe("Notary", function () {
  let notary, owner;

  before(async () => {
    const Notary = await ethers.getContractFactory("Notary");
    [owner] = await ethers.getSigners();
    notary = await Notary.deploy();
    await notary.waitForDeployment();
  });

  it("stores a new document hash and emits an event", async () => {
    // Beispiel-Hash für "MeinDokument"
    const docHash = ethers.keccak256(ethers.toUtf8Bytes("MeinDokument"));

    // Event-Prüfung mit anyValue als Placeholder für den Timestamp
    await expect(notary.storeDocumentHash(docHash))
      .to.emit(notary, "DocumentNotarized")
      .withArgs(owner.address, docHash, anyValue);

    // Mapping-Eintrag prüfen (Timestamp > 0)
    const ts = await notary.timestamps(docHash);
    expect(ts).to.be.gt(0);
  });

  it("reverts when storing the same hash twice", async () => {
    const docHash = ethers.keccak256(ethers.toUtf8Bytes("MeinDokument"));
    await expect(notary.storeDocumentHash(docHash))
      .to.be.revertedWith("Schon notariell hinterlegt");
  });
});
