# API Documentation

**Basis-URL:** `http://localhost:5001/api`
Authentifizierung via Session-Cookie (Flask-Login) oder Wallet-Signatur.

---

## Authentifizierung & Nutzerverwaltung

### GET `/login/nonce`

Erzeugt eine einmalige Nonce für Wallet-Login.

* **URL:** `/login/nonce?address={walletAddress}`
* **Methode:** `GET`
* **Auth:** keine
* **Query-Parameter:**

  * `address` (string): Ethereum-Adresse

**Antworten:**

* **200 OK**

  ```json
  { "nonce": "d4f2a9b1c3e5..." }
  ```
* **400 Bad Request**

  ```json
  { "error": "Ungültige Adresse" }
  { "error": "Ungültiges Adress-Format" }
  ```
* **404 Not Found**

  ```json
  { "error": "Adresse nicht registriert" }
  ```

---

### POST `/login/wallet`

Login per Ethereum-Wallet-Signatur.

* **URL:** `/login/wallet`
* **Methode:** `POST`
* **Auth:** keine
* **Body (JSON):**

  ```json
  {
    "address": "0xAbc123...def",
    "signature": "0x5f3b..."
  }
  ```

**Antworten:**

* **200 OK**

  ```json
  {
    "message": "Login erfolgreich",
    "user": {
      "id": 1,
      "email": "alice@test.org",
      "isOwner": false,
      "organizationId": 42,
      "wallet": "0xAbc123...def"
    }
  }
  ```
* **400 Bad Request**

  ```json
  { "error": "Ungültige Adresse" }
  { "error": "Ungültiges Adress-Format" }
  ```
* **401 Unauthorized**

  ```json
  { "error": "Nonce nicht gefunden" }
  { "error": "Signatur ungültig" }
  { "error": "Address mismatch" }
  ```

---

### POST `/login`

Login per E-Mail/Passwort mit optionalem 2FA (TOTP).

* **URL:** `/login`
* **Methode:** `POST`
* **Auth:** keine
* **Body (Form-Data oder JSON):**

  | Feld     | Typ    | Beschreibung                              |
  | -------- | ------ | ----------------------------------------- |
  | email    | string | E-Mail des Nutzers                        |
  | password | string | Klartext-Passwort                         |
  | otp      | string | TOTP-Code, falls 2FA aktiviert (optional) |

**Antworten:**

* **200 OK**

  ```json
  {
    "message": "Login erfolgreich",
    "user": {
      "id": 1,
      "email": "alice@test.org",
      "isOwner": false,
      "organizationId": 42,
      "wallet": "0xAbc123...def"
    }
  }
  ```
* **401 Unauthorized**

  ```json
  { "error": "Ungültige E-Mail oder Passwort" }
  { "error": "2FA erforderlich" }
  { "error": "Ungültiges OTP" }
  ```

---

### POST `/logout`

Loggt den aktuellen Benutzer aus.

* **URL:** `/logout`
* **Methode:** `POST`
* **Auth:** Session-Cookie

**Antwort:**

* **200 OK**

  ```json
  { "message": "Logout erfolgreich" }
  ```

---

### GET `/setup-2fa`

Erzeugt OTP-Secret, Provisioning-URI und QR-Code.

* **URL:** `/setup-2fa`
* **Methode:** `GET`
* **Auth:** Session-Cookie

**Antwort (200 OK):**

```json
{
  "otp_secret": "JBSWY3DPEHPK3PXP",
  "provisioning_uri": "otpauth://totp/DocNotary:alice%40test.org?secret=…&issuer=DocNotary",
  "qr_code_png_base64": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```

---

### POST `/user/2fa`

Aktiviert oder deaktiviert 2FA für den eingeloggten Nutzer.

* **URL:** `/user/2fa`
* **Methode:** `POST`
* **Auth:** Session-Cookie
* **Body (JSON):**

  ```json
  { "enable": true }
  ```

**Antworten:**

* **200 OK** (Aktivierung)

  ```json
  {
    "message": "2FA aktiviert",
    "otp_secret": "...",
    "provisioning_uri": "...",
    "qr_code_png_base64": "..."
  }
  ```
* **200 OK** (Deaktivierung)

  ```json
  { "message": "2FA deaktiviert" }
  ```

---

### GET `/user/profile`

Gibt Profildaten des aktuellen Nutzers zurück.

* **URL:** `/user/profile`
* **Methode:** `GET`
* **Auth:** Session-Cookie

**Antwort (200 OK):**

```json
{
  "email": "alice@test.org",
  "organization": "TestOrg",
  "2faEnabled": true,
  "walletAddress": "0xAbc123...def",
  "isOwner": false
}
```

---

## Notarisierung & Dokumentenverwaltung

> **Hinweis:** alle folgenden Endpoints erfordern Session-Cookie (Flask-Login) und sind unter `/api` registriert.

---

### POST `/hashes`

Berechnet `idHash` und `docHash` für ein Dokument.

* **URL:** `/hashes`
* **Methode:** `POST`
* **Auth:** Session-Cookie
* **Form-Data:**

  | Feld       | Typ    | Beschreibung             |
  | ---------- | ------ | ------------------------ |
  | file       | File   | Hochzuladende Datei      |
  | documentId | string | Eindeutige Dokumenten-ID |

**Antworten:**

* **200 OK**

  ```json
  {
    "idHash": "0x…",
    "docHash": "0x…"
  }
  ```
* **400 Bad Request**

  ```json
  { "error": "file und documentId nötig" }
  ```

---

### POST `/notarize/commit`

Speichert das Dokument endgültig mit Transaktions-Hash ab.

* **URL:** `/notarize/commit`
* **Methode:** `POST`
* **Auth:** Session-Cookie
* **Body (JSON):**

  ```json
  {
    "idHash": "0x…",
    "txHash": "0x…"
  }
  ```

**Antworten:**

* **200 OK**

  ```json
  { "success": true }
  ```
* **404 Not Found**

  ```json
  { "error": "Keine vorbereitete Datei gefunden" }
  ```

---

### POST `/verify`

Prüft, ob ein Dokument bereits notariell registriert wurde.

* **URL:** `/verify`
* **Methode:** `POST`
* **Auth:** Session-Cookie
* **Form-Data:**

  | Feld | Typ  | Beschreibung      |
  | ---- | ---- | ----------------- |
  | file | File | Zu prüfende Datei |

**Antworten:**

* **200 OK**

  ```json
  { "verified": true, "timestamp": 1745919683 }
  ```
* **400 Bad Request**

  ```json
  { "error": "No file provided" }
  ```
* **404 Not Found**

  ```json
  { "verified": false }
  ```

---

### GET `/documents`

Listet alle notariellen Dokumente der eigenen Organisation.

* **URL:** `/documents`
* **Methode:** `GET`
* **Auth:** Session-Cookie

**Antwort (200 OK):**

```json
{
  "orgChainAddress": "0xabc123…",
  "contractAddress": "0xdef456…",
  "documents": [
    {
      "idHash": "0x…",
      "documentHash": "0x…",
      "timestamp": 1745919683,
      "isoTimestamp": "2025-05-18T12:34:56Z",
      "blockNumber": 42,
      "txHash": "0x…",
      "downloadUrl": "/documents/0x…/download"
    }
  ]
}
```

---

### GET `/documents/{idHash}/download`

Lädt das zuletzt gespeicherte Dokument-Blob herunter.

* **URL:** `/documents/{idHash}/download`
* **Methode:** `GET`
* **Auth:** Session-Cookie

**Antworten:**

* **200 OK**
  Datei als Attachment `Content-Disposition: attachment; filename="{idHash}.pdf"`
* **404 Not Found**
  Kein Dokument gefunden.

---

### GET `/stats`

Stellt Statistiken zu Notarisierungen der Organisation bereit.

* **URL:** `/stats`
* **Methode:** `GET`
* **Auth:** Session-Cookie

**Antwort (200 OK):**

```json
{
  "contractAddress": "0xdef456…",
  "contractCreator": "0xowner…",
  "deployBlock": 10,
  "totalNotarizations": 5,
  "firstNotarization": { "timestamp": 1745919600, "documentHash": "0x…" },
  "latestNotarization": { "timestamp": 1745919700, "documentHash": "0x…" }
}
```

---

## Admin-Routen (Organisation-Owner)

### GET `/orgs/{org_id}/users`

Listet alle Nutzer einer Organisation auf (nur Owner).

* **URL:** `/orgs/{org_id}/users`
* **Methode:** `GET`
* **Auth:** Session-Cookie + Owner-Rechte

**Antwort (200 OK):**

```json
{
  "users": [
    { "id": 1, "email": "a@x.de", "wallet": "0x…", "is_owner": true }
  ]
}
```

---

### PUT `/users/{user_id}/wallet`

Aktualisiert die Wallet-Adresse eines Nutzers (nur Owner).

* **URL:** `/users/{user_id}/wallet`
* **Methode:** `PUT`
* **Auth:** Session-Cookie + Owner-Rechte
* **Body (JSON):**

  ```json
  { "wallet": "0xNewAddress…" }
  ```

**Antworten:**

* **200 OK**

  ```json
  { "wallet": "0xNewAddress…" }
  ```
* **400 Bad Request**

  ```json
  { "error": "Ungültige Adresse" }
  ```
* **403 Forbidden**
  Kein Owner oder falsche Organisation.

---

### POST `/orgs/{org_id}/contract`

Setzt Smart-Contract-Adresse und optionalen Deploy-Block (nur Owner).

* **URL:** `/orgs/{org_id}/contract`
* **Methode:** `POST`
* **Auth:** Session-Cookie + Owner-Rechte
* **Body (JSON):**

  ```json
  {
    "contractAddress": "0xContract…",
    "deployBlock": 123
  }
  ```

**Antworten:**

* **200 OK**

  ```json
  {
    "contractAddress": "0xContract…",
    "deployBlock": 123
  }
  ```
* **400 Bad Request**

  ```json
  { "error": "Keine contractAddress übergeben" }
  { "error": "Ungültige Ethereum-Adresse" }
  ```
* **403 Forbidden**, **404 Not Found**

---

### GET `/get_contract_address`

Gibt gespeicherte Contract-Adresse der Organisation und Org-ID zurück.

* **URL:** `/get_contract_address`
* **Methode:** `GET`
* **Auth:** Session-Cookie

**Antwort (200 OK):**

```json
{
  "contractAddress": "0x…",
  "organization_id": 42
}
```

**404 Not Found**

```json
{ "error": "Keine Contract-Adresse für diese Organisation hinterlegt" }
```

---

### GET `/get_org_id`

Gibt die ID der Organisation des aktuellen Nutzers zurück.

* **URL:** `/get_org_id`
* **Methode:** `GET`
* **Auth:** Session-Cookie

**Antwort (200 OK):**

```json
{ "organization_id": 42 }
```
