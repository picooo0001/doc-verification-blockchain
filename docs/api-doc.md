# API-Dokumentation

**Base URL:**

- Auth-Routes: ``http://localhost:5001``

- Notary-Routes: ``http://localhost:5001/api``

---

## Authentifizierung & Nutzer

### POST `/login`
Authentifiziert einen Benutzer (Form-Data oder JSON).

**Methode**  
`POST`

**Request Body**  
**Form-Data**  
  | Feld     | Typ    | Beschreibung                     |
  |----------|--------|----------------------------------|
  | `email`  | String | E-Mail-Adresse des Benutzers     |
  | `password` | String | Klartext-Passwort               |
  | `otp`    | String | Einmal-Passwort (6-stellig), falls 2FA aktiv |

**JSON**  
  ```json
  {
    "email": "alice@test.org",
    "password": "Secret123",
    "otp": "123456"          // optional, nur wenn 2FA eingerichtet
  }

**Erfolgs-Response (200 OK)**  
```json
{ "message": "Login erfolgreich" }
```

**Fehler-Responses (400 Bad Request)**  
```json
{ "error": "Ungültige E-Mail oder Passwort" }
{ "error": "2FA erforderlich" }
{ "error": "Ungültiges OTP" }
```
---

### POST `/logout`
Loggt den aktuell eingeloggten Benutzer aus.

**URL**  
`/logout`

**Methode**  
`POST`

**Authentifizierung**  
Cookie / Session via Flask-Login


**Erfolgs-Response (200 OK)**  
```json
{ "message": "Logout erfolgreich" }
```
---

### GET `/setup-2fa`
Erzeugt (falls noch nicht vorhanden) ein neues TOTP-Secret für den eingeloggten Benutzer und liefert Secret, Provisioning-URI & QR-Code.

**URL**  
`/setup-2fa`

**Methode**  
`GET`

**Erfolgs-Response (200 OK)**
``` json
{
  "otp_secret": "JBSWY3DPEHPK3PXP",
  "provisioning_uri": "otpauth://totp/DocNotary:alice%40test.org?secret=JBSWY3DPEHPK3PXP&issuer=DocNotary",
  "qr_code_png_base64": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```

**Fehler-Responses**  
- **401 Unauthorized**  
```json
{ "error": "Authentication required" }
```

---

### POST `/user/2fa`
Aktiviert oder deaktiviert 2-Faktor-Authentifizierung für den eingeloggten Benutzer.

**URL**  
`/user/2fa`

**Methode**  
`POST`

**Authentifizierung**
Cookie / Session

**Request Body (JSON)**  
```json
{ "enable": true }   // oder false
```

**Erfolgs-Response (200 OK)**

- Aktivieren
```json
{
  "message": "2FA aktiviert",
  "otp_secret": "JBSWY3DPEHPK3PXP",
  "provisioning_uri": "otpauth://…",
  "qr_code_png_base64": "iVBORw0KG…"
}
```
- Dekativieren
```json
{ "message": "2FA deaktiviert" }
```
---

## GET `/user/profile`
Gibt Profildaten des eingeloggten Nutzers zurück.

**URL**
`/user/profile`

**Methode**  
`GET`

**Authentifizierung**
Cookie / Session

**Erfolgs-Response (200 OK)**
```json
{
  "email": "alice@test.org",
  "organization": "TestOrg",
  "2faEnabled": true
}
```
---
## Notatisierung & Verifikation

Alle folgenden Routen erfordern Authentifizierung (Cookie / Session).

### POST `/api/notarize`
Notarisiert ein Dokument in der Blockchain.

**URL**
`/api/notarize`

**Methode**  
`POST`

**Form-Data**
| Feld     | Typ    | Beschreibung                     |
|----------|--------|----------------------------------|
| `file`  | File | Zu notarisierende PDF/Binärdatei     |
| `documentId` | String | Eindeutige ID, unter der das Dokument hinterlegt werden soll|

**Erfolgs-Response (200 OK)**
```json
{
  "txHash": "0x6988…",
  "blockNumber": 42
}
```

**Fehler-Responses (400 Bad Request)**

```json
{ "error": "No file provided" }
{ "error": "No documentId provided" }
{ "error": "Dokument darf nicht geändert werden" }
{ "error": "Schon notariell hinterlegt" }
```
---
### POST `/api/verify`
Prüft, ob ein Dokument bereits notariell hinterlegt ist.

**URL**
`/api/verify`

**Methode**  
`POST`

**Form-Data**
| Feld     | Typ    | Beschreibung                     |
|----------|--------|----------------------------------|
| `file`  | File | Zu verifizierendes PDF/Binärdatei     |

**Erfolgs-Response (200 OK)**
```json
{
  "verified": true,
  "timestamp": 1745919683
}
```
**Fehler Responses**
- 403 Forbidden
```json
{ "error": "Nicht berechtigt" }
````
- 404 Not found
```json
{ "error": "Document not found" }
```
---
### GET /api/documents/<documentId>/history
Zeigt die vollständige Notarisierungs-Historie zu einer documentId.

**URL**
`/api/documents/`{documentId}`/history`

**Methode**  
`GET`

**Erfolgs Response**
```json
[
  {
    "documentHash": "0xdef456…",
    "timestamp":    1745919683,
    "txHash":       "0xdeadbeef…",
    "blockNumber":  42
  },
  {
    "documentHash": "0xfeedface…",
    "timestamp":    1745919700,
    "txHash":       "0xfacefeed…",
    "blockNumber":  43
  }
]
```
**Fehler Response**
```json
{ "error": "Nicht berechtigt" }
```
---
### GET /api/stats
Gibt Kennzahlen für die eigene Organisation aus.

**URL**
`/api/stats`

**Methode**  
`GET`

**Erfolgs Response**
```json
{
  "totalNotarizations": 10,
  "latestNotarization": {
    "documentHash": "0xdef456…",
    "timestamp":    1745919683
  }
}
```
---
## Allgemeine Hinweise

- Alle Zeitstempel im Unix-Epoch-Format (Sekunden seit 1970-01-01 UTC).

- Session-Cookie wird über /login gesetzt und für alle /api-Routen benötigt.

- Für lokale Tests: Hardhat-Node auf localhost:8545 und Notary-Contract deployed.

- CORS: Bei Frontend auf anderer Origin bitte in app/__init__.py konfigurieren.


