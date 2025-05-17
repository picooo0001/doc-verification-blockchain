# backend/app/routes.py
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, abort, send_file, url_for, session
from flask_login import login_required, current_user
from .web3utils import w3, get_notary_contract_for_org
from .models import db, Document, User, Organization
from io import BytesIO
import json
from eth_utils import is_address, to_checksum_address
from .config import Config

bp = Blueprint("notary", __name__)

pending_files = {} 

with open(Config.CONTRACT_ABI_PATH) as f:
    NOTARY_ABI = json.load(f)['abi']

def owner_required(func):
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_owner:
            abort(403, description="Owner-Rechte erforderlich")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def format_event(e):
    blk = w3.eth.get_block(e.blockNumber)
    ts  = blk.timestamp
    return {
        "documentHash": e.args.documentHash.hex(),
        "timestamp": ts,
        "isoTimestamp": datetime.now(timezone.utc),
        "blockNumber":  e.blockNumber,
        "txHash":       e.transactionHash.hex()
    }

@bp.route("/hashes", methods=["POST"])
@login_required
def prepare_notarize():
    file   = request.files.get("file")
    doc_id = request.form.get("documentId")
    if not file or not doc_id:
        return jsonify(error="file und documentId nötig"), 400

    data     = file.read()
    id_hash  = w3.keccak(text=doc_id).hex()
    doc_hash = w3.keccak(data).hex()

    pending_files[id_hash] = {
        "data": data,
        "mimetype": file.mimetype,
        "user_id": current_user.id
    }

    return jsonify({
        "idHash":  "0x" + id_hash,
        "docHash": "0x" + doc_hash
    }), 200

@bp.route("/notarize/commit", methods=["POST"])
@login_required
def commit_notarize():
    payload = request.get_json() or {}
    raw_id = payload.get("idHash","")
    clean_id = raw_id[2:] if raw_id.startswith("0x") else raw_id
    entry = pending_files.pop(clean_id, None)
    if not entry or entry["user_id"] != current_user.id:
        return jsonify(error="Keine vorbereitete Datei gefunden"), 404

    document = Document(
        document_id = clean_id,
        org_id      = current_user.organization_id,
        file_data   = entry["data"],
        mime_type   = entry["mimetype"],
        tx_hash     = payload.get("txHash")
    )
    db.session.add(document)
    db.session.commit()
    return jsonify(success=True), 200

@bp.route("/verify", methods=["POST"])
@login_required
def verify():
    file = request.files.get("file")
    if not file:
        return jsonify(error="No file provided"), 400

    data     = file.read()
    doc_hash = w3.keccak(data)                   
    contract = get_notary_contract_for_org(current_user.organization)

    if not contract.functions.notarized(doc_hash).call():
        return jsonify(verified=False), 404

    evt_filter = contract.events.DocumentNotarized.create_filter(
        from_block=0,                           
        to_block='latest',                     
        argument_filters={'documentHash': doc_hash}
    )
    events = evt_filter.get_all_entries()
    if not events:
        # sollte nicht passieren, aber zur Sicherheit
        return jsonify(verified=True, timestamp=None), 200

    last_evt = events[-1]
    ts       = last_evt.args.timestamp
    return jsonify(verified=True, timestamp=ts), 200

@bp.route("/documents", methods=["GET"])
@login_required
def list_documents():
    org      = current_user.organization
    contract_address = org.contract_address or ""
    if not contract_address:
        return jsonify({"error": "Kein Contract für diese Organisation hinterlegt"}), 400

    contract = get_notary_contract_for_org(org.contract_address)
    events = contract.events.DocumentNotarized.create_filter(
        from_block=0,
        to_block='latest'
    ).get_all_entries()

    docs = []
    for e in sorted(events, key=lambda e: w3.eth.get_block(e.blockNumber).timestamp, reverse=True):
        fe = format_event(e)
        docs.append({
            "idHash":       e.args.idHash.hex(),
            **fe,
            "downloadUrl":  url_for('notary.download_document', idHash=e.args.idHash.hex(), _external=False)
        })

    return jsonify({
        "orgChainAddress": current_user.wallet_address,
        "contractAddress": w3.to_checksum_address(org.contract_address),
        "documents":       docs
    }), 200

@bp.route("/documents/<string:idHash>/download", methods=["GET"])
@login_required
def download_document(idHash):
    """
    Liefert das zuletzt hochgeladene Blob basierend auf idHash.
    """
    doc = Document.query.filter_by(
        document_id=idHash,
        org_id=current_user.organization.id
    ).order_by(Document.id.desc()).first()
    if not doc:
        abort(404)
    return send_file(
        BytesIO(doc.file_data),
        mimetype=doc.mime_type,
        as_attachment=True,
        download_name=f"{idHash}.pdf"
    )

@bp.route('/stats', methods=['GET'])
@login_required
def stats():
    org = current_user.organization
    ca  = org.contract_address
    if not ca:
        return jsonify({'error':'Kein Contract hinterlegt'}), 404

    from_block = org.deploy_block or 0
    contract = w3.eth.contract(
        address=w3.to_checksum_address(ca),
        abi=NOTARY_ABI
    )

    evt_filter = contract.events.DocumentNotarized.create_filter(
        from_block=from_block,
        to_block='latest'
    )
    events = evt_filter.get_all_entries()
    total  = len(events)

    if total:
        events_sorted = sorted(
            events,
            key=lambda e: w3.eth.get_block(e.blockNumber).timestamp
        )
        first_evt  = events_sorted[0]
        latest_evt = events_sorted[-1]

        first = {
            'timestamp': w3.eth.get_block(first_evt.blockNumber).timestamp,
            'documentHash': first_evt.args.documentHash.hex()
        }
        latest = {
            'timestamp': w3.eth.get_block(latest_evt.blockNumber).timestamp,
            'documentHash': latest_evt.args.documentHash.hex()
        }
    else:
        first  = {}
        latest = {}
    try:
        creator = contract.functions.owner().call()
    except Exception:
        creator = None

    return jsonify({
        'contractAddress':     ca,
        'contractCreator':     creator,
        'deployBlock':         org.deploy_block,
        'totalNotarizations':  total,
        'firstNotarization':   first,
        'latestNotarization':  latest,
    }), 200

@bp.route('/users/me/activities', methods=['GET'])
@login_required
def personal_activities():
    # Organisation des aktuellen Users
    org = Organization.query.get_or_404(current_user.organization_id)
    if not org.contract_address:
        return jsonify({'error': 'Keine Contract-Adresse hinterlegt'}), 404

    # Contract-Instanz und Blockbereich
    contract = get_notary_contract_for_org(org.contract_address)
    start_block = org.deploy_block or 0

    # Alle DocumentNotarized-Events abrufen
    events = contract.events.DocumentNotarized.create_filter(
        from_block=start_block,
        to_block='latest'
    ).get_all_entries()

    # Nur eigene Transaktionen filtern
    activities = []
    user_addr = (current_user.wallet_address or '').lower()
    for e in sorted(events, key=lambda e: e.blockNumber, reverse=True):
        tx = w3.eth.get_transaction(e.transactionHash)
        if tx['from'].lower() != user_addr:
            continue
        activities.append({
            'documentHash': e.args.idHash.hex(),
            'timestamp':     e.args.timestamp,
            'txHash':        e.transactionHash.hex(),
            'blockNumber':   e.blockNumber
        })

    return jsonify({'activities': activities}), 200

#Admin Panel Routen:

@bp.route('/orgs/<int:org_id>/users', methods=['GET'])
@owner_required
def list_org_users(org_id):
    if current_user.organization_id != org_id or not current_user.is_owner:
        abort(403)
    users = User.query.filter_by(organization_id=org_id).all()
    out   = []
    for u in users:
        out.append({
            'id':       u.id,
            'email':    u.email,
            'wallet':   u.wallet_address,
            'is_owner': u.is_owner
        })
    return jsonify({'users': out}), 200

@bp.route('/users/<int:user_id>/wallet', methods=['PUT'])
@owner_required
def update_wallet(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.organization_id != user.organization_id or not current_user.is_owner:
        abort(403)
    data   = request.get_json() or {}
    wallet = data.get('wallet','').strip()
    if wallet and not is_address(wallet):
        return jsonify({'error':'Ungültige Adresse'}), 400
    user.wallet_address = to_checksum_address(wallet) if wallet else None
    db.session.commit()
    return jsonify({'wallet': user.wallet_address}), 200

@bp.route('/get_contract_address', methods=['GET'])
@login_required
def get_contract_address():
    org = Organization.query.get_or_404(current_user.organization_id)

    if not org.contract_address:
        return jsonify({'error': 'Keine Contract-Adresse für diese Organisation hinterlegt'}), 404

    return jsonify({
        'contractAddress': org.contract_address,
        "organization_id": org.id
    }), 200

@bp.route('/get_org_id', methods=['GET'])
@login_required
def get_org_id():
    org = Organization.query.get_or_404(current_user.organization_id)

    return jsonify({
        "organization_id": org.id
    }), 200

@bp.route('/orgs/<int:org_id>/contract', methods=['POST'])
@owner_required
def set_contract_address(org_id):
    org = Organization.query.get_or_404(org_id)
    if current_user.organization_id != org_id or not current_user.is_owner:
        abort(403)

    data = request.get_json() or {}
    address = data.get('contractAddress', '').strip()
    deploy_block = data.get('deployBlock')
    if not address:
        return jsonify({'error': 'Keine contractAddress übergeben'}), 400
    from eth_utils import is_checksum_address
    if not is_checksum_address(address):
        return jsonify({'error': 'Ungültige Ethereum-Adresse'}), 400

    org.contract_address = address
    if isinstance(deploy_block, int):
        org.deploy_block = deploy_block
    db.session.commit()
    return jsonify({
        'contractAddress': org.contract_address,
        'deployBlock': org.deploy_block
    }), 200
