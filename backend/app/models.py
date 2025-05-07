from . import db, bcrypt
from flask_login import UserMixin
import pyotp

class Organization(db.Model):
    __tablename__ = "organizations"
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(128), unique=True, nullable=False)
    chain_address = db.Column(db.String(42), unique=True, nullable=False)
    contract_address = db.Column(db.String(42), unique=True, nullable=True)
    users         = db.relationship("User", backref="organization", lazy=True)

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id             = db.Column(db.Integer, primary_key=True)

    # MetaMask Login
    wallet_address = db.Column(db.String(42), unique=True, nullable=True)
    login_nonce    = db.Column(db.String(32), nullable=True)

    # Alter Login Prozess
    email          = db.Column(db.String(128), unique=True, nullable=False)
    password_hash  = db.Column(db.String(128), nullable=False)
    otp_secret     = db.Column(db.String(32), nullable=True)

    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False)

class Document(db.Model):
    __tablename__ = 'documents'
    id          = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.String, nullable=False)
    org_id      = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    file_data   = db.Column(db.LargeBinary, nullable=False)
    mime_type   = db.Column(db.String, nullable=False)
    __table_args__ = (
        db.Index('ix_documents_org_doc', 'org_id', 'document_id'),
    )

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode()

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def generate_otp_secret(self):
        self.otp_secret = pyotp.random_base32()

    def verify_otp(self, token):
        if not self.otp_secret or not token:
            return False
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(token, valid_window=5)
