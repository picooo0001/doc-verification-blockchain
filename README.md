# Dezentrale Notarisierung von Dokumenten

## 🚀 Projektziel
Blockchain-basierte Verifikation und Notarisierung von Dokumenten.

## 📁 Ordnerstruktur
- `contracts/`: Smart Contracts (Solidity)
- `backend/`: API-Server (Python/Flask oder Node.js)
- `frontend/`: Web-UI (HTML/CSS/JS mit MetaMask)
- `docs/`: Spezifikationen & Diagramme
- `tests/`: Unit- und Integrationstests

## 🔧 Setup (lokal)
1. `cd contracts` → `npm init -y` → Hardhat/Truffle installieren  
2. `cd frontend` → `npm init -y` → Web3-Libs installieren  
3. `cd backend` → Python-Virtualenv anlegen → `pip install -r requirements.txt`  
4. Ganache starten: `ganache-cli`  
5. Smart Contract deployen (Hardhat/Truffle)  
6. Frontend/Backend starten

## ⚙️ Git-Workflow
- Neue Features: `git checkout -b feature/<kurzbeschreibung>`
- Änderungen committen & pushen → Pull Request gegen `main`

## 📄 Lizenz
MIT
