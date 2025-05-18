# Contracts-Dokumentation

Dieser Ordner enthält die Solidity-Smart-Contracts, das Deployment-Script und die Unit-Tests für das Projekt.

## Ordnerstruktur

```plaintext
contracts/
├── artifacts/              # Kompilierte Contract-Artefakte
│   ├── build-info/         # Metadaten der Builds
│   └── contracts/          # JSON-ABI und Debug-Informationen
│       └── Notary.sol/     # ABI + Debug für Notary-Contract
├── cache/                  # Hardhat Solidity-Cache
├── contracts/              # Ursprungs-Solidity-Quellen (.sol-Dateien)
├── node_modules/           # Installierte Node.js-Module (npm/yarn)
├── test/                   # Unit-Tests gegen lokale Hardhat-Instanz
│   └── notary.test.js      # Tests für Notary-Contract (nicht up to date)
├── hardhat.config.js       # Hardhat-Konfiguration (Netzwerke, Compiler-Versionen)
├── package.json            # Node.js-Projektdefinition und Skripte (zum Contract kompilieren + in ./frontend/artifacts zu schieben `npm run build`)
└── yarn.lock               # Lockfile für Node-Abhängigkeiten
```

## Datei- und Ordner-Beschreibungen

### `contracts/Notary.sol`

Der zentrale Smart Contract für die Blockchain-Notarisierung von Dokumenten:

* Authorisiert nur Organisation-Admins zum Speichern von Dokument-Hashes
* Emittiert `DocumentNotarized`-Events mit Org-Address, idHash, docHash, Timestamp
* Verhindert doppelte Notarisierung derselben ID innerhalb einer Instanz
* Owner Wallet kann Admin Wallets hinzufügen & entfernen

### `test/notary.test.js`- Veraltet

Unit-Tests mit Hardhat, Chai und Ether.js:

* Autorisierung: nur Org-Admins dürfen notarisieren
* Schutz vor doppelter Notarisierung
* Mehrere Instanzen erlauben gleiche ID in unterschiedlichen Contracts

### `artifacts/`

Enthält alle kompilierten Artefakte (ABIs, Bytecode) für die Deploy- und Test-Läufe.

### `cache/`

Hardhat-internes Cache-Verzeichnis für beschleunigte Kompilierung.

### `hardhat.config.js`

Konfiguration von Hardhat:

* Compiler-Version
* Netzwerkdefinitionen (Sepolia Testnet)

### `package.json` & `yarn.lock`

Node.js-Abhängigkeiten und Skripte