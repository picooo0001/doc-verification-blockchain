# Projektstruktur

Dies ist die Ordner- und Dateistruktur des Backend-Services. Die Dokumentation liegt in `api-doc.md` und beinhaltet alle Endpoints der Anwendung.

```
backend/
├── app/
│   ├── __init__.py        # Initialisiert das Flask-App-Package
│   ├── auth.py            # Authentifizierungs-Blueprint (Login/Logout/2FA)
│   ├── config.py          # Konfigurationsklasse (Flask-Settings, Umgebungsvariablen)
│   ├── models.py          # SQLAlchemy-Modelle (User, Organization, Document)
│   ├── routes.py          # Notary-Blueprint (Dokumenten-API: notarize, verify, stats...)
│   └── web3utils.py       # Helper-Funktionen für Web3 (Contract-Ladefunktion etc.)
├── tests/                 # Unit- und Integrationstests (teilweise veraltet)
├── venv/                  # Virtuelle Umgebung (nicht im Repo)
├── requirements.txt       # Projekt-Abhängigkeiten (pip install -r requirements.txt)  
└── run.py                 # Start-Skript für den Flask-Server
```

## Kurze Beschreibung der Ordner und Dateien

* **app/**

  * `__init__.py`

    * Initialisiert die Flask-Anwendung über `create_app()` (CORS, DB, Migrations, Blueprints).
  * `config.py`

    * Projektkonfiguration (Datenbank-URL, Secret Key, CONTRACT_ABI_PATH).
  * `models.py`

    * Definiert die Datenbankmodelle `User`, `Organization`, `Document` mit ihren Attributen und Methoden.
  * `auth.py`

    * Authentifizierungs-Blueprint: Endpoints für Login (E-Mail/Passwort, Wallet-Signatur), Logout, 2FA-Setup und Profil.
  * `routes.py`

    * Notary-Blueprint: Endpoints für Dokumenten-Hashes, Commit, Verifikation, Listing, Download, Stats, Admin Routen
  * `web3utils.py`

    * Hilfsfunktionen rund um Web3: Laden des Contracts, Verbindungsaufbau zu Etherum, Konfiguration (ABI-Pfad, RPC_URL)

* **tests/**

  * Beinhaltet Tests für die verschiedenen Endpoints und Models (veraltet).

* **venv/**

  * Virtuelle Python-Umgebung (lokal erstellt; nicht im Git-Repo).

* **requirements.txt**

  * Listet alle Python-Abhängigkeiten mit exakten Versionsangaben. Installiere via:

    ```bash
    pip install -r requirements.txt
    ```

* **run.py**

  * Skript zum Starten der Flask-Anwendung:

    ```bash
    python run.py
    ```

---

> **Hinweis:** Die API-Endpunkte sind in `api-doc.md` dokumentiert.
