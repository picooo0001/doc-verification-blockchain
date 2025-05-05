from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from .web3utils import w3, contract, default_sender_account, get_user_org_address
from web3 import Web3

bp = Blueprint("notary", __name__)

@bp.route("/notarize", methods=["POST"])
@login_required
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
@login_required
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

@bp.route("/documents", methods=["GET"])
@login_required
def list_documents():
    """
    Listet alle Dokumente auf, die zur Organisation des aktuellen Nutzers gehören.
    """
    org_addr = get_user_org_address(current_user).lower()
    events = contract.events.DocumentNotarized.create_filter(from_block=0).get_all_entries()

    docs = []
    for ev in events:
        owner = contract.functions.getDocOrg(ev.args.idHash).call()
        if owner.lower() != org_addr:
            continue
        docs.append({
            "idHash":       ev.args.idHash.hex(),
            "documentHash": ev.args.documentHash.hex(),
            "timestamp":    ev.args.timestamp,
            "txHash":       ev.transactionHash.hex(),
            "blockNumber":  ev.blockNumber
        })
    return jsonify(docs), 200

@bp.route("/documents/<string:documentId>", methods=["GET"])
@login_required
def get_document(documentId):
    """
    Gibt Details zu einem einzelnen Dokument zurück, wenn es zur Organisation gehört.
    """
    org_addr = get_user_org_address(current_user).lower()
    id_hash = w3.keccak(text=documentId)

    # Prüfe, ob die Org dieses Dokument hält
    owner = contract.functions.getDocOrg(id_hash).call()
    if owner.lower() != org_addr:
        return jsonify({"error": "Nicht berechtigt"}), 403

    entries = contract.events.DocumentNotarized.create_filter(
        from_block=0,
        argument_filters={"idHash": id_hash}
    ).get_all_entries()

    if not entries:
        return jsonify({"error": "Document not found"}), 404

    ev = entries[0]
    return jsonify({
        "documentId":    documentId,
        "idHash":        ev.args.idHash.hex(),
        "documentHash":  ev.args.documentHash.hex(),
        "timestamp":     ev.args.timestamp,
        "txHash":        ev.transactionHash.hex(),
        "blockNumber":   ev.blockNumber
    }), 200

@bp.route("/stats", methods=["GET"])
@login_required
def stats():
    """
    Liefert Kennzahlen zur eigenen Organisation:
      - totalNotarizations
      - latestNotarization { documentHash, timestamp }
    """
    org_addr = get_user_org_address(current_user).lower()
    events = contract.events.DocumentNotarized.create_filter(from_block=0).get_all_entries()
    own = [
        e for e in events
        if contract.functions.getDocOrg(e.args.idHash).call().lower() == org_addr
    ]

    total = len(own)
    latest = None
    if own:
        ev = max(own, key=lambda e: e.args.timestamp)
        latest = {
            "documentHash": ev.args.documentHash.hex(),
            "timestamp":    ev.args.timestamp
        }

    return jsonify({
        "totalNotarizations": total,
        "latestNotarization": latest
    }), 200

@bp.route("/documents/<string:documentId>/history", methods=["GET"])
@login_required
def document_history(documentId):
    """
    Liefert die komplette Historie der Notarisierungen für eine documentId:
      - documentHash
      - timestamp
      - txHash
      - blockNumber
    """
    # 1) Organisations-Check
    org_addr = get_user_org_address(current_user).lower()
    id_hash  = w3.keccak(text=documentId)

    # 2) Prüfe, ob die Org dieses Dokument hält
    owner = contract.functions.getDocOrg(id_hash).call()
    if owner.lower() != org_addr:
        return jsonify({"error": "Nicht berechtigt"}), 403

    # 3) Alle DocumentNotarized-Events für diese ID abholen
    events = contract.events.DocumentNotarized.create_filter(
        from_block=0,
        argument_filters={"idHash": id_hash}
    ).get_all_entries()

    # 4) Eine Liste von History-Einträgen zusammenstellen
    history = []
    for ev in events:
        history.append({
            "documentHash": ev.args.documentHash.hex(),
            "timestamp":    ev.args.timestamp,
            "txHash":       ev.transactionHash.hex(),
            "blockNumber":  ev.blockNumber
        })

    return jsonify(history), 200

