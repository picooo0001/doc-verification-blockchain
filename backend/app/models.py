from . import db, bcrypt
from flask_login import UserMixin
import pyotp

class Organization(db.Model):
    """
    Repräsentiert eine Organisation, die Dokumente notariell registrieren kann.

    Attributes:
        id (int): Primärschlüssel der Organisation.
        name (str): Eindeutiger Name der Organisation.
        deploy_block (int | None): Start-Blocknummer, ab der Events gelesen werden.
        contract_address (str | None): Ethereum-Contract-Adresse der Notary-Instanz.
        users (List[User]): Liste der Benutzer, die zu dieser Organisation gehören.
    """
    __tablename__ = "organizations"
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(128), unique=True, nullable=False)
    deploy_block     = db.Column(db.Integer,      nullable=True)
    contract_address = db.Column(db.String(42), unique=True, nullable=True)
    users         = db.relationship("User", backref="organization", lazy=True)

class User(db.Model, UserMixin):
    """
    Repräsentiert einen Benutzer innerhalb einer Organisation.

    Unterstützt sowohl E-Mail/Passwort-Login als auch Ethereum-Wallet-Login.

    Attributes:
        id (int): Primärschlüssel des Benutzers.
        wallet_address (str | None): Ethereum-Adresse für Wallet-Login.
        login_nonce (str | None): Einmalige Nonce für Wallet-Login-Signaturen.
        email (str): E-Mail-Adresse für Passwort-Login.
        password_hash (str): Gehashter Passwort-String.
        otp_secret (str | None): Secret für Zwei-Faktor-Authentifizierung (TOTP).
        is_owner (bool): Gibt an, ob der Benutzer Owner-Rechte hat.
        organization_id (int): Fremdschlüssel zur zugehörigen Organisation.
    """
    __tablename__ = "users"
    id             = db.Column(db.Integer, primary_key=True)
    wallet_address = db.Column(db.String(42), unique=True, nullable=True)
    login_nonce    = db.Column(db.String(32), nullable=True)
    email          = db.Column(db.String(128), unique=True, nullable=False)
    password_hash  = db.Column(db.String(128), nullable=False)
    otp_secret     = db.Column(db.String(32), nullable=True)
    is_owner       = db.Column(db.Boolean, default=False, nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode()

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def generate_otp_secret(self):
        """
        Generiert ein neues OTP-Secret für TOTP und speichert es im Benutzerobjekt.
        """
        self.otp_secret = pyotp.random_base32()

    def verify_otp(self, token):
        """
        Verifiziert einen TOTP-Token gegen das gespeicherte OTP-Secret.

        Args:
            token (str): Der vom Benutzer generierte TOTP-Code.

        Returns:
            bool: True, wenn der Token gültig ist, sonst False.
        """
        if not self.otp_secret or not token:
            return False
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(token, valid_window=5)

class Document(db.Model):
    """
    Repräsentiert ein notariell registriertes Dokument innerhalb einer Organisation.

    Attributes:
        id (int): Primärschlüssel des Dokument-Eintrags.
        document_id (str): Hexadezimaler Keccak-256-Hash der Dokumenten-ID.
        org_id (int): Fremdschlüssel zur Organisation.
        file_data (bytes): Binärdaten der hochgeladenen Datei.
        mime_type (str): MIME-Typ der Datei.
        tx_hash (str): Transaktions-Hash der Blockchain-Notarisierung.
    """
    __tablename__ = 'documents'
    id          = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.String, nullable=False)
    org_id      = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    file_data   = db.Column(db.LargeBinary, nullable=False)
    mime_type   = db.Column(db.String, nullable=False)
    tx_hash     = db.Column(db.String(66), nullable=False)

    __table_args__ = (
        db.Index('ix_documents_org_doc', 'org_id', 'document_id'),
    )