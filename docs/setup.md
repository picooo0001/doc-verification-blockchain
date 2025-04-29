# Setup-Anleitung für das Backend

Diese Anleitung zeigt, wie du das Backend mit Docker (PostgreSQL), Flask-Migrationen und Testdaten startklar machst.

---

## Voraussetzungen

- **Docker** & **Docker Compose** installiert (bzw. `docker compose` Befehl verfügbar)
- **Python 3.8+** und **Virtual Environment** (venv)
- **Node.js** & **Hardhat** (für Smart-Contract-Tests)

---

## 1. PostgreSQL starten mit Docker Compose

Lege eine Datei `docker-compose.yml` im Projekt-Root an:

```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypass
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
volumes:
  pgdata:
```

Dann im Terminal im Projekt-Root:

```bash
docker compose up -d
```

- **Port 5432** wird exposed.
- DB-Daten werden persistiert im Docker-Volume `pgdata`.

---

## 2. Virtualenv & Abhängigkeiten installieren

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### `requirements.txt` sollte enthalten:
```
Flask
Flask-SQLAlchemy
Flask-Migrate
Flask-Bcrypt
Flask-Login
python-dotenv
psycopg2-binary
pyotp
pytest
python-dotenv
web3
```

---

## 3. Umgebungsvariablen setzen

Nehme die `app/config.py` Datei:
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Lokaler Hardhat RPC
    RPC_URL = os.getenv("RPC_URL", "http://127.0.0.1:8545")
    # Pfad zur Datei mit der deployed contract address
    DEPLOYED_ADDRESS_FILE = os.getenv(
        "DEPLOYED_ADDRESS_FILE",
        "../contracts/contracts/deployed-address.txt"
    )
    # Contract ABI – wird später von web3utils geladen
    CONTRACT_ABI_PATH = os.getenv(
        "CONTRACT_ABI_PATH",
        "../contracts/artifacts/contracts/Notary.sol/Notary.json"
    )
    # Datenbank URL
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://myuser:mypass@localhost:5432/mydb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "setz-dir-ein-geheimes-key")


```
---

## 4. App starten und Migrations-Commands

### a) App-Umgebung konfigurieren

```bash
export FLASK_APP=run.py
export FLASK_ENV=development
```

### b) Migration initialisieren (erstmalig)

```bash
flask db init        # erzeugt migrations/
```

### c) Migrationsskript erstellen

```bash
flask db migrate -m "Initial schema: Organization + User"
```

### d) Migration anwenden

```bash
flask db upgrade
```

Damit sind die Tabellen `organizations` und `users` in Postgres angelegt.

---

## 5. Testdaten anlegen (Flask Shell)

```bash
flask shell
```

```python
>>> from app import db
>>> from app.models import Organization, User
>>> org = Organization(name='TestOrg')
>>> user = User(email='alice@test.org', organization=org)
>>> user.set_password('Secret123')
>>> user.generate_otp_secret()
>>> db.session.add_all([org, user])
>>> db.session.commit()
>>> print('OTP-Secret:', user.otp_secret)
>>> exit()
```
---

## 6. Backend starten

```bash
python run.py
```

Das Backend läuft auf **http://localhost:5001** und verbindet sich zur Postgres-DB.

---

## 7. Lokaled Hardhat Testnetz aufsetzen

Wie gehabt Hardhat Testnetz mit folgendem Command aufsetzen:

```bash
npx hardhat node
```

Ist das Testnetz online, den Contract deployen (in einem neuen Terminal):

```bash
npx hardhat run scripts/deploy.js --network localhost
```
---

## 7. Tests ausführen

- **Unit-Tests** (SQLite-In-Memory):
  ```bash
  pytest -q
  ```
---

## 8. Endpoints testen

- **Notarize**:  
  `curl -F "file=@/path/to/doc.pdf" -F "documentId=test1" http://localhost:5001/api/notarize`

- **Verify**:  
  `curl -F "file=@/path/to/doc.pdf" http://localhost:5001/api/verify`

- **Login**:  
  ```bash
  OTP=$(python3 - <<EOF
  import pyotp
  print(pyotp.TOTP("$SECRET").now())
  EOF
  )
  curl -F "email=alice@test.org" -F "password=Secret123" -F "otp=$OTP" http://localhost:5001/login
  ```

- **Logout**:  
  `curl -X POST http://localhost:5001/logout`

---

