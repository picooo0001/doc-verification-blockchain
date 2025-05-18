from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db
import pyotp
import qrcode
import io
import base64
from .web3utils import w3
from eth_account.messages import encode_defunct
from hexbytes import HexBytes

bp = Blueprint("auth", __name__)

@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """
    Loggt den aktuellen Benutzer aus der Sitzung aus.

    Ruft logout_user() auf, um den Benutzer abzumelden, und gibt eine
    JSON-Response mit einer Erfolgsmeldung zurück.

    Rückgabe:
        200: {"message": "Logout erfolgreich"} – Bestätigung der Abmeldung
    """
    logout_user()
    return jsonify({"message": "Logout erfolgreich"}), 200

@bp.route("/login", methods=["POST"])
def login():
    """
    Authentifizierungs-Endpoint für Benutzer.

    Unterstützt sowohl JSON- als auch Form-POSTs mit den Feldern:
        - email (str): E-Mail-Adresse des Benutzers
        - password (str): Passwort des Benutzers
        - otp (str, optional): One-Time-Password, falls 2FA aktiviert ist

    Ablauf:
        1. Liest E-Mail, Passwort und optional OTP aus JSON-Payload oder Form-Daten.
        2. Sucht den Benutzer anhand der E-Mail und prüft das Passwort.
           Bei Fehlschlag wird HTTP 401 mit Fehlermeldung zurückgegeben.
        3. Wenn der Benutzer ein otp_secret besitzt, wird OTP-Verifikation verlangt.
           - Fehlt das OTP: HTTP 401 mit {"error": "2FA erforderlich"}
           - Ungültiges OTP: HTTP 401 mit {"error": "Ungültiges OTP"}
        4. Bei erfolgreicher Authentifizierung wird der Benutzer eingeloggt
           und eine JSON-Antwort mit Benutzerinformationen zurückgegeben.

    Rückgabe:
        - 200: {
            "message": "Login erfolgreich",
            "user": {
                "id": int,
                "email": str,
                "isOwner": bool,
                "organizationId": int,
                "wallet": str|None
            }
          }
        - 401: {"error": str} bei ungültigen Anmeldedaten oder fehlender/ungültiger 2FA
    """
    if request.is_json:
        data     = request.get_json()
        email    = data.get("email")
        password = data.get("password")
        otp      = data.get("otp")
    else:
        email    = request.form.get("email")
        password = request.form.get("password")
        otp      = request.form.get("otp")

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Ungültige E-Mail oder Passwort"}), 401

    if user.otp_secret:
        if not otp:
            return jsonify({"error": "2FA erforderlich"}), 401
        if not user.verify_otp(otp):
            return jsonify({"error": "Ungültiges OTP"}), 401

    login_user(user)
    return jsonify({
        "message": "Login erfolgreich",
        "user": {
            "id":       user.id,
            "email":    user.email,
            "isOwner":  user.is_owner,
            "organizationId": user.organization_id,
            "wallet":   user.wallet_address 
        }
    }), 200

@bp.route("/setup-2fa", methods=["GET"])
@login_required
def setup_2fa():
    """
    Generiert das OTP-Secret für den aktuellen Benutzer (falls noch nicht vorhanden),
    erstellt die zugehörige Provisioning-URI für Authenticator-Apps und liefert 
    einen QR-Code als Base64-kodiertes PNG.

    Ablauf:
        1. Holt das aktuelle Benutzerobjekt.
        2. Erzeugt bei Bedarf ein neues otp_secret und speichert es in der Datenbank.
        3. Erstellt mit pyotp eine Provisioning-URI (Issuer: "DocNotary", Nutzer-E-Mail als Name).
        4. Generiert einen QR-Code aus der URI und kodiert ihn als Base64-PNG.

    Rückgabe (JSON, HTTP 200):
        {
            "otp_secret": str,              # Das OTP-Secret für die 2FA
            "provisioning_uri": str,        # URI zum Hinzufügen in Authenticator-Apps
            "qr_code_png_base64": str       # QR-Code als Base64-kodiertes PNG
        }
    """
    user = current_user

    if not user.otp_secret:
        user.generate_otp_secret()
        db.session.commit()

    uri = pyotp.TOTP(user.otp_secret).provisioning_uri(
        name=user.email,
        issuer_name="DocNotary"
    )

    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    qr_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    return jsonify({
        "otp_secret": user.otp_secret,
        "provisioning_uri": uri,
        "qr_code_png_base64": qr_b64
    }), 200

@bp.route("/user/2fa", methods=["POST"])
@login_required
def update_2fa():
    """
    Aktiviert oder deaktiviert 2FA für den eingeloggten Nutzer.
    Bei enable=True: Generiert (falls nötig) ein neues Secret, 
    speichert es, und liefert Secret, Provisioning-URI und QR-Code.
    Bei enable=False: Entfernt das Secret.
    """
    data = request.get_json() or {}
    enable = data.get("enable", False)
    user = current_user

    if enable:
        if not user.otp_secret:
            user.generate_otp_secret()
            db.session.commit()

        uri = pyotp.TOTP(user.otp_secret).provisioning_uri(
            name=user.email,
            issuer_name="DocNotary"
        )

        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(uri)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        qr_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        return jsonify({
            "message": "2FA aktiviert",
            "otp_secret": user.otp_secret,
            "provisioning_uri": uri,
            "qr_code_png_base64": qr_b64
        }), 200

    else:
        user.otp_secret = None
        db.session.commit()
        return jsonify({"message": "2FA deaktiviert"}), 200
        
@bp.route("/login/nonce", methods=["GET"])
def get_nonce():
    """
    Aktiviert oder deaktiviert die Zwei-Faktor-Authentifizierung (2FA) für den aktuellen Benutzer.

    Erwartet ein JSON-Objekt mit dem Feld:
        - enable (bool): True zum Aktivieren der 2FA, False zum Deaktivieren.

    Bei enable=True:
        1. Generiert (falls noch nicht vorhanden) ein neues OTP-Secret und speichert es in der DB.
        2. Erstellt eine Provisioning-URI für Authenticator-Apps (Issuer "DocNotary").
        3. Generiert einen QR-Code aus der URI und kodiert ihn als Base64-PNG.
        4. Gibt zurück:
            - message: "2FA aktiviert"
            - otp_secret: das neue OTP-Secret
            - provisioning_uri: URI für Authenticator
            - qr_code_png_base64: QR-Code als Base64-kodiertes PNG

    Bei enable=False:
        - Entfernt das vorhandene OTP-Secret des Benutzers und speichert die Änderung.
        - Gibt zurück:
            - message: "2FA deaktiviert"

    Rückgabe:
        - 200: JSON-Antwort mit den jeweiligen Feldern bei erfolgreicher (De)Aktivierung.
    """
    raw = request.args.get("address", "")
    if not w3.is_address(raw):
        return jsonify({"error": "Ungültige Adresse"}), 400
    try:
        address = w3.to_checksum_address(raw)
    except ValueError:
        return jsonify({"error": "Ungültiges Adress-Format"}), 400

    user = User.query.filter_by(wallet_address=address).first()
    if not user:
        return jsonify({"error": "Adresse nicht registriert"}), 404

    import os, binascii
    nonce = binascii.hexlify(os.urandom(16)).decode()
    user.login_nonce = nonce
    db.session.commit()

    return jsonify({"nonce": nonce}), 200

@bp.route("/login/wallet", methods=["POST"])
def login_wallet():
    """
    Authentifiziert einen Benutzer mittels Ethereum-Wallet-Signatur.

    Erwartet ein JSON-Objekt mit den Feldern:
        - address (str): Ethereum-Adresse des Nutzers
        - signature (str): Signatur über die zuvor generierte Nonce

    Ablauf:
        1. Validiert die übergebene Adresse; gibt 400 bei ungültigem Format zurück.
        2. Sucht den Nutzer anhand der checksummierten Adresse und prüft, ob eine Nonce vorhanden ist.
           - Fehlende Nonce oder kein Nutzer: 401 mit {"error": "Nonce nicht gefunden"}.
        3. Erstellt eine Nachricht aus der Nonce und versucht, die Signatur wiederherzustellen.
           - Fehlschlag: 401 mit {"error": "Signatur ungültig"}.
        4. Vergleicht die wiederhergestellte Adresse mit der übergebenen:
           - Abweichung: 401 mit {"error": "Address mismatch"}.
        5. Setzt die Nonce auf None, speichert die Änderung, loggt den Nutzer ein und liefert
           eine JSON-Antwort mit Benutzerinfos.

    Rückgabe:
        - 200: {
            "message": "Login erfolgreich",
            "user": {
                "id": int,
                "email": str,
                "isOwner": bool,
                "organizationId": int,
                "wallet": str
            }
          }
        - 400: {"error": "Ungültige Adresse" | "Ungültiges Adress-Format"}
        - 401: {"error": "Nonce nicht gefunden" | "Signatur ungültig" | "Address mismatch"}
    """
    data      = request.get_json() or {}
    raw       = data.get("address", "")
    signature = data.get("signature")

    if not w3.is_address(raw):
        return jsonify({"error": "Ungültige Adresse"}), 400
    try:
        address = w3.to_checksum_address(raw)
    except ValueError:
        return jsonify({"error": "Ungültiges Adress-Format"}), 400

    user = User.query.filter_by(wallet_address=address).first()
    if not user or not user.login_nonce:
        return jsonify({"error": "Nonce nicht gefunden"}), 401

    message = encode_defunct(text=user.login_nonce)
    try:
        recovered = w3.eth.account.recover_message(message, signature=HexBytes(signature))
    except Exception:
        return jsonify({"error": "Signatur ungültig"}), 401

    if recovered != address:
        return jsonify({"error": "Address mismatch"}), 401

    user.login_nonce = None
    db.session.commit()
    login_user(user)
    
    return jsonify({
        "message": "Login erfolgreich",
        "user": {
            "id":       user.id,
            "email":    user.email,
            "isOwner":  user.is_owner,
            "organizationId": user.organization_id,
            "wallet":   user.wallet_address
        }
    }), 200

@bp.route("/user/profile", methods=["GET"])
@login_required
def user_profile():
    """
    Gibt das Profil des aktuell angemeldeten Benutzers zurück.

    Liest die E-Mail, den Organisationsnamen, den 2FA-Status, die Wallet-Adresse
    und die Owner-Rolle des aktuellen Nutzers aus und gibt diese Informationen
    als JSON-Response zurück.

    Rückgabe (HTTP 200):
        {
            "email": str,               # E-Mail-Adresse des Nutzers
            "organization": str,        # Name der Organisation
            "2faEnabled": bool,         # True, wenn 2FA aktiviert ist
            "walletAddress": str|None,  # Wallet-Adresse oder None, falls nicht gesetzt
            "isOwner": bool             # True, wenn der Nutzer Owner-Rechte besitzt
        }
    """
    wallet = current_user.wallet_address
    return jsonify({
        "email": current_user.email,
        "organization": current_user.organization.name,
        "2faEnabled": bool(current_user.otp_secret),
        "walletAddress": wallet if wallet else None,
        "isOwner": bool(current_user.is_owner)
    }), 200