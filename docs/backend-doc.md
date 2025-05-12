# Backend-Dokumentation

Das Backend befindet sich im Ordner `backend/` und stellt die API-Server-Logik für Authentifizierung, Dokumenten-Notarisierung und Datenbank-Interaktion bereit.

## Ordnerstruktur

```plaintext
backend/
├── app/
│   ├── __init__.py       # Flask-App-Konfiguration und Erstellung
│   ├── auth.py           # Authentifizierungs-Routen (E‑Mail/Passwort, OTP, Wallet-Login)
│   ├── config.py         # Konfigurationsklasse (RPC_URL, CONTRACT_ABI_PATH, DB-URL, SECRET_KEY)
│   ├── models.py         # Datenbank-Modelle (User, Organization, Document)
│   ├── routes.py         # Feature-Routen (notarize, verify, stats, documents, download)
│   └── web3utils.py      # Web3-Hilfsfunktionen (Contract-Instanzen, Adressen)
├── migrations/           # Alembic-Migrationen für das DB-Schema
├── tests/                # Unit- und Integrationstests (teilweise veraltet)
├── venv/                 # Virtuelle Umgebung (nicht im Repo)
├── requirements.txt      # Python-Abhängigkeiten
└── run.py                # Skript zum Starten des Flask-Servers
```

## Datei-Beschreibungen

### `app/__init__.py`

* Initialisiert und konfiguriert die Flask-App
* Registriert Extensions (SQLAlchemy, Flask-Login) und Blueprints

### `app/auth.py`

Definiert alle Authentifizierungs-Endpoints:

* **POST** `/login` (E‑Mail/Passwort + OTP)
* **GET** `/login/nonce` & **POST** `/login/wallet` (Wallet-basiertes Login)
* **POST** `/logout`
* **GET** `/setup-2fa` & **POST** `/user/2fa` (2FA-Setup und Aktivierung/Deaktivierung)
* **GET** `/user/profile` & **GET** `/org/allowed-addresses`

### `app/config.py`

Konfigurationsklasse `Config` mit folgenden Parametern (via `python-dotenv` und `os.getenv`):

* `RPC_URL` (Hardhat/Ganache RPC, Default: `http://127.0.0.1:8545`)
* `CONTRACT_ABI_PATH` (Pfad zum Notary-ABI, Default: `../contracts/artifacts/contracts/Notary.sol/Notary.json`)
* `SQLALCHEMY_DATABASE_URI` (Datenbank-URL)
* `SECRET_KEY` (Session-Secret)

### `app/models.py`

Datenbank-Modelle mit SQLAlchemy:

* `User` (E‑Mail, Passwort-Hash, OTP-Secret, Wallet-Adresse, Nonce)
* `Organization` (Name, Chain- und Contract-Adressen)
* `Document` (Dokumenten-ID, Org-ID, BLOB, MIME-Typ)

### `app/routes.py`

Implementiert die Kern-Funktionalität:

* **POST** `/notarize`
* **POST** `/verify`
* **GET** `/stats`
* **GET** `/documents`
* **GET** `/documents/<idHash>/download`

### `app/web3utils.py`

Hilfsfunktionen für Web3-Interaktionen:

* Aufbau von `w3` (Web3.py Instanz)
* Laden des Notary-Contracts für Organisationen
* Ermittlung von Adressen (User, Organization)

### `migrations/`

Enthält Alembic-Migrationsskripte zur Versionierung und Aktualisierung des Datenbank-Schemas.

### `tests/`

Enthält Tests für Login-, Notarisierungs- und Verifikations-Endpoints. Einige Tests sind nicht mehr aktuell und sollten überarbeitet werden.
**outdated**

### `venv/`

Virtuelle Python-Umgebung – nicht im Repository committen.

### `requirements.txt`

Liste aller benötigten Python-Pakete (Flask, Web3.py, SQLAlchemy, etc.).

### `run.py`

Einfaches Skript zum Starten des Flask-Backends:

```bash
python run.py
```
