# Contracts-Dokumentation

Dieser Ordner enthält die Solidity-Smart-Contracts, das Deployment-Script und die Unit-Tests für das Projekt.

## Ordnerstruktur

```plaintext
contracts/
├── artifacts/              # Kompilierte Contract-Artefakte
│   ├── build-info/         # Metadaten der Builds
│   └── contracts/          # JSON-ABI und Debug-Informationen
│       ├── Lock.sol/       # ABI + Debug für Lock-Contract
│       └── Notary.sol/     # ABI + Debug für Notary-Contract
├── cache/                  # Hardhat Solidity-Cache
├── contracts/              # Ursprungs-Solidity-Quellen (.sol-Dateien)
├── node_modules/           # Installierte Node.js-Module (npm/yarn)
├── scripts/                # Deployment- und Hilfsskripte
│   └── deploy.js           # Deployment-Script für mehrere Organisations-Instanzen
├── test/                   # Unit-Tests gegen lokale Hardhat-Instanz
│   └── notary.test.js      # Tests für Notary-Contract (Autorisierung, doppelte Notarisierung etc.)
├── deployed-contracts.json # Ausgabedatei mit deployed Adressen (orgA, orgB)
├── hardhat.config.js       # Hardhat-Konfiguration (Netzwerke, Compiler-Versionen)
├── package.json            # Node.js-Projektdefinition und Skripte
└── yarn.lock               # Lockfile für Node-Abhängigkeiten
```

## Datei- und Ordner-Beschreibungen

### `contracts/Notary.sol`

Der zentrale Smart Contract für die Blockchain-Notarisierung von Dokumenten:

* Authorisiert nur Organisation-Admins zum Speichern von Dokument-Hashes
* Emittiert `DocumentNotarized`-Events mit Org-Address, idHash, docHash, Timestamp
* Verhindert doppelte Notarisierung derselben ID innerhalb einer Instanz

### `contracts/Lock.sol`

Ein einfaches Beispiel-Contract (Lock), standardmäßig von Hardhat-Init-Template.

### `scripts/deploy.js`

Deployment-Skript (Node.js) für zwei Organisationen:

1. Holt Signer (Deployer, Org A/B, Admins)
2. Deployt je eine Instanz von `Notary` für Org A und Org B
3. Fügt Admin-Adressen hinzu (`addOrgAdmin`)
4. Schreibt die Contract-Adressen in `deployed-contracts.json` für die Nachnutzung

### `test/notary.test.js`

Unit-Tests mit Hardhat, Chai und Ether.js:

* Autorisierung: nur Org-Admins dürfen notarisieren
* Schutz vor doppelter Notarisierung
* Mehrere Instanzen erlauben gleiche ID in unterschiedlichen Contracts

### `artifacts/`

Enthält alle kompilierten Artefakte (ABIs, Bytecode) für die Deploy- und Test-Läufe.

### `cache/`

Hardhat-internes Cache-Verzeichnis für beschleunigte Kompilierung.

### `deployed-contracts.json`

Ergebnis des Deploy-Skripts mit Struktur:

```json
{
  "orgA": "0x...",
  "orgB": "0x..."
}
```

### `hardhat.config.js`

Konfiguration von Hardhat:

* Compiler-Version
* Netzwerkdefinitionen (z. B. `localhost` auf `127.0.0.1:8545`)
* Pfade für Artefakte und Cache

### `package.json` & `yarn.lock`

Node.js-Abhängigkeiten und Skripte:

* `npm run test` → führt `notary.test.js` aus
* `npm run deploy` → ruft `scripts/deploy.js` auf