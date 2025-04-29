# API-Dokumentation

**Basis-URL:** `http://localhost:5001/api`

---

## POST `/notarize`

Notarisiert ein hochgeladenes Dokument in der Blockchain.

**URL**  
`/notarize`

**Methode**  
`POST`

**Form-Data**  
| Feldname | Typ  | Beschreibung                    |
|----------|------|---------------------------------|
| file     | File | Zu notarisiertes PDF/Binärdaten |
| documentId     | String | Eindeutige ID, unter der das Dokument notariell hinterlegt werden soll |


**Erfolgs-Response (200 OK)**  
```json
{
  "txHash": "0x6988c3d48bbcdf7fc10740c1eb80ef93bcf59285526bba2c3ddb81edaeee723e",
  "blockNumber": 2
}
````
**Fehler-Responses**
- 400 Bad Request
```json
{ "error": "No file provided" }

{ "error": "No documentId provided" }

{ "error": "Dokument darf nicht geändert werden" }

{ "error": "Schon notariell hinterlegt" }
```
- 500 Internal Server Error

## POST `/verify`

Prüft, ob ein Dokument bereits notariell hinterlegt ist.

**URL**  
`/verify`

**Methode**  
`POST`

**Form-Data**  
| Feldname | Typ  | Beschreibung                    |
|----------|------|---------------------------------|
| file     | File | Zu verifizierendes PDF/Binärdaten |

**Erfolgs-Response (200 OK)**  
```json
{
  "verified": true,
  "timestamp": 1745919683
}
````
**Fehler-Responses**
- 404 Not Found
```json
{ "verified": false }
```
- 400 Bad Request
```json
{ "error": "No file provided" }
```

## Hinweise
- Der timestamp ist im Unix-Epoch-Format (Sekunden seit 1970-01-01 UTC).

- Standard-Port des Backends: 5001.

- Für lokale Tests: Stelle sicher, dass der Hardhat-Node auf localhost:8545 läuft und der Notary-Contract deployed ist.

- Falls das Frontend auf einer anderen Origin läuft, teste und konfiguriere CORS in app/__init__.py.
