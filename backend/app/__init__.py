from flask import Flask
from .config import Config
from .routes import bp as notary_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Blueprint registrieren
    app.register_blueprint(notary_bp, url_prefix="/api")

    return app
