# Dezentrale Notarisierung von Dokumenten

## 🚀 Projektziel
Blockchain-basierte Verifikation und Notarisierung von Dokumenten.

## 📁 Ordnerstruktur
- `contracts/`: Smart Contracts (Solidity)
- `backend/`: API-Server (Python/Flask)
- `frontend/`: Web-UI (Vue.js mit MetaMask)
- `docs/`: Spezifikationen & Diagramme
- `tests/`: Unit- und Integrationstests

## 🔧 Setup (lokal)
1. `cd contracts` → `npm init -y` → Hardhat/Truffle installieren  
2. `cd frontend` → `npm init -y` → Web3-Libs installieren  
3. `cd backend` → Python-Virtualenv anlegen → `pip install -r requirements.txt`  
4. Ganache starten: `ganache-cli` //evtl. raus  
5. Smart Contract deployen (Hardhat/Truffle) im lokalen Netzwerk (Test only): `cd contracts` → `npx hardhat node` →  `npx hardhat run scripts/deploy.js --network localhost`→  `contracts/deployed-address.txt` (ausgegebene Adresse ablegen und ablegen)
6. Frontend/Backend starten

## ⚙️ Git-Workflow
- Änderungen committen & pushen → Pull Request gegen `main`
- File adden `git add <filename>`
- Commit erstellen `git commit -m "Nachricht"`
- Commit pushen `git push origin main`

- Status abrufen `git status`
- Lokale Änderungen sichern, die noch nicht commited sind `git stash`
- Updated Repo lokal ziehen `git pull oirigin main`
- Gestashete Änderungen wieder holen `git stash pop`

## 📄 Lizenz
MIT
