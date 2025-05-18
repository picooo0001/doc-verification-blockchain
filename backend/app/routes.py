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
    """
    Dekorator, der sicherstellt, dass ein Benutzer eingeloggt ist und über Owner-Rechte verfügt.
    
    Wenn der Benutzer nicht eingeloggt ist, wird er durch @login_required weitergeleitet.
    Wenn der Benutzer eingeloggt, aber kein Owner ist, wird ein HTTP-403-Fehler ausgelöst.
    """
    @login_required
    def wrapper(*args, **kwargs):
        """
        Wrapper-Funktion, die vor dem Aufruf der ursprünglichen Funktion überprüft,
        ob der aktuelle Benutzer Owner-Rechte besitzt.
        """
        if not current_user.is_owner:
            abort(403, description="Owner-Rechte erforderlich")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def format_event(e):
    """
    Formatiert ein Ethereum-Event-Objekt zu einem lesbaren Dictionary.

    Ruft den zugehörigen Block ab, extrahiert den Zeitstempel und wandelt
    die relevanten Felder des Events in ein Python-Dictionary um.

    :param e: Web3 Event-Objekt mit den Attributen blockNumber, args und transactionHash
    :type e: web3.datastructures.AttributeDict
    :return: Dictionary mit folgenden Schlüsseln:
        - documentHash (str): Hex-codierter Dokument-Hash aus e.args.documentHash
        - timestamp (int): Unix-Timestamp des Blocks
        - isoTimestamp (datetime): Aktuelles Datum/Uhrzeit in UTC
        - blockNumber (int): Block-Nummer des Events
        - txHash (str): Hex-codierte Transaktions-Hash
    """
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
    """
    Bereitet die Notarisierung eines Dokuments vor.

    Liest die hochgeladene Datei und die übergebene Dokumenten-ID aus dem POST-Request,
    berechnet je einen Keccak-256-Hash für die Dokumenten-ID (idHash) und den Dateiinhaltes (docHash)
    und speichert die Datei zusammen mit Metadaten zur späteren Verarbeitung in pending_files.

    Form-Parameter:
        file (werkzeug.datastructures.FileStorage): Hochgeladene Datei unter dem Schlüssel "file"
        documentId (str): Eindeutige Dokumenten-ID unter dem Schlüssel "documentId"

    Speichert in:
        pending_files[id_hash] (dict): Dictionary mit:
            - "data" (bytes): Rohdaten der Datei
            - "mimetype" (str): MIME-Typ der Datei
            - "user_id" (int): ID des aktuellen Benutzers

    Rückgabe:
        JSON-Response mit:
            - idHash (str): Hexadezimaler Keccak-256-Hash der Dokumenten-ID, präfixiert mit "0x"
            - docHash (str): Hexadezimaler Keccak-256-Hash des Dateiinhalts, präfixiert mit "0x"
        HTTP-Statuscodes:
            - 200: Hashes erfolgreich generiert
            - 400: Fehlender Upload oder fehlende Dokumenten-ID
    """
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
    """
    Führt die Commit-Phase der Notarisierung durch.

    Liest die JSON-Payload des Requests aus, extrahiert und bereinigt den idHash,
    prüft, ob eine vorbereitete Datei existiert und dem aktuellen Benutzer gehört,
    erstellt ein Document-Objekt und speichert es in der Datenbank.

    Erwartete JSON-Felder:
        - idHash (str): Hexadezimaler Keccak-256-Hash der Dokumenten-ID (mit oder ohne "0x"-Präfix)
        - txHash (str): Transaktions-Hash der Blockchain-Notarisierung

    Ablauf:
        1. Extrahiert raw_id aus der Payload und entfernt optionales "0x"-Präfix.
        2. Holt den Eintrag aus pending_files und prüft die Benutzer-Zugehörigkeit.
        3. Erzeugt ein Document-Objekt mit Feldern:
           - document_id: bereinigter idHash
           - org_id: Organisations-ID des aktuellen Benutzers
           - file_data: Rohdaten der Datei
           - mime_type: MIME-Typ der Datei
           - tx_hash: übergebener Transaktions-Hash
        4. Speichert das Document in der Datenbank und bestätigt mit success=True.

    Rückgabe:
        - 200: {"success": True} bei erfolgreichem Commit
        - 404: {"error": "Keine vorbereitete Datei gefunden"} wenn keine passende Datei existiert oder der Benutzer nicht berechtigt ist
    """
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
    """
    Verifiziert, ob eine hochgeladene Datei bereits notariell beglaubigt wurde.

    Liest die hochgeladene Datei aus dem POST-Request, berechnet den Keccak-256-Hash
    des Inhalts und prüft über den Smart Contract, ob dieser Hash notariell registriert ist.
    Falls registriert, werden alle zugehörigen DocumentNotarized-Events gefiltert,
    und der Zeitstempel des letzten Events zurückgegeben.

    Form-Parameter:
        file (werkzeug.datastructures.FileStorage): Hochgeladene Datei unter dem Schlüssel "file"

    Ablauf:
        1. Datei aus dem Request entnehmen; bei Fehlen HTTP 400 zurückgeben.
        2. Keccak-256-Hash des Dateiinhalts berechnen.
        3. Notary-Contract der Organisation des aktuellen Benutzers laden.
        4. Über contract.functions.notarized(doc_hash).call() prüfen, ob der Hash registriert ist.
        5. Wenn nicht registriert, HTTP 404 mit {"verified": False}.
        6. Ansonsten DocumentNotarized-Events mit matching documentHash abrufen.
        7. Wenn keine Events gefunden werden, {"verified": True, "timestamp": None}.
        8. Sonst Zeitstempel des letzten Events ausgeben: {"verified": True, "timestamp": ts}.

    Rückgabe:
        - 200: {"verified": True, "timestamp": <int|None>}
        - 404: {"verified": False} wenn der Hash nicht registriert ist
        - 400: {"error": "No file provided"} wenn keine Datei übergeben wurde
    """
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
    """
    Listet alle notariell registrierten Dokumente der aktuellen Organisation auf.

    Liest die Smart-Contract-Adresse der Organisation des aktuellen Benutzers,
    lädt den Notary-Contract und holt alle DocumentNotarized-Events von Block 0 bis 'latest'.
    Sortiert die Events nach Block-Timestamp absteigend und formatiert jedes Event
    mithilfe von format_event(). Fügt zu jedem Eintrag die Download-URL für das Dokument hinzu.

    Rückgabe:
        JSON-Response mit:
            - orgChainAddress (str): Wallet-Adresse der Organisation des Benutzers
            - contractAddress (str): Checksummiert korrigierte Contract-Adresse
            - documents (List[dict]): Liste von Dokument-Einträgen mit Feldern:
                * idHash (str): Dokumenten-ID-Hash (hexadezimal)
                * documentHash (str): Datei-Hash (hexadezimal)
                * timestamp (int): Unix-Timestamp des Notarisierungs-Blocks
                * isoTimestamp (datetime): Zeitstempel in ISO/UTC
                * blockNumber (int): Block-Nummer
                * txHash (str): Transaktion-Hash (hexadezimal)
                * downloadUrl (str): Interne URL zum Herunterladen des Dokuments
        HTTP-Statuscodes:
            - 200: Liste erfolgreich erstellt
            - 400: Kein Contract für die Organisation hinterlegt
    """
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
    Liefert das zuletzt gespeicherte Dokument-Blob für den gegebenen idHash als Datei-Download.

    :param idHash: Hexadezimaler Keccak-256-Hash der Dokumenten-ID, ohne "0x"-Präfix
    :type idHash: str
    :raises 404: Wenn kein Dokument mit diesem idHash für die Organisation des aktuellen Benutzers gefunden wird
    :return: Flask Response-Objekt, das die Datei mit dem Original-MIME-Typ als Anhang zurückgibt
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
    """
    Liefert Statistiken zur Notarisierung für die Organisation des aktuellen Benutzers.

    Holt die Contract-Adresse und den optionalen Deploy-Block der Organisation,
    liest alle DocumentNotarized-Events aus dem Smart Contract von from_block bis 'latest',
    und berechnet Metriken wie Gesamtzahl der Notarisierungen, erstes und letztes Event.
    Zusätzlich wird versucht, den Contract-Owner abzufragen.

    Rückgabe:
        JSON-Response mit folgenden Feldern:
        - contractAddress (str): Smart-Contract-Adresse der Organisation
        - contractCreator (str|None): Adresse des Contract-Besitzers (sofern verfügbar)
        - deployBlock (int|None): Blocknummer, ab der Events gelesen werden (falls gesetzt)
        - totalNotarizations (int): Gesamtanzahl der gefundenen Notarisierungs-Events
        - firstNotarization (dict): 
            • timestamp (int): Unix-Timestamp des ersten Events  
            • documentHash (str): Hash des ersten notarierten Dokuments  
          (leer, falls keine Events)
        - latestNotarization (dict):
            • timestamp (int): Unix-Timestamp des letzten Events  
            • documentHash (str): Hash des letzten notarierten Dokuments  
          (leer, falls keine Events)

    HTTP-Statuscodes:
        - 200: Statistiken erfolgreich ermittelt
        - 404: Kein Contract für die Organisation hinterlegt
    """
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
    """
    Liefert eine Liste aller eigenen Notarisierungs-Aktivitäten des aktuellen Benutzers.

    Liest die Contract-Adresse und den optionalen Deploy-Block der Organisation des Benutzers,
    lädt alle DocumentNotarized-Events im relevanten Blockbereich und filtert dann
    diejenigen Transaktionen heraus, die vom Wallet des aktuellen Benutzers initiiert wurden.

    Rückgabe:
        JSON-Response mit:
            - activities (List[dict]): Liste der Aktivitäten, sortiert nach absteigender Blocknummer:
                * documentHash (str): Hexadezimaler Hash der Dokumenten-ID
                * timestamp (int): Unix-Timestamp der Notarisierung
                * txHash (str): Transaktions-Hash (hexadezimal)
                * blockNumber (int): Block-Nummer der Transaktion
        HTTP-Statuscodes:
            - 200: Aktivitäten erfolgreich ermittelt
            - 404: Keine Contract-Adresse für die Organisation hinterlegt
    """
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
    """
    Gibt alle Benutzer einer Organisation zurück; nur Owner dürfen darauf zugreifen.

    Überprüft, ob der aktuelle Benutzer Owner der angeforderten Organisation ist.
    Liest alle User-Einträge der Organisation aus der Datenbank und gibt eine Liste
    mit Benutzerinfos zurück.

    :param org_id: ID der Organisation, für die die Benutzerliste angefordert wird
    :type org_id: int
    :raises 403: Wenn der aktuelle Benutzer nicht Owner der Organisation ist
    :return: JSON-Response mit:
        - users (List[dict]): Liste von Benutzerobjekten mit Feldern:
            * id (int): Benutzer-ID
            * email (str): E-Mail-Adresse des Benutzers
            * wallet (str): Wallet-Adresse des Benutzers
            * is_owner (bool): Gibt an, ob der Benutzer Owner-Rechte besitzt
        HTTP-Statuscode 200 bei Erfolg
    """
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
    """
    Aktualisiert die Wallet-Adresse eines Benutzers innerhalb der Organisation.

    Diese Route ist nur für Owner der Organisation zugänglich. Liest die neue
    Wallet-Adresse aus der JSON-Payload, validiert sie und speichert die
    checksummierte Adresse in der Datenbank.

    :param user_id: ID des Benutzers, dessen Wallet-Adresse aktualisiert werden soll
    :type user_id: int
    :raises 403: Wenn der aktuelle Benutzer nicht Owner der Organisation ist
    :raises 400: Wenn die angegebene Adresse ungültig ist
    :return: JSON-Response mit:
        - wallet (str|None): Die neue, gespeicherte Wallet-Adresse oder None
        HTTP-Statuscode 200 bei Erfolg
    """
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
    """
    Gibt die Smart-Contract-Adresse der Organisation des aktuellen Benutzers zurück.

    Liest die Organisation des eingeloggten Benutzers aus der Datenbank und prüft, ob
    eine Contract-Adresse hinterlegt ist. Gibt bei Erfolg die Adresse und die
    Organisations-ID als JSON zurück.

    Rückgabe:
        200:
            {
                "contractAddress": str,
                "organization_id": int
            }
        404:
            {
                "error": str
            }
    """
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
    """
    Gibt die ID der Organisation des aktuell angemeldeten Benutzers zurück.

    Liest die Organisation des eingeloggten Benutzers anhand current_user.organization_id
    aus der Datenbank und gibt deren ID als JSON-Response zurück.

    Rückgabe:
        200: {"organization_id": int} – Die ID der Organisation
        404: Standard-Fehler, wenn die Organisation nicht gefunden wird
    """
    org = Organization.query.get_or_404(current_user.organization_id)

    return jsonify({
        "organization_id": org.id
    }), 200

@bp.route('/orgs/<int:org_id>/contract', methods=['POST'])
@owner_required
def set_contract_address(org_id):
    """
    Legt die Smart-Contract-Adresse und optional den Deploy-Block einer Organisation fest.

    Diese Route ist nur für Organisation-Owner zugänglich. Liest die neue Contract-Adresse
    und optional den Deploy-Block aus der JSON-Payload, validiert die Adresse und speichert
    die Angaben in der Datenbank.

    Erwartenes JSON-Format:
        {
            "contractAddress": str,  # Checksummierte Ethereum-Contract-Adresse
            "deployBlock": int       # Optional, Blocknummer des Vertrags-Deployments
        }

    Validierungen:
        - contractAddress muss vorhanden sein und eine gültige checksummierte Adresse sein.
        - deployBlock wird nur übernommen, wenn es sich um einen Integer handelt.

    Rückgabe:
        200: {
            "contractAddress": str,  # Gespeicherte Contract-Adresse
            "deployBlock": int       # Gespeicherter Deploy-Block (oder None)
        }
        400: {"error": str}         # Fehlende oder ungültige Eingaben
        403:                        # Wenn der Benutzer nicht Owner der Organisation ist
        404:                        # Wenn die Organisation nicht existiert
    """
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
