from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db
import pyotp
import qrcode
import io
import base64

bp = Blueprint("auth", __name__)

@bp.route("/login", methods=["POST"])
def login():
    email    = request.form.get("email")
    password = request.form.get("password")
    otp      = request.form.get("otp")  # optional

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Ungültige E-Mail oder Passwort"}), 401

    # falls OTP eingerichtet, muss Token stimmen
    if user.otp_secret and not user.verify_otp(otp):
        return jsonify({"error": "Ungültiges OTP"}), 401

    login_user(user)
    return jsonify({"message": "Login erfolgreich"}), 200

@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout erfolgreich"}), 200

@bp.route("/setup-2fa", methods=["GET"])
@login_required
def setup_2fa():
    """
    Generiert und liefert dem eingeloggten Nutzer sein OTP-Secret,
    die Provisioning-URI und den QR-Code als Base64-PNG.
    """
    user = current_user

    # 1) Secret neu generieren, falls noch nicht vorhanden
    if not user.otp_secret:
        user.generate_otp_secret()
        db.session.commit()

    # 2) Provisioning-URI nach RFC6238
    uri = pyotp.TOTP(user.otp_secret).provisioning_uri(
        name=user.email,
        issuer_name="DocNotary"
    )

    # 3) QR-Code für die URI erzeugen
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")

    # 4) In-Memory-PNG und Base64 enkodieren
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    qr_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    return jsonify({
        "otp_secret": user.otp_secret,
        "provisioning_uri": uri,
        "qr_code_png_base64": qr_b64
    }), 200
