// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Notary {
    address public chainOwner;

    mapping(address => bool) public isOrg;
    mapping(address => mapping(address => bool)) public orgAdmins;
    // Welcher Admin gehört zu welcher Org (ein Admin gehört genau einer Org)
    mapping(address => address) public adminOf;
    // Welche Org hält welche documentId
    mapping(bytes32 => address) public docOrg;

    mapping(bytes32 => bytes32) public originalHash;
    mapping(bytes32 => uint256) public timestamps;
    mapping(bytes32 => uint256) public fileTimestamps;

    event DocumentNotarized(bytes32 indexed idHash, bytes32 indexed documentHash, uint256 timestamp);

    modifier onlyChainOwner() {
        require(msg.sender == chainOwner, "Nur Chain Owner");
        _;
    }

    constructor() {
        chainOwner = msg.sender;
    }

    function registerOrg(address orgAddress) external onlyChainOwner {
        require(!isOrg[orgAddress], "Org existiert bereits");
        isOrg[orgAddress] = true;
        orgAdmins[orgAddress][orgAddress] = true;
        adminOf[orgAddress] = orgAddress;
    }

    function addOrgAdmin(address orgAddress, address admin) external {
        require(isOrg[orgAddress], "Org existiert nicht");
        require(
            msg.sender == orgAddress || orgAdmins[orgAddress][msg.sender],
            "Nicht Org-Admin"
        );
        orgAdmins[orgAddress][admin] = true;
        adminOf[admin] = orgAddress;
    }

    function removeOrgAdmin(address orgAddress, address admin) external {
        require(isOrg[orgAddress], "Org existiert nicht");
        require(msg.sender == orgAddress, "Nur Org Owner");
        orgAdmins[orgAddress][admin] = false;
        adminOf[admin] = address(0);
    }

    function getDocOrg(bytes32 idHash) external view returns (address) {
        return docOrg[idHash];
    }

    function storeDocumentHash(bytes32 idHash, bytes32 documentHash) external {
        address org = docOrg[idHash];
        if (org == address(0)) {
            // Erst-Notarisierung: msg.sender muss Org-Admin sein
            address adminOrg = adminOf[msg.sender];
            require(adminOrg != address(0), "Nicht Org-Admin");
            org = adminOrg;
            docOrg[idHash] = org;
        } else {
            // Folgevorgänge: msg.sender muss Admin der verwaltenden Org sein
            require(orgAdmins[org][msg.sender], "Nicht Org-Admin");
        }

        bytes32 zero = bytes32(0);
        bytes32 orig = originalHash[idHash];
        require(orig == zero || orig == documentHash, "Dokument darf nicht geaendert werden");

        bytes32 key = keccak256(abi.encodePacked(idHash, documentHash));
        require(timestamps[key] == 0, "Schon notariell hinterlegt");

        originalHash[idHash]        = documentHash;
        timestamps[key]             = block.timestamp;
        fileTimestamps[documentHash] = block.timestamp;

        emit DocumentNotarized(idHash, documentHash, block.timestamp);
    }
}
