# backend/app/routes.py

from flask import Blueprint, request, jsonify, abort
from flask_login import login_required, current_user
from web3 import Web3
from .web3utils import w3, get_notary_contract_for_org, get_user_org_address

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
    doc_hash = w3.keccak(data)
    id_hash = w3.keccak(text=doc_id)

    contract = get_notary_contract_for_org(current_user.organization)

    orig_bytes = contract.functions.originalHash(id_hash).call()
    if orig_bytes != (b"\x00"*32) and orig_bytes != doc_hash:
        return jsonify({"error": "Dokument darf nicht geändert werden"}), 400

    key = w3.keccak(id_hash + doc_hash)
    if contract.functions.timestamps(key).call() != 0:
        return jsonify({"error": "Schon notariell hinterlegt"}), 400

    sender = get_user_org_address(current_user)
    nonce  = w3.eth.get_transaction_count(sender)
    tx = contract.functions.storeDocumentHash(id_hash, doc_hash).build_transaction({
        "from": sender,
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
    contract = get_notary_contract_for_org(current_user.organization)

    ts = contract.functions.fileTimestamps(doc_hash).call()
    if ts == 0:
        return jsonify({"verified": False}), 404

    return jsonify({"verified": True, "timestamp": ts}), 200

@bp.route("/documents", methods=["GET"])
@login_required
def list_documents():
    """
    Listet alle Dokumente auf, die zur Organisation des aktuellen Nutzers gehören.
    Zusätzlich werden Org-Chain-Address und Contract-Address mitgeliefert.
    """
    org = current_user.organization
    contract = get_notary_contract_for_org(org)
    events = contract.events.DocumentNotarized.create_filter(from_block=0).get_all_entries()

    docs = []
    for ev in sorted(events, key=lambda e: e.args.timestamp, reverse=True):
        docs.append({
            "idHash":       ev.args.idHash.hex(),
            "documentHash": ev.args.documentHash.hex(),
            "timestamp":    ev.args.timestamp,
            "txHash":       ev.transactionHash.hex(),
            "blockNumber":  ev.blockNumber
        })

    return jsonify({
        "orgChainAddress": org.chain_address,
        "contractAddress": org.contract_address,
        "documents": docs
    }), 200

@bp.route("/documents/<string:documentId>", methods=["GET"])
@login_required
def get_document(documentId):
    id_hash = w3.keccak(text=documentId)
    org = current_user.organization
    contract = get_notary_contract_for_org(org)

    if contract.functions.timestamps(id_hash).call() == 0:
        return jsonify({"error": "Document not found"}), 404

    entries = contract.events.DocumentNotarized.create_filter(
        from_block=0,
        argument_filters={"idHash": id_hash}
    ).get_all_entries()
    ev = entries[0]
    return jsonify({
        "organization":    org.name,
        "orgChainAddress": org.chain_address,
        "contractAddress": org.contract_address,
        "documentId":      documentId,
        "idHash":          ev.args.idHash.hex(),
        "documentHash":    ev.args.documentHash.hex(),
        "timestamp":       ev.args.timestamp,
        "txHash":          ev.transactionHash.hex(),
        "blockNumber":     ev.blockNumber
    }), 200

@bp.route("/stats", methods=["GET"])
@login_required
def stats():
    """
    Liefert Kennzahlen zur eigenen Organisation:
      - orgChainAddress
      - contractAddress
      - totalNotarizations
      - firstNotarization {documentHash, timestamp}
      - latestNotarization {documentHash, timestamp}
    """
    org = current_user.organization
    contract = get_notary_contract_for_org(org)
    events = contract.events.DocumentNotarized.create_filter(from_block=0).get_all_entries()

    sorted_events = sorted(events, key=lambda e: e.args.timestamp)
    total = len(sorted_events)
    first = None
    latest = None
    if total > 0:
        ev_first = sorted_events[0]
        ev_last  = sorted_events[-1]
        first = {
            "documentHash": ev_first.args.documentHash.hex(),
            "timestamp":    ev_first.args.timestamp
        }
        latest = {
            "documentHash": ev_last.args.documentHash.hex(),
            "timestamp":    ev_last.args.timestamp
        }

    return jsonify({
        "orgName":          org.name,
        "orgChainAddress": org.chain_address,
        "contractAddress": org.contract_address,
        "totalNotarizations": total,
        "firstNotarization": first,
        "latestNotarization": latest
    }), 200

@bp.route("/documents/<string:documentId>/history", methods=["GET"])
@login_required
def document_history(documentId):
    """
    Liefert die komplette Historie der Notarisierungen für eine documentId,
    inklusive Org- und Contract-Info. Sortiert nach Zeitstempel aufsteigend.
    """
    id_hash = w3.keccak(text=documentId)
    org = current_user.organization
    contract = get_notary_contract_for_org(org)

    entries = contract.events.DocumentNotarized.create_filter(
        from_block=0,
        argument_filters={"idHash": id_hash}
    ).get_all_entries()

    if not entries:
        return jsonify({"error": "Document not found"}), 404

    history = []
    for ev in sorted(entries, key=lambda e: e.args.timestamp):
        history.append({
            "documentHash": ev.args.documentHash.hex(),
            "timestamp":    ev.args.timestamp,
            "txHash":       ev.transactionHash.hex(),
            "blockNumber":  ev.blockNumber
        })

    return jsonify({
        "orgName":          org.name,
        "orgChainAddress": org.chain_address,
        "contractAddress": org.contract_address,
        "history":         history
    }), 200
