# tests/test_login_endpoint.py

import pytest
import pyotp
from app import create_app, db
from app.models import Organization, User

@pytest.fixture
def client():
    # 1) App mit Test-Datenbank (SQLite In-Memory) erzeugen
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
    app = create_app(test_config)

    # 2) Tabellen erzeugen und Daten anlegen
    with app.app_context():
        db.create_all()
        org = Organization(name="TestOrg")
        user = User(email="alice@test.org", organization=org)
        user.set_password("Secret123")
        user.generate_otp_secret()
        db.session.add_all([org, user])
        db.session.commit()

    return app.test_client()

def test_login_success(client):
    # gleichen Flow wie zuvor: OTP holen und login testen
    from app.models import User
    with client.application.app_context():
        user = User.query.filter_by(email="alice@test.org").first()
        otp = pyotp.TOTP(user.otp_secret).now()

    res = client.post("/login", data={
        "email": "alice@test.org",
        "password": "Secret123",
        "otp": otp
    })
    assert res.status_code == 200
    assert res.get_json() == {"message": "Login erfolgreich"}

def test_login_failure(client):
    res = client.post("/login", data={
        "email": "alice@test.org",
        "password": "WrongPassword",
        "otp": "000000"
    })
    assert res.status_code == 401
    assert "error" in res.get_json()
