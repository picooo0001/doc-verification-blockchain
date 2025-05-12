# Setup-Anleitung für lokales Projekt

Diese Anleitung beschreibt alle nötigen Schritte, um das Projekt **lokal** mit Smart Contracts, Backend und Frontend zu starten. Vorausgesetzt wird, dass das Repository bereits geklont wurde.

---

## Voraussetzungen

* **Node.js & npm:** Installation von [Node.js](https://nodejs.org/) (Version 14+ empfohlen).
* **Python 3:** Installation von Python (3.7 oder neuer) und `pip`.
* **Git:** Zum Klonen und Aktualisieren des Repositories.
* **Ethereum-Testnetzwerk:** Entweder **Hardhat** oder **Ganache CLI** für ein lokales Blockchain-Netzwerk.

---

## 1. Smart Contracts deployen

1. **In das Contracts-Verzeichnis wechseln:**

   ```bash
   cd contracts
   ```
2. **Dependencies installieren:**

   ```bash
   npm install
   ```
3. **Hardhat-Node starten:** (lokales Ethereum-Netzwerk)

   ```bash
   npx hardhat node
   ```

   Lasse dieses Terminal geöffnet – der Node lauscht nun auf `localhost:8545`.
4. **Contracts deployen:** In einem neuen Terminal

   ```bash
   npx hardhat run scripts/deploy.js --network localhost
   ```

   Nach dem Deploy findest du die Adressen (2x per Default) in der Console. Notiere dir diese & füge sie händisch in die Datenbank ein.
   Die Chain Adressen sind unter `../contracts/deployed-contracts.json`einsehbar.

---

## 2. Backend aufsetzen

1. **In das Backend-Verzeichnis wechseln:**

   ```bash
   cd ../backend
   ```
2. **Virtuelle Umgebung anlegen (optional):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate      
   #Windows: venv\Scripts\activate
   ```
3. **Abhängigkeiten installieren:**

   ```bash
   pip install -r requirements.txt
   ```
4. **Konfiguration anpassen:**

   * Öffne im Backend-Verzeichnis die Datei `config.py`.
   * `config.py` lädt über `python-dotenv` Umgebungsvariablen (sofern vorhanden) und definiert:

     * `RPC_URL`: Umgebungsvariable `RPC_URL`, Default: `"http://127.0.0.1:8545"`
     * `CONTRACT_ABI_PATH`: Umgebungsvariable `CONTRACT_ABI_PATH`, Default: `"../contracts/artifacts/contracts/Notary.sol/Notary.json"`
     * `SECRET_KEY`: Umgebungsvariable `SECRET_KEY`, Default: `"setz-dir-ein-geheimes-key"`
     * `SQLALCHEMY_DATABASE_URI`: Umgebungsvariable `SQLALCHEMY_DATABASE_URI`, Default: `"postgresql://"
        "postgres.fffabyazqvvwdaimdcmk:"
        "qE9b%5EM%3B42%3BLn"
        "@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"`
        (Datenbak URL - Docker wird nicht mehr benötigt)
5. **Datenbank-Initalisierung (falls nötig):**
   ```bash
   flask db upgrade
   ```
6. **Backend starten:**

   ```bash
   python run.py
   ```

   Das Backend läuft jetzt unter `http://localhost:5001`.

---

## 3. Frontend starten

1. **In das Frontend-Verzeichnis wechseln:**

   ```bash
   cd ../frontend
   ```
2. **Dependencies installieren:**

   ```bash
   npm install
   ```
3. **Konfiguration anpassen:**

   * Setze in der Frontend-Initialisierung (z. B. direkt in main.js oder einer entsprechenden Datei) die Basis-URL für Axios:
   ```javascript
   axios.defaults.baseURL = 'http://localhost:5001'
   ```
4. **Frontend starten:**

   ```bash
   npm run dev
   ```

   Standardmäßig unter `http://localhost:5173` erreichbar.

---

## 4. Erste Tests

* **Test-Nutzer anlegen:** Lege in der Datenbank einen Benutzer an (via Datenbank): E-Mail, Passwort, Organisation und (optional) `wallet_address`.
* **Login prüfen:** Melde dich im Browser unter `http://localhost:8080` an. Für Wallet-Login MetaMask auf lokales Netzwerk stellen und Nonce signieren.
* **2FA einrichten:** Über Profil → 2FA-Setup secret und QR-Code erzeugen.
* **Dokument notarize/verify:** Upload-Seite im Frontend nutzen – PDF hochladen, anschließend Verifikation testen.
* **Dokumentenliste & Statistiken:** Überprüfe `/api/documents` und `/api/stats` im Browser.

---

