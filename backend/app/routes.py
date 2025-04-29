from flask import Blueprint, request, jsonify
from .web3utils import w3, contract, default_sender_account

bp = Blueprint("notary", __name__)

@bp.route("/notarize", methods=["POST"])
def notarize():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file provided"}), 400

    data = file.read()
    doc_hash = w3.keccak(data)

    # Pre-Check: bereits notariell?
    if contract.functions.timestamps(doc_hash).call() != 0:
        return jsonify({"error": "Dokument schon notariell hinterlegt"}), 400

    # Transaction aufbauen
    #Debugging: print(f"[routes] Using contract.address = {contract.address}")
    nonce = w3.eth.get_transaction_count(default_sender_account)
    tx = contract.functions.storeDocumentHash(doc_hash).build_transaction({
        "from": default_sender_account,
        #"to": contract.address,
        "nonce": nonce,
        "gas": 200_000,
        "gasPrice": w3.to_wei("1", "gwei"),
    })

    # senden & Receipt abwarten
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

    ts = contract.functions.timestamps(doc_hash).call()
    if ts == 0:
        return jsonify({"verified": False}), 404

    return jsonify({"verified": True, "timestamp": ts}), 200
