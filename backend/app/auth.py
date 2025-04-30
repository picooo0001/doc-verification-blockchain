from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db
import pyotp
import qrcode
import io
import base64

bp = Blueprint("auth", __name__)

@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout erfolgreich"}), 200

# auth.py

bp = Blueprint("auth", __name__)

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

