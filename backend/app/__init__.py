from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from .config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(test_config: dict = None):
    """
    Erzeugt und konfiguriert die Flask-Anwendung.

    Lädt die Basis-Konfiguration, wendet optional Test-Konfigurationen an,
    richtet CORS nur für http://localhost:5173 ein und aktiviert Credentials-Support.
    Initialisiert alle Extensions (Datenbank, Migration, Bcrypt, Login-Manager),
    definiert das Verhalten für nicht autorisierte Zugriffe und lädt Benutzer-Objekte.
    Registriert anschließend die Notary- und Auth-Blueprints unter dem Prefix /api.

    :param test_config: Optionales Dictionary mit Konfigurationsüberschreibungen (z.B. für Tests)
    :type test_config: dict, optional
    :return: Flask-Anwendung, fertig konfiguriert und registriert
    :rtype: Flask
    """
    app = Flask(__name__)
    CORS(app, 
         supports_credentials=True,
         origins=["http://localhost:5173"])
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    CORS(app, resources={r"/*": {"origins": "http://localhost:5173", "supports_credentials": True}})

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.unauthorized_handler
    def return_401_for_api():
        return jsonify({"error": "Unauthorized"}), 401

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

    from .routes import bp as notary_bp
    from .auth import bp as auth_bp

    app.register_blueprint(notary_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api")

    return app
