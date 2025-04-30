from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
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
    # E-Mail, Passwort und optionales OTP aus dem Request holen
    email = request.form.get("email")
    password = request.form.get("password")
    otp = request.form.get("otp")  # OTP ist optional

    # Benutzer anhand der E-Mail ermitteln
    user = User.query.filter_by(email=email).first()
    # Überprüfen, ob Benutzer existiert und Passwort korrekt ist
    if not user or not user.check_password(password):
        return jsonify({"error": "Ungültige E-Mail oder Passwort"}), 401

    # Wenn 2FA aktiviert ist (otp_secret hinterlegt), muss ein gültiges OTP mitgeliefert werden
    if user.otp_secret:
        # Überprüfen, ob ein OTP eingegeben wurde und ob es korrekt ist
        if not otp or not user.verify_otp(otp):
            return jsonify({"error": "Ungültiges OTP"}), 401

    # Anmeldung erfolgreich, Benutzer einloggen
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
#@login_required
def user_profile():
    return jsonify({
        "email": current_user.email,
        "organization": current_user.organization.name,
        "2faEnabled": bool(current_user.otp_secret)
    }), 200
