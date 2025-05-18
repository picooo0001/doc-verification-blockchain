# Schnellstart mit Docker Compose

**Ziel:** Nach dem Klonen des Repositories sofort Frontend und Backend starten.

## Voraussetzungen

* Docker & Docker Compose installiert
* Git installiert

## 1. Repo klonen

```bash
git clone https://github.com/dein-org/dein-repo.git
cd dein-repo
```

## 2. `.env` anlegen

Kopiere die Beispiel-Datei und fülle deine Secrets ein:

```bash
cp .env.example .env
RPC_URL=https://sepolia.infura.io/v3/<API Key>
ETHERSCAN_API_KEY=<API Key>
DEPLOYER_KEY=XXX
CONTRACT_ABI_PATH=../contracts/artifacts/contracts/Notary.sol/Notary.json
SECRET_KEY=XXX
SQLALCHEMY_DATABASE_URI=XXX

```

## 3. Container bauen & starten

```bash
docker-compose up --build -d
```

## 4. Zugriff

* **Frontend**: [http://localhost](http://localhost)
* **API**:     [http://localhost/api](http://localhost/api)

**Fertig!** Änderungen an Code werden beim Neustart (`docker-compose up --build`) automatisch übernommen.
