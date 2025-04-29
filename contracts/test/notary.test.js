// test/notary.test.js

const { expect } = require("chai");
const { ethers } = require("hardhat");
const { anyValue } = require("@nomicfoundation/hardhat-chai-matchers/withArgs");

describe("Notary (with immutable originalHash per ID)", function () {
  let notary, owner;

  before(async () => {
    const Notary = await ethers.getContractFactory("Notary");
    [owner] = await ethers.getSigners();
    notary = await Notary.deploy();
    await notary.waitForDeployment();
  });

  it("stores a new document hash under a given id and emits an event", async () => {
    const documentId = "mitarbeiter-123";
    const idHash = ethers.keccak256(ethers.toUtf8Bytes(documentId));
    const documentHash = ethers.keccak256(ethers.toUtf8Bytes("MeinDokument"));

    // Store
    const tx = await notary.storeDocumentHash(idHash, documentHash);
    await expect(tx)
      .to.emit(notary, "DocumentNotarized")
      .withArgs(idHash, documentHash, anyValue);

    // Prüfe timestamp über getTimestamp
    const ts = await notary.getTimestamp(idHash, documentHash);
    expect(ts).to.be.gt(0);

    // Prüfe zusätzlich das neue Mapping fileTimestamps
    const fileTs = await notary.fileTimestamps(documentHash);
    expect(fileTs).to.equal(ts);
  });

  it("reverts when storing the same id+hash twice", async () => {
    const documentId = "mitarbeiter-456";
    const idHash = ethers.keccak256(ethers.toUtf8Bytes(documentId));
    const documentHash = ethers.keccak256(ethers.toUtf8Bytes("AnderesDokument"));

    // erster Aufruf → OK
    await expect(notary.storeDocumentHash(idHash, documentHash)).not.to.be.reverted;

    // zweiter Aufruf derselben Kombination → revert mit require-Message
    await expect(
      notary.storeDocumentHash(idHash, documentHash)
    ).to.be.revertedWith("Schon notariell hinterlegt");
  });

  it("reverts when storing a different hash under the same id", async () => {
    const documentId = "mitarbeiter-789";
    const idHash = ethers.keccak256(ethers.toUtf8Bytes(documentId));
    const hashA = ethers.keccak256(ethers.toUtf8Bytes("VersionA"));
    const hashB = ethers.keccak256(ethers.toUtf8Bytes("VersionB"));

    // Erstes Dokument → OK
    await expect(notary.storeDocumentHash(idHash, hashA)).not.to.be.reverted;

    // Anderes Dokument unter derselben ID → revert mit Änderung-Verbot
    await expect(notary.storeDocumentHash(idHash, hashB))
      .to.be.revertedWith("Dokument darf nicht geaendert werden");
  });

  it("allows the same file under different ids", async () => {
    const content = ethers.toUtf8Bytes("GleicheDatei");
    const hash = ethers.keccak256(content);
    const idHash1 = ethers.keccak256(ethers.toUtf8Bytes("id1"));
    const idHash2 = ethers.keccak256(ethers.toUtf8Bytes("id2"));

    await expect(notary.storeDocumentHash(idHash1, hash)).not.to.be.reverted;
    await expect(notary.storeDocumentHash(idHash2, hash)).not.to.be.reverted;
  });
});
