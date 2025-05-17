// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract Notary {
    address public immutable owner;
    mapping(address => bool) public orgAdmins;

    // Neu: Event für Notarisierung
    event DocumentNotarized(
        bytes32 indexed idHash,
        bytes32 indexed documentHash,
        uint256 timestamp
    );
    event AdminAdded(address indexed admin);
    event AdminRemoved(address indexed admin);

    modifier onlyOwner() { require(msg.sender == owner, "Owner only"); _; }
    modifier onlyAdmin() { require(orgAdmins[msg.sender], "Admin only"); _; }

    constructor(address _owner) {
        require(_owner != address(0), "owner = 0");
        owner = _owner;
        orgAdmins[_owner] = true;
    }

    function addOrgAdmin(address admin) external onlyOwner {
        require(!orgAdmins[admin], "exists");
        orgAdmins[admin] = true;
        emit AdminAdded(admin);
    }

    function removeOrgAdmin(address admin) external onlyOwner {
        require(admin != owner, "cannot remove owner");
        require(orgAdmins[admin], "not admin");
        orgAdmins[admin] = false;
        emit AdminRemoved(admin);
    }

    mapping(bytes32 => bool) public notarized;

    // Neu: notarize inklusive idHash & Event-Emit
    function notarize(bytes32 idHash, bytes32 documentHash) external onlyAdmin {
        require(!notarized[documentHash], "already");
        notarized[documentHash] = true;
        emit DocumentNotarized(idHash, documentHash, block.timestamp);
    }

    function isNotarized(bytes32 documentHash) external view returns (bool) {
        return notarized[documentHash];
    }
}