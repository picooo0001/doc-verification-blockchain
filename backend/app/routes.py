from flask import Blueprint, request, jsonify
from .web3utils import w3, contract, default_sender_account
from web3 import Web3

bp = Blueprint("notary", __name__)

@bp.route("/notarize", methods=["POST"])
def notarize():
    file = request.files.get("file")
    doc_id = request.form.get("documentId")
    if not file:
        return jsonify({"error": "No file provided"}), 400
    if not doc_id:
        return jsonify({"error": "No documentId provided"}), 400

    data = file.read()
    # 1) Erzeuge den raw-Hash (bytes32)
    doc_hash = w3.keccak(data)

    # 2) ID-Hash (bytes32)
    id_hash = w3.keccak(text=doc_id)

    # 3) Original-Hash aus dem Contract holen – rohes bytes32
    orig_bytes = contract.functions.originalHash(id_hash).call()

    # 4) Pre-Check: wenn orig_bytes nicht Null-Hash und nicht derselbe Hash → verboten
    zero32 = b'\x00' * 32
    if orig_bytes != zero32 and orig_bytes != doc_hash:
        return jsonify({"error": "Dokument darf nicht geändert werden"}), 400

    # 5) Key fürs Timestamp-Mapping bauen (wie im Contract)
    key = w3.keccak(id_hash + doc_hash)
    if contract.functions.timestamps(key).call() != 0:
        return jsonify({"error": "Schon notariell hinterlegt"}), 400

    # 6) Transaktion bauen und senden
    nonce = w3.eth.get_transaction_count(default_sender_account)
    tx = contract.functions.storeDocumentHash(id_hash, doc_hash).build_transaction({
        "from": default_sender_account,
        "nonce": nonce,
        "gas": 200_000,
        "gasPrice": w3.to_wei("1", "gwei"),
    })
    tx_hash = w3.eth.send_transaction(tx)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return jsonify({
        "txHash": receipt.transactionHash.hex(),
        "blockNumber": receipt.blockNumber
    }), 200

@bp.route("/verify", methods=["POST"])
def verify():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file provided"}), 400

    data = file.read()
    doc_hash = w3.keccak(data)

    # Prüfe globalen Dateihash (neues Mapping fileTimestamps)
    ts = contract.functions.fileTimestamps(doc_hash).call()    
    if ts == 0:
        return jsonify({"verified": False}), 404

    return jsonify({"verified": True, "timestamp": ts}), 200