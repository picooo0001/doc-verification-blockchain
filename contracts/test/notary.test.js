const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Notary with org-based access control", function () {
  let Notary, notary;
  let chainOwner, orgA, adminA1, adminA2, outsider;

  beforeEach(async () => {
    [chainOwner, orgA, adminA1, adminA2, outsider] = await ethers.getSigners();
    Notary = await ethers.getContractFactory("Notary");
    notary = await Notary.connect(chainOwner).deploy();
    await notary.waitForDeployment();

    // Org A registrieren, Org-Wallet wird automatisch Admin seiner selbst
    await notary.connect(chainOwner).registerOrg(orgA.address);
    // Zwei weitere Admins hinzufügen
    await notary.connect(orgA).addOrgAdmin(orgA.address, adminA1.address);
    await notary.connect(orgA).addOrgAdmin(orgA.address, adminA2.address);
  });

  it("allows any org admin to notarize under the org", async () => {
    const idHash = ethers.keccak256(ethers.toUtf8Bytes("id1"));
    const docHash = ethers.keccak256(ethers.toUtf8Bytes("docA"));

    // Erst-Notarisierung durch adminA1 → OK
    await expect(
      notary.connect(adminA1).storeDocumentHash(idHash, docHash)
    ).to.emit(notary, "DocumentNotarized");

    // Zweiter Versuch derselben Kombination → revert wegen Schon notariell hinterlegt
    await expect(
      notary.connect(adminA1).storeDocumentHash(idHash, docHash)
    ).to.be.revertedWith("Schon notariell hinterlegt");
  });

  it("prevents outsider from notarizing for the org", async () => {
    const idHash = ethers.keccak256(ethers.toUtf8Bytes("id2"));
    const docHash = ethers.keccak256(ethers.toUtf8Bytes("docB"));

    await expect(
      notary.connect(outsider).storeDocumentHash(idHash, docHash)
    ).to.be.revertedWith("Nicht Org-Admin");
  });

  it("prevents admins of other orgs from accessing", async () => {
    // Org B registrieren (outsider wird Org-Wallet und Admin)
    await notary.connect(chainOwner).registerOrg(outsider.address);

    const idHashA = ethers.keccak256(ethers.toUtf8Bytes("sharedId"));
    const docHashA = ethers.keccak256(ethers.toUtf8Bytes("docA"));
    // Org A Admin notariert
    await notary.connect(adminA1).storeDocumentHash(idHashA, docHashA);

    // Org B Admin (outsider) versucht für dieselbe ID → revert
    await expect(
      notary.connect(outsider).storeDocumentHash(idHashA, docHashA)
    ).to.be.revertedWith("Nicht Org-Admin");
  });

  it("correctly reports docOrg mapping", async () => {
    const idHash = ethers.keccak256(ethers.toUtf8Bytes("id3"));
    const docHash = ethers.keccak256(ethers.toUtf8Bytes("docC"));

    await notary.connect(adminA2).storeDocumentHash(idHash, docHash);
    expect(await notary.getDocOrg(idHash)).to.equal(orgA.address);
  });
});
