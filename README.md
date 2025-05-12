# Dezentrale Notarisierung von Dokumenten

## 🚀 Projektziel
Blockchain-basierte Verifikation und Notarisierung von Dokumenten.

## 📁 Ordnerstruktur

* `contracts/`
  Enthält die Solidity-Smart-Contracts, Deployment-Skripte und Unit-Tests. Hier definiert ihr den `Notary.sol`-Contract, testet ihn mit Hardhat und deployt ihn lokal.

* `backend/`
  API-Server auf Basis von Python und Flask. In diesem Ordner findet ihr:

  * Flask-App-Konfiguration (`app/__init__.py`, `config.py`)
  * Authentifizierung, 2FA, Wallet-Login (`auth.py`)
  * Datenbank-Modelle (`models.py`)
  * Dokumenten-Notarisierungs-Routen (`routes.py`)
  * Web3-Hilfsfunktionen (`web3utils.py`)

* `frontend/`
  Vue.js-Weboberfläche für Nutzerinteraktion. Hier werden:

  * Benutzer-Login/2FA-Flow abgebildet
  * Dokumenten-Upload und Verifikation über MetaMask eingebunden
  * Statistiken und Dokumentenlisten angezeigt

* `docs/`
  Projekt-Dokumentation und Setup-Anleitungen:

  * Ausführliche API-Dokumentation (`api-doc.md`)
  * Setup-Anleitung für Backend, Contracts und Frontend (`setup.md`)
  * Ausführlichere Dokumentation zu den verschiedenen Ordnern

* `docker-compose.yml`
  Richtet via Docker lediglich eine lokale PostgreSQL-Datenbank auf `localhost:5432` ein; diese wird aktuell nicht mehr verwendet, da die Datenbank nun extern gehostet wird.

* `README.md`
  Überblick und schnelle Einstiegshilfe:

  * Projektziel und Motivation
  * Kurze Erläuterung der Ordnerstruktur (siehe oben)
  * Installation und erste Schritte
  * Verweise auf detaillierte Dokumente in `docs/`

* `.gitignore`
  Listet Dateien und Ordner, die nicht versioniert werden sollen (z. B. `node_modules/`, `venv/`, lokale Konfigs).

## 🔧 Setup (lokal)
- siehe `docs/setup.md`

## ⚙️ Git-Workflow
- Änderungen committen & pushen → Pull Request gegen `main`
- File adden `git add <filename>`
- Commit erstellen `git commit -m "Nachricht"`
- Commit pushen `git push`
- Status abrufen `git status`
- Lokale Änderungen sichern, die noch nicht commited sind `git stash`
- Updated Repo lokal ziehen `git pull oirigin main`
- Gestashete Änderungen wieder holen `git stash pop`

**Checken ob die Branch die Richtige ist!**

## 📄 Lizenz
MIT
