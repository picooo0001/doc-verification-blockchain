// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Notary {
    // Speichert für jede ID den ersten Dokument-Hash
    mapping(bytes32 => bytes32) public originalHash;
    // Speichert Timestamp unter dem kombinierten Key keccak(idHash, documentHash)
    mapping(bytes32 => uint256) public timestamps;
    mapping(bytes32 => uint256) public fileTimestamps;


    event DocumentNotarized(
        bytes32 indexed idHash,
        bytes32 indexed documentHash,
        uint256 timestamp
    );

    /// @notice Speichert einen Dokument-Hash unter einer ID, einmalig und unveränderlich
    function storeDocumentHash(bytes32 idHash, bytes32 documentHash) external {
        bytes32 orig = originalHash[idHash];
        if (orig == bytes32(0)) {
            // erste Notarisierung für diese ID
            originalHash[idHash] = documentHash;
        } else {
            // nur derselbe Hash ist erlaubt, Änderungen verboten
            require(
                documentHash == orig,
                "Dokument darf nicht geaendert werden"
            );
        }

        bytes32 key = keccak256(abi.encodePacked(idHash, documentHash));
        require(timestamps[key] == 0, "Schon notariell hinterlegt");

        timestamps[key] = block.timestamp;
        fileTimestamps[documentHash] = block.timestamp;
        
        emit DocumentNotarized(idHash, documentHash, block.timestamp);
    }

    /// @notice Gibt den Timestamp zurück, wenn diese ID+Hash-Kombi existiert
    function getTimestamp(bytes32 idHash, bytes32 documentHash)
        external
        view
        returns (uint256)
    {
        bytes32 key = keccak256(abi.encodePacked(idHash, documentHash));
        return timestamps[key];
    }
}
