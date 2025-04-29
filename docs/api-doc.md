# API-Dokumentation

**Basis-URL:** `http://localhost:5001`

---

## POST `/api/notarize`
Notarisiert ein hochgeladenes Dokument in der Blockchain.

**URL**  
`/api/notarize`

**Methode**  
`POST`

**Form-Data**  
| Feldname    | Typ    | Beschreibung                                                           |
|-------------|--------|------------------------------------------------------------------------|
| `file`      | File   | Zu notarisiertes PDF/Binärdaten                                        |
| `documentId`| String | Eindeutige ID, unter der das Dokument notariell hinterlegt werden soll |

**Erfolgs-Response (200 OK)**  
```json
{
  "txHash": "0x6988...",
  "blockNumber": 2
}
```

**Fehler-Responses (400 Bad Request)**  
```json
{ "error": "No file provided" }
{ "error": "No documentId provided" }
{ "error": "Dokument darf nicht geändert werden" }
{ "error": "Schon notariell hinterlegt" }
```
- **500 Internal Server Error**

---

## POST `/api/verify`
Prüft, ob ein Dokument bereits notariell hinterlegt ist.

**URL**  
`/api/verify`

**Methode**  
`POST`

**Form-Data**  
| Feldname | Typ  | Beschreibung                      |
|----------|------|-----------------------------------|
| `file`   | File | Zu verifizierendes PDF/Binärdaten |

**Erfolgs-Response (200 OK)**  
```json
{
  "verified": true,
  "timestamp": 1745919683
}
```

**Fehler-Responses**  
- **400 Bad Request**  
```json
{ "error": "No file provided" }
```
- **404 Not Found**  
```json
{ "verified": false }
```

---

## POST `/login`
Authentifiziert einen Benutzer mit E-Mail, Passwort und OTP.

**URL**  
`/login`

**Methode**  
`POST`

**Form-Data**  
| Feldname | Typ    | Beschreibung                                    |
|----------|--------|-------------------------------------------------|
| `email`  | String | E-Mail-Adresse des Benutzers                    |
| `password`| String| Klartext-Passwort                               |
| `otp`    | String | Zeitbasiertes Einmal-Passwort (6-stellig) *optional* |

**Erfolgs-Response (200 OK)**  
```json
{ "message": "Login erfolgreich" }
```

**Fehler-Responses**  
- **401 Unauthorized**  
```json
{ "error": "Ungültige E-Mail oder Passwort" }
{ "error": "Ungültiges OTP" }
```

---

## POST `/logout`
Loggt den aktuell eingeloggten Benutzer aus.

**URL**  
`/logout`

**Methode**  
`POST`

**Erfolgs-Response (200 OK)**  
```json
{ "message": "Logout erfolgreich" }
```

---

## GET `/setup-2fa`
Gibt dem eingeloggten Benutzer sein OTP-Secret, die Provisioning-URI und einen QR-Code zurück, damit er 2-Faktor-Authentifizierung in seiner Authenticator-App einrichten kann.

**URL**
`/setup-2fa`

**Methode**
`GET`

**Authentifizierung**
Erofrdert gültige Session (Cookie) via Flask-Login.

**Erfolgs-Response (200 OK)**
```json
{
  "otp_secret": "JBSWY3DPEHPK3PXP",
  "provisioning_uri": "otpauth://totp/DocNotary:alice%40test.org?secret=JBSWY3DPEHPK3PXP&issuer=DocNotary",
  "qr_code_png_base64": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```
- **otp_secret**: Base32-endcodeter Schlüssel für TOTP-Apps
- **provisoning_uri**: URI zum Import in Autehnticatior-Apps (RFC 6238)
- **qr_code_png_base64**: QR-Code als Base64-PNG

**Fehler-Responses**
- **401 Unauthorized**
```json
{ "error": "Authentication required" }
```

## Hinweise

- Der `timestamp` wird im Unix-Epoch-Format (Sekunden seit 1970-01-01 UTC) zurückgegeben.
- OTPs sind 6-stellig und basieren auf dem Secret, das bei der User-Anlage ausgegeben wurde. Ein Zeitfenster von ±30 Sekunden wird akzeptiert.
- Standard-Port des Backends: `5001`.
- Für lokale Tests: Stelle sicher, dass der Hardhat-Node auf `localhost:8545` läuft und der Notary-Contract deployed ist.
- CORS: Wenn das Frontend auf einer anderen Origin läuft, konfiguriere CORS in `app/__init__.py`.
- Session-Cookie: `/login`, `/logout` und `/setup-2fa setzen` bzw. benötigen das Flask-Login-Cookie.

