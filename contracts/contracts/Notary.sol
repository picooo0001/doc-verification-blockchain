// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Notary {
    event DocumentNotarized(address indexed sender, bytes32 hash, uint256 timestamp);

    mapping(bytes32 => uint256) public timestamps;

    function storeDocumentHash(bytes32 docHash) external {
        require(timestamps[docHash] == 0, "Schon notariell hinterlegt");
        timestamps[docHash] = block.timestamp;
        emit DocumentNotarized(msg.sender, docHash, block.timestamp);
    }
}