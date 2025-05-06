// contracts/Notary.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Notary {
    address public orgWallet;
    mapping(address => bool) public orgAdmins;
    mapping(bytes32 => bytes32) public originalHash;
    mapping(bytes32 => uint256) public timestamps;
    mapping(bytes32 => uint256) public fileTimestamps;

    event DocumentNotarized(
        address indexed org,
        bytes32 indexed idHash,
        bytes32 indexed documentHash,
        uint256 timestamp
    );

    modifier onlyOrgAdminOrWallet() {
        require(msg.sender == orgWallet || orgAdmins[msg.sender], "Nicht Org-Admin");
        _;
    }

    constructor(address _orgWallet) {
        require(_orgWallet != address(0), "Ungueltige Org-Adresse");
        orgWallet = _orgWallet;
    }

    function addOrgAdmin(address admin) external onlyOrgAdminOrWallet {
        require(admin != address(0), "Ungueltige Adresse");
        orgAdmins[admin] = true;
    }

    function storeDocumentHash(bytes32 idHash, bytes32 documentHash)
        external onlyOrgAdminOrWallet
    {
        require(timestamps[idHash] == 0, "Schon notariell hinterlegt");
        bytes32 orig = originalHash[idHash];
        require(orig == bytes32(0) || orig == documentHash, "Dokument geaendert");
        originalHash[idHash] = documentHash;
        timestamps[idHash] = block.timestamp;
        fileTimestamps[documentHash] = block.timestamp;
        emit DocumentNotarized(orgWallet, idHash, documentHash, block.timestamp);
    }

    function getDocOrg(bytes32 idHash) external view returns (address) {
        if (timestamps[idHash] != 0) return orgWallet;
        return address(0);
    }

    function verify(bytes32 documentHash) external view returns (bool) {
        return fileTimestamps[documentHash] != 0;
    }
}