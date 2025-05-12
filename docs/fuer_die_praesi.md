# Wichtige Punkte für die Präsentation
## Welche Vorteile bringt die Blockchain Technologie mit sich?
- Unveränderbarkeit (Immutability): Hash-Werte, die einmal hinterlegt wurden sind in der Blockchain festgeschrieben und nachträglich nicht mehr änderbar (Das Gleiche ist auch bei unseren PDFs der Fall. Dokument wird hochgeladen und direkt in der DB gespeichert)
- Nachvollziehbarkeit -> Jeder Notarisierung wird protokolliert als Transaktion -> Lässt sich nachvollziehen (naja bei uns nicht ganz weil jeder mit der gleichen Adresse hochlädt, wäre ein Thema für die Herausforderungen...)
- Dezentralisierung: kein Single-Point-of-Failure. Wenn einzelen "Nodes" ausfallen schränkt das das Netzwerk nicht ein (auch eher auf Testnetz anwendbar)
- Vertrauensfreiheit: Nutzer müssen keiner zentralen Instanz trauen -> Integrität wird kryptisch dargestellt druch Hash-Werte (Kollisionen ausgeschlossen)
- Zeitstempel beweist dass Dokument X zumindest zu einem Zeitpunkt exisiterte
## Was hat Cybersecurity mit unserem Thema zu tun?
- Integrität: Blockchain nutzt kryptografische Hash-Funktionen und digitale Signaturen -> stellt sicher dass Daten nicht unbemerkt geändert werden können
- Authentifizierung & Autorisierung: Über Wallet Login wird sichergestellt dass nur berechtigte Addressen auf die Plattfrom innerhalb einer Org zugreifen dürfen (und somit auch per Org-Admins Addy signieren)
- Vertraulichkeit: Hash-Werte sind zwar öffentlich gespeichert (im Testnet), die Originaldokumente liegen jedoch lokal in der DB
- Verfügbarkeit: Durch die Blockchain wird sichergestell, dass die der Content verfügbar ist, auch wenn einige Nodes ausfallen.
- Schutz vor Replay: Die Anatomie des Smart Contracts verhindert doppelte Notarisierungen

## Zusammenfassung
- manipulationssicher, transparent, dezentral -> nur autorisierte Akteure können agieren

## Folienideen
### Herausforderungen: 
- "neue Technologie" -> vieles nicht 100% gut notiert
- public Testnet vs. lokales Testnet
    - Schritt von lokalem Testnet zu öffentlichem Testnet groß (Wallets, benötigte API Keys, Anpassungen im Code da nur lokal gedacht)
- Wallet Integration (lokal = eine zentrale Wallet die Transaktionen signiert vs public testnet = eigene Wallets)
- Balance zwischen Dezentralisierung und Zentralisierung (Transaktionen sind dezentral in der Blockchain während die pdf Dateien lokal in der Datenbank liegen)
- viel "hardcoded" im lokalen Testnet (Wallet keys etc. öffentlich - feste Zuweisung der Org Wallets)
- hohe Komplexität (Backend - Contracts / Backend - Frontend)

### Umsetzung (lokal):
- Ausschnitte aus Notary.sol / Routen (/notarize) zeigen + erklären anhand von Screenshots in der Präsi (immer wieder Bogen schlafen zu den Keypoints (Warum wichtig für Cybersecurity?)
- Eine Art Roadmap mit den verschiedenen Schritten (Iterationen die immer wieder durchlaufen wurden):
    - Contract erstellen, kompilieren
    - lokales Netz deployen
    - Backend anpassen / Routen hinzufügen
    - Backend Endpunkte ins Frontend integrieren 
    - alles wieder von vorne

### Migration ins Testnetz (optional):
- Wie sind wir vorgegangen, um die Applikation auch im Testnet zu "etablieren"? Code Änderungen, Änderungen im Smart Contract etc..

### Ausblick / Wie könnte es weitergehen?
- Funktionen: jeder User signiert selbst in Zukunft mit eigener Wallet
- Verwaltbarer machen:
    - Admin Panel: 
        - jemand muss prüfen, wer berechtigt ist Funktionen zu nutzen (Wallet whitlisten über GUI)
        - User einer Orga managen
    - Smart Contract Code anzeigen -> fördert Transparenz
    - Mit etherscan.io für mehr Insights arbeiten

### Was existiert schon im Markt (optional):
- Gibt es ähnliche Plattfromen schon / was wird anders gemacht?
- Ist das in DE / EU überhaupt möglich -> Gesetzeslage
- Würde das überhaupt auf Akzeptanz stoßen?

## Allgemeine Anmerkunden
- Ist das Elefanten Icon wirklich für Postgres?

