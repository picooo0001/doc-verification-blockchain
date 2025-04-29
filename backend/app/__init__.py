# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from .config import Config

# Extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(test_config: dict = None):
    # 1) Basis-Config laden
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 2) Test-Config (falls vorhanden) direkt überschreiben
    if test_config:
        app.config.update(test_config)

    # Extensions initialisieren
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Blueprints importieren und registrieren (deferred Imports verhindern Zirkuläre Abhängigkeiten)
    from .routes import bp as notary_bp
    from .auth import bp as auth_bp

    app.register_blueprint(notary_bp, url_prefix="/api")
    app.register_blueprint(auth_bp)

    return app