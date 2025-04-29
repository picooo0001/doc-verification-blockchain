from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db

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