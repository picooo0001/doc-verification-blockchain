# Dezentrale Notarisierung von Dokumenten

## 🚀 Projektziel

- Verifikation und Notarisierung von Dokumenten in einer dezentralen Blockchain (Sepolia).
- Einfacher Login via Wallet oder Username/2FA.
- Dokumentenupload und -verifikation direkt im Browser mit MetaMask.

## 📁 Ordnerstruktur

* `contracts/`
  Enthält den Solidity-Smart-Contracts und Unit-Tests, sowie die Hardhat Config für die Festlegung des Netzwerks.

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
  * Admin Panel für das User und Contract Management

* `docs/`
  Projekt-Dokumentation und Setup-Anleitungen:

  * Ausführliche API-Dokumentation (`api-doc.md`)
  * Setup-Anleitung für Backend, Contracts und Frontend (`setup.md`)
  * Ausführlichere Dokumentation zu den verschiedenen Ordnern

* `docker-compose.yml`
  Richtet via Docker gesamte Applikation ein.

* `README.md`
  Überblick und schnelle Einstiegshilfe:

  * Projektziel
  * Kurze Erläuterung der Ordnerstruktur
  * Installation und erste Schritte
  * Git-Workflow

* `.gitignore`
  Listet Dateien und Ordner, die nicht versioniert werden sollen (z. B. `node_modules/`, `venv/`, `.env`).

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

Aktuelle Branch: `fetaure/sepolia-integration`

## 📄 Lizenz
MIT
