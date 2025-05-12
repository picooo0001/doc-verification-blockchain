# API-Dokumentation

**Base URL:**

* Auth-Routes: `http://localhost:5001`
* Notary-Routes: `http://localhost:5001/api`

---

## Authentifizierung & Nutzer

### POST `/login`

Authentifiziert einen Benutzer per E-Mail/Passwort (Form-Data oder JSON).

* **URL:** `/login`
* **Methode:** `POST`
* **Authentifizierung:** Keine (öffnet Session-Cookie)

**Request Body (Form-Data oder JSON):**

| Feld       | Typ    | Beschreibung                                 |
| ---------- | ------ | -------------------------------------------- |
| `email`    | String | E-Mail-Adresse des Benutzers                 |
| `password` | String | Klartext-Passwort                            |
| `otp`      | String | Einmal-Passwort (6-stellig), falls 2FA aktiv |

JSON-Beispiel:

```json
{
  "email": "alice@test.org",
  "password": "Secret123",
  "otp": "123456"   // optional, nur wenn 2FA eingerichtet
}
```

**Erfolgs-Response (200 OK):**

```json
{ "message": "Login erfolgreich" }
```

**Fehler-Responses:**

* **401 Unauthorized** – bei falscher E-Mail/Passwort oder fehlendem/ungültigem OTP:

```json
{ "error": "Ungültige E-Mail oder Passwort" }
{ "error": "2FA erforderlich" }
{ "error": "Ungültiges OTP" }
```

---

### GET `/login/nonce`

Ermittelt einen Zufalls-Nonce für das Wallet-Login.

* **URL:** `/login/nonce?address={walletAddress}`
* **Methode:** `GET`
* **Parameter:** `address` (in Query-String, Ethereum-Adresse)
* **Authentifizierung:** Keine

**Erfolgs-Response (200 OK):**

```json
{ "nonce": "d4f2a9b1c3e5..." }
```

**Fehler-Responses:**

* **400 Bad Request** – ungültige oder falsche Adressformat:

```json
{ "error": "Ungültige Adresse" }
{ "error": "Ungültiges Adress-Format" }
```

* **404 Not Found** – Adresse nicht in der Datenbank (nicht registriert):

```json
{ "error": "Adresse nicht registriert" }
```

---

### POST `/login/wallet`

Loggt den Benutzer über Wallet-Signatur ein.

* **URL:** `/login/wallet`
* **Methode:** `POST`
* **Authentifizierung:** Keine

**Request Body (JSON):**

```json
{
  "address": "0xAbc123...def",   // Ethereum-Adresse des Nutzers
  "signature": "0x5f3b..."       // Signatur des Nonce-Textes
}
```

**Erfolgs-Response (200 OK):**

```json
{ "message": "Login erfolgreich" }
```

**Fehler-Responses:**

* **400 Bad Request** – ungültige Adresse oder Format:

```json
{ "error": "Ungültige Adresse" }
{ "error": "Ungültiges Adress-Format" }
```

* **401 Unauthorized** – fehlender Nonce oder Signatur ungültig bzw. Adress-Mismatch:

```json
{ "error": "Nonce nicht gefunden" }
{ "error": "Signatur ungültig" }
{ "error": "Address mismatch" }
```

---

### POST `/logout`

Loggt den aktuell eingeloggten Benutzer aus.

* **URL:** `/logout`
* **Methode:** `POST`
* **Authentifizierung:** Cookie/Session (Flask-Login)

**Erfolgs-Response (200 OK):**

```json
{ "message": "Logout erfolgreich" }
```

---

### GET `/setup-2fa`

Generiert (falls noch nicht vorhanden) ein neues TOTP-Secret für den eingeloggten Benutzer und liefert Secret, Provisioning-URI & QR-Code.

* **URL:** `/setup-2fa`
* **Methode:** `GET`
* **Authentifizierung:** Cookie/Session (benötigt Anmeldung)

**Erfolgs-Response (200 OK):**

```json
{
  "otp_secret": "JBSWY3DPEHPK3PXP",
  "provisioning_uri": "otpauth://totp/DocNotary:alice%40test.org?secret=JBSWY3DPEHPK3PXP&issuer=DocNotary",
  "qr_code_png_base64": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```

**Fehler-Response (401 Unauthorized):**

```json
{ "error": "Authentication required" }
```

---

### POST `/user/2fa`

Aktiviert oder deaktiviert 2-Faktor-Authentifizierung für den eingeloggten Benutzer.

* **URL:** `/user/2fa`
* **Methode:** `POST`
* **Authentifizierung:** Cookie/Session (benötigt Anmeldung)

**Request Body (JSON):**

```json
{ "enable": true }   // true: 2FA aktivieren, false: 2FA deaktivieren
}
```

**Erfolgs-Responses (200 OK):**

* Bei Aktivierung (`enable=true`):

```json
{
  "message": "2FA aktiviert",
  "otp_secret": "JBSWY3DPEHPK3PXP",
  "provisioning_uri": "otpauth://totp/DocNotary:alice%40test.org?secret=JBSWY3DPEHPK3PXP&issuer=DocNotary",
  "qr_code_png_base64": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```

* Bei Deaktivierung (`enable=false`):

```json
{ "message": "2FA deaktiviert" }
```

---

### GET `/user/profile`

Gibt Profildaten des aktuell eingeloggten Nutzers zurück.

* **URL:** `/user/profile`
* **Methode:** `GET`
* **Authentifizierung:** Cookie/Session (benötigt Anmeldung)

**Erfolgs-Response (200 OK):**

```json
{
  "email": "alice@test.org",
  "organization": "TestOrg",
  "2faEnabled": true,
  "walletAddress": "0xAbc123...def",
  "hasWallet": true
}
```

---

### GET `/org/allowed-addresses`

Gibt alle Wallet-Adressen der Nutzer der eigenen Organisation zurück.

* **URL:** `/org/allowed-addresses`
* **Methode:** `GET`
* **Authentifizierung:** Cookie/Session (benötigt Anmeldung)

**Erfolgs-Response (200 OK):**

```json
{
  "allowedAddresses": [
    "0xAbc123...def",
    "0x456efc...789",
    "0x111222...aaa"
  ]
}
```

---

## Notarisierung & Verifikation

*Alle folgenden Routen erfordern Authentifizierung (Cookie/Session via Flask-Login).*

### POST `/api/notarize`

Notarisiert ein Dokument in der Blockchain.

* **URL:** `/api/notarize`
* **Methode:** `POST`
* **Authentifizierung:** Cookie/Session
* **Form-Data:**

  | Feld         | Typ    | Beschreibung                                                 |
  | ------------ | ------ | ------------------------------------------------------------ |
  | `file`       | File   | Zu notarisierende PDF- oder Binärdatei                       |
  | `documentId` | String | Eindeutige ID, unter der das Dokument hinterlegt werden soll |

**Erfolgs-Response (200 OK):**

```json
{
  "txHash": "0x6988abc123...fed",
  "blockNumber": 42
}
```

**Fehler-Responses (400 Bad Request):**

```json
{ "error": "No file provided" }
{ "error": "No documentId provided" }
{ "error": "Dokument darf nicht geändert werden" }
{ "error": "Schon notariell hinterlegt" }
```

---

### POST `/api/verify`

Prüft, ob ein Dokument bereits notariell hinterliegt.

* **URL:** `/api/verify`
* **Methode:** `POST`
* **Authentifizierung:** Cookie/Session
* **Form-Data:**

  | Feld   | Typ  | Beschreibung                      |
  | ------ | ---- | --------------------------------- |
  | `file` | File | Zu verifizierendes PDF/Binärdatei |

**Erfolgs-Response (200 OK):** – Dokument ist notariell hinterlegt:

```json
{ "verified": true, "timestamp": 1745919683 }
```

**Fehler-Responses:**

* **400 Bad Request** – kein File gesendet:

```json
{ "error": "No file provided" }
```

* **404 Not Found** – Dokument **nicht** hinterlegt (verified=false, Status 404):

```json
{ "verified": false }
```

---

### GET `/api/documents`

Listet alle Dokumente der Organisation des aktuellen Nutzers auf.

* **URL:** `/api/documents`
* **Methode:** `GET`
* **Authentifizierung:** Cookie/Session

**Erfolgs-Response (200 OK):**

```json
{
  "orgChainAddress": "0xabc123...xyz",
  "contractAddress": "0xdef456...uvw",
  "documents": [
    {
      "idHash": "0xaaaa1111bbbb2222cccc3333dddd4444eeee5555ffff6666gggg7777hhhh8888",
      "documentHash": "0xaaaabbbbcccc1111222233334444dddd",
      "timestamp": 1745919683,
      "txHash": "0xdeadbeefdeadbeefdeadbeefdeadbeef",
      "blockNumber": 42,
      "downloadUrl": "/api/documents/0xaaaa1111bbbb2222cccc3333dddd4444eeee5555ffff6666gggg7777hhhh8888/download"
    },
    {
      "idHash": "0x11112222333344445555666677778888aaaabbbbccccdddd1111222233334444",
      "documentHash": "0x11112222333344445555666677778888",
      "timestamp": 1745919700,
      "txHash": "0xfeedfacefeedfacefeedfacefeedface",
      "blockNumber": 43,
      "downloadUrl": "/api/documents/0x11112222333344445555666677778888aaaabbbbccccdddd1111222233334444/download"
    }
  ]
}
```

*Hinweis: Bei keinem Dokument liefert `documents` eine leere Liste.*

---

### GET `/api/documents/<string:idHash>/download`

Lädt das zuletzt hochgeladene Dokument (Blob) für die angegebene `idHash` herunter.

* **URL:** `/api/documents/<string:idHash>/download`
* **Methode:** `GET`
* **Authentifizierung:** Cookie/Session

**Erfolgs-Response (200 OK):**

* Datei-Download (PDF/Binärdaten)
* Header `Content-Disposition: attachment; filename="<idHash>.pdf"`

**Fehler-Response (404 Not Found):**

* Kein Dokument mit dieser `idHash` gefunden

---

### GET `/api/stats`

Gibt Kennzahlen zur eigenen Organisation zurück.

* **URL:** `/api/stats`
* **Methode:** `GET`
* **Authentifizierung:** Cookie/Session

**Erfolgs-Response (200 OK):**

```json
{
  "orgName": "TestOrg",
  "orgChainAddress": "0xabc123...xyz",
  "contractAddress": "0xdef456...uvw",
  "totalNotarizations": 10,
  "firstNotarization": {
    "documentHash": "0xaaaabbbbcccc11112222",
    "timestamp": 1745919600
  },
  "latestNotarization": {
    "documentHash": "0x9999aaaa0000bbbb1111",
    "timestamp": 1745919700
  }
}
```

*Hinweis: Bei `totalNotarizations` = 0 sind `firstNotarization` und `latestNotarization` `null`.*

---

## Allgemeine Hinweise

* **Zeitstempel:** alle Zeiten im Unix-Epoch-Format (Sekunden seit 1970-01-01 UTC).
* **Session-Cookie:** Der Login (`/login` oder `/login/wallet`) setzt ein Session-Cookie, das bei allen `/api`-Aufrufen mitsendet werden muss.
* **Blockchain-Testnetzwerk:** Starte ein lokales Ethereum-Testnetzwerk (Hardhat oder Ganache) auf `localhost:8545` und deploye den Notary-Contract.
* **CORS:** Bei Frontend unter anderer Origin ggf. CORS in `app/__init__.py` konfigurieren.

---
