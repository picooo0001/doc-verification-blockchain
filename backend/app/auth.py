from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db
import pyotp
import qrcode
import io
import base64

# neue Imports
import os, binascii
from .web3utils import w3
from eth_account.messages import encode_defunct
from hexbytes import HexBytes

bp = Blueprint("auth", __name__)

@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout erfolgreich"}), 200

@bp.route("/login", methods=["POST"])
def login():
    # 1) Payload lesen (Form-Data oder JSON)
    if request.is_json:
        data     = request.get_json()
        email    = data.get("email")
        password = data.get("password")
        otp      = data.get("otp")
    else:
        email    = request.form.get("email")
        password = request.form.get("password")
        otp      = request.form.get("otp")

    # 2) Benutzer & Passwort prüfen
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Ungültige E-Mail oder Passwort"}), 401

    # 3) 2FA-Flow: fehlt otp?
    if user.otp_secret:
        if not otp:
            # kein OTP im Request → OTP erforderlich
            return jsonify({"error": "2FA erforderlich"}), 401
        if not user.verify_otp(otp):
            # falsches OTP
            return jsonify({"error": "Ungültiges OTP"}), 401

    # 4) alles ok → Login
    login_user(user)
    return jsonify({"message": "Login erfolgreich"}), 200

@bp.route("/setup-2fa", methods=["GET"])
@login_required
def setup_2fa():
    """
    Generiert und liefert dem eingeloggten Nutzer sein OTP-Secret,
    die Provisioning-URI und den QR-Code als Base64-PNG.
    """
    user = current_user

    # 1) Neues OTP-Secret nur generieren, wenn noch keines vorhanden ist
    if not user.otp_secret:
        user.generate_otp_secret()
        db.session.commit()

    # 2) Provisioning-URI nach RFC6238 für den Authenticator erstellen
    uri = pyotp.TOTP(user.otp_secret).provisioning_uri(
        name=user.email,
        issuer_name="DocNotary"
    )

    # 3) QR-Code für die Provisioning-URI erzeugen
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")

    # 4) QR-Code in PNG konvertieren und als Base64 kodieren
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    qr_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    return jsonify({
        "otp_secret": user.otp_secret,
        "provisioning_uri": uri,
        "qr_code_png_base64": qr_b64
    }), 200

@bp.route("/user/profile", methods=["GET"])
@login_required
def user_profile():
    return jsonify({
        "email": current_user.email,
        "organization": current_user.organization.name,
        "2faEnabled": bool(current_user.otp_secret)
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
        # 2FA aktivieren: Secret generieren, wenn noch keines existiert
        if not user.otp_secret:
            user.generate_otp_secret()
            db.session.commit()

        # Provisioning-URI erstellen
        uri = pyotp.TOTP(user.otp_secret).provisioning_uri(
            name=user.email,
            issuer_name="DocNotary"
        )

        # QR-Code erzeugen und als Base64 kodieren
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
        # 2FA deaktivieren: Secret entfernen
        user.otp_secret = None
        db.session.commit()
        return jsonify({"message": "2FA deaktiviert"}), 200
    
# neue Login Route für Wallet based Logn

@bp.route("/login/nonce", methods=["GET"])
def get_nonce():
    raw = request.args.get("address", "")
    # 1) Gültige Ethereum-Adresse?
    if not w3.is_address(raw):
        return jsonify({"error": "Ungültige Adresse"}), 400
    # 2) Checksummen-Format
    try:
        address = w3.to_checksum_address(raw)
    except ValueError:
        return jsonify({"error": "Ungültiges Adress-Format"}), 400

    user = User.query.filter_by(wallet_address=address).first()
    if not user:
        return jsonify({"error": "Adresse nicht registriert"}), 404

    # 3) Nonce erzeugen und speichern
    import os, binascii
    nonce = binascii.hexlify(os.urandom(16)).decode()
    user.login_nonce = nonce
    db.session.commit()

    return jsonify({"nonce": nonce}), 200

@bp.route("/login/wallet", methods=["POST"])
def login_wallet():
    data      = request.get_json() or {}
    raw       = data.get("address", "")
    signature = data.get("signature")

    # 1) Adresse validieren & normalisieren
    if not w3.is_address(raw):
        return jsonify({"error": "Ungültige Adresse"}), 400
    try:
        address = w3.to_checksum_address(raw)
    except ValueError:
        return jsonify({"error": "Ungültiges Adress-Format"}), 400

    # 2) User + Nonce prüfen
    user = User.query.filter_by(wallet_address=address).first()
    if not user or not user.login_nonce:
        return jsonify({"error": "Nonce nicht gefunden"}), 401

    # 3) Signatur prüfen
    message = encode_defunct(text=user.login_nonce)
    try:
        recovered = w3.eth.account.recover_message(message, signature=HexBytes(signature))
    except Exception:
        return jsonify({"error": "Signatur ungültig"}), 401

    if recovered != address:
        return jsonify({"error": "Address mismatch"}), 401

    # 4) Login abschließen
    user.login_nonce = None
    db.session.commit()
    login_user(user)
    return jsonify({"message": "Login erfolgreich"}), 200
