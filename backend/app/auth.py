from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Organization
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
    logout_user()
    return jsonify({"message": "Logout erfolgreich"}), 200

# Normale Login Routen (Email + PW + (OTP))

@bp.route("/login", methods=["POST"])
def login():
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
    Generiert und liefert dem eingeloggten Nutzer sein OTP-Secret,
    die Provisioning-URI und den QR-Code als Base64-PNG.
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
    
# Wallet Login:
    
@bp.route("/login/nonce", methods=["GET"])
def get_nonce():
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

#User Profile fetching:
@bp.route("/user/profile", methods=["GET"])
@login_required
def user_profile():
    wallet = current_user.wallet_address
    return jsonify({
        "email": current_user.email,
        "organization": current_user.organization.name,
        "2faEnabled": bool(current_user.otp_secret),
        "walletAddress": wallet if wallet else None,
        "isOwner": bool(current_user.is_owner)
    }), 200