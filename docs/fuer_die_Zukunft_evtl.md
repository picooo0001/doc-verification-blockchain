# Bitte beachten in Zukunft

Damit dein System stabil, sicher und wartbar bleibt, behalte bitte folgende Punkte im Hinterkopf:

---

## 1. Konfigurations- & Secrets-Management
- Nutze für Produktions-Umgebungen starke Zufallswerte für `SECRET_KEY` (nicht den Dev-Fallback).
- Lade sensible Werte (Datenbank-URL, RPC-URL, API-Credentials) ausschließlich aus Umgebungsvariablen oder einem Secret-Manager (.env, Vault, AWS Parameter Store etc.).
- Achte darauf, dass `.env` nicht ins Git-Repository gelangt.

## 2. Sicherheit & Hardening
- **HTTPS**: Setze TLS für alle Endpunkte in Produktion ein.
- **Rate-Limiting**: Schütze Login- und Notarisierungs-Endpoints gegen Brute-Force/DoS (z. B. mit `flask-limiter`).
- **CSRF-Protection**: Wenn du HTML-Forms nutzt, verwende `Flask-WTF`.
- **CORS**: Beschränke `Flask-CORS` auf autorisierte Frontend-Origins.
- **Secure Cookies & HSTS**: Konfiguriere Cookie-Flags (`Secure`, `HttpOnly`, `SameSite`) und HSTS-Header.

## 3. Datenbank-Management
- **Migrations**: Halte Alembic-Migrations im VCS, führe in CI automatisiert `flask db migrate` und `flask db upgrade` aus.
- **Backups**: Richte regelmäßige Backups deiner PostgreSQL-Datenbank (Dump oder Snapshot) ein.
- **Seed-Daten**: Erstelle ein Skript oder CLI-Command, um Development/Testing-Daten zu seed-en.
- **Connection-Pooling**: In Production `SQLALCHEMY_POOL_SIZE` und `POOL_RECYCLE` konfigurieren.

## 4. Testing & CI/CD
- **Unit-Tests**: Nutze SQLite-In-Memory für schnelle Isolationstests oder `pytest-testcontainers` für echte Postgres-Tests.
- **Integrationstests**: Teste End-to-End-Flows (Login → Notarize → Verify) per API-Requests.
- **CI/CD-Pipeline**: Baue Tests und Migrations in deine Pipeline (GitHub Actions, GitLab CI) ein.
- **Linting/Formatting**: Setze `flake8`, `black`, `isort` für konsistenten Code-Stil ein.

## 5. Logging & Monitoring
- **Structured Logging**: Nutze JSON-Logger (`python-json-logger` oder `structlog`) für zentrale Log-Analyse.
- **Error-Tracking**: Integriere Sentry oder Rollbar, um Exceptions in Production zu erfassen.
- **Health-Checks**: Biete einen `/health`-Endpoint an, der DB- und RPC-Verbindung prüft.

## 6. Docker & Deployment
- **Multi-Stage Dockerfile**: Verwende Multi-Stage Builds, um das Image klein zu halten.
- **Docker Compose vs. Kubernetes**: Entwickle lokal mit `docker-compose`, deploye in Prod evtl. mit K8s.
- **Env-Injection**: Setze Umgebungsvariablen as runtime secrets, nicht im Image.
- **Service-Dependencies**: Nutze `depends_on`, aber implementiere Health-Checks im Orchestrator.

## 7. Features Roadmap & Dashboard
- **User-Management**: Admin-UI zur Verwaltung von Mitarbeitern und Rollen.
- **Rollen & Permissions**: Granulares RBAC (Admin, Uploader, Verifier).
- **Audit-Trail**: Lückenlose Historie aller Aktionen (Notarisierungen, Logins).
- **KPIs & Reports**: CSV-Export, Diagramme (Notarisierungen pro Tag, 2FA-Nutzung).
- **Benachrichtigungen**: E-Mail oder Webhooks bei neuen Notarisierungen.
- **API-Versionierung**: OpenAPI/Swagger-Dokumentation und Versionierungsstrategie.

---

Diese Punkte dienen als Leitfaden für zukünftige Erweiterungen und Wartung deines Projekts. Viel Erfolg!

