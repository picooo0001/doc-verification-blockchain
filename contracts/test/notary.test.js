// test/notary.test.js
const { expect } = require("chai");
const { ethers } = require("hardhat");
const { anyValue } = require("@nomicfoundation/hardhat-chai-matchers/withArgs");

describe("Notary – pro-Organisation-Instanz", function () {
  let Notary, notaryA, notaryB;
  let owner, orgA, adminA1, orgB, adminB1, outsider;

  beforeEach(async () => {
    [owner, orgA, adminA1, orgB, adminB1, outsider] = await ethers.getSigners();
    Notary = await ethers.getContractFactory("Notary");
    notaryA = await Notary.connect(owner).deploy(orgA.address);
    await notaryA.waitForDeployment();
    notaryB = await Notary.connect(owner).deploy(orgB.address);
    await notaryB.waitForDeployment();
    await notaryA.connect(orgA).addOrgAdmin(adminA1.address);
    await notaryB.connect(orgB).addOrgAdmin(adminB1.address);
  });

  it("ermöglicht Org-Admins, Dokumente zu notarisieren", async () => {
    const idHash = ethers.keccak256(ethers.toUtf8Bytes("id1"));
    const docHash = ethers.keccak256(ethers.toUtf8Bytes("docA"));
    await expect(
      notaryA.connect(adminA1).storeDocumentHash(idHash, docHash)
    )
      .to.emit(notaryA, "DocumentNotarized")
      .withArgs(orgA.address, idHash, docHash, anyValue);
  });

  it("verhindert Outsider-Notarisierung", async () => {
    const idHash = ethers.keccak256(ethers.toUtf8Bytes("id2"));
    const docHash = ethers.keccak256(ethers.toUtf8Bytes("docB"));
    await expect(
      notaryA.connect(outsider).storeDocumentHash(idHash, docHash)
    ).to.be.revertedWith("Nicht Org-Admin");
  });

  it("verhindert doppelte Notarisierung in derselben Instanz", async () => {
    const idHash = ethers.keccak256(ethers.toUtf8Bytes("dup1"));
    const docHash = ethers.keccak256(ethers.toUtf8Bytes("docDup"));
    await notaryA.connect(adminA1).storeDocumentHash(idHash, docHash);
    await expect(
      notaryA.connect(adminA1).storeDocumentHash(idHash, docHash)
    ).to.be.revertedWith("Schon notariell hinterlegt");
  });

  it("ermöglicht getrennte Notarisierung derselben ID in verschiedenen Instanzen", async () => {
    const idHash = ethers.keccak256(ethers.toUtf8Bytes("shared2"));
    const docA = ethers.keccak256(ethers.toUtf8Bytes("docA"));
    const docB = ethers.keccak256(ethers.toUtf8Bytes("docB"));
    await expect(
      notaryA.connect(adminA1).storeDocumentHash(idHash, docA)
    )
      .to.emit(notaryA, "DocumentNotarized")
      .withArgs(orgA.address, idHash, docA, anyValue);
    await expect(
      notaryB.connect(adminB1).storeDocumentHash(idHash, docB)
    )
      .to.emit(notaryB, "DocumentNotarized")
      .withArgs(orgB.address, idHash, docB, anyValue);
  });
});