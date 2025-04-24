<template>
  <div class="about-container">
    <h1>Über dieses Projekt</h1>
    <p>
      Dieses Projekt mit dem Arbeitstitel <strong>„Blockchain-basierte Dokumentenverifikation und Notarisierung“</strong> befasst sich mit der Entwicklung eines webbasierten Prototyps, der die Integrität und Echtheit digitaler Dokumente mithilfe der Blockchain-Technologie sicherstellt. Im Zentrum steht die Signierung und Verifikation von PDF-Dokumenten über Smart Contracts auf einer Ethereum-Test-Blockchain.
    </p>

    <h2>Einleitung</h2>
    <p>
      Die Blockchain-Technologie gewinnt zunehmend an Bedeutung im Bereich der Cyber-Security. Insbesondere für Szenarien wie Dokumentenverifikation und Notarisierung bietet sie Vorteile wie Transparenz, Unveränderbarkeit und Dezentralität. Dieses Projekt nutzt genau diese Eigenschaften, um einen Prototypen zur sicheren Dokumentensignatur zu realisieren.
    </p>

    <h2>Projektaufbau</h2>
    <ul>
      <li><strong>Frontend:</strong> Vue.js mit PrimeVue-Komponenten für ein intuitives UI</li>
      <li><strong>Backend:</strong> Node.js API für Upload, Hashing und Kommunikation mit der Blockchain</li>
      <li><strong>Blockchain-Schnittstelle:</strong> Interaktion über Web3 mit einem Smart Contract in Solidity</li>
      <li><strong>Systemarchitektur:</strong> Klare Trennung von UI, Logik und Blockchain-Komponenten</li>
    </ul>

    <h2>Technologie-Stack</h2>
    <ul>
      <li>Ethereum Testnetz (z. B. Sepolia)</li>
      <li>Smart Contracts in Solidity</li>
      <li>IPFS zur optionalen dezentralen Dateiablage</li>
      <li>Node.js + Express im Backend</li>
      <li>Vue 3 mit PrimeVue im Frontend</li>
    </ul>

    <h2>Use Case</h2>
    <p>
      Der Hauptanwendungsfall liegt in der Signierung von PDF-Dokumenten, z. B. Verträgen oder Zertifikaten, durch Erzeugung eines Hash-Wertes und dessen Speicherung auf der Blockchain. Eine spätere Verifikation erfolgt durch Vergleich des aktuellen Dokument-Hashes mit dem gespeicherten Eintrag.
    </p>

    <h2>Fazit & Ausblick</h2>
    <p>
      Die entwickelte Lösung zeigt, wie Blockchain-Technologie zur digitalen Vertrauensbildung beitragen kann. In Zukunft könnten Erweiterungen wie Mehrfachsignaturen, NFT-basierte Besitznachweise oder eine Einbindung in Behördenprozesse denkbar sein.
    </p>
  </div>
</template>

<style scoped>
.about-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  font-family: -apple-system, BlinkMacSystemFont, 'San Francisco', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.about-container h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.about-container h2 {
  margin-top: 2rem;
  font-size: 1.75rem;
}

.about-container p, li {
  font-size: 1.125rem;
  line-height: 1.6;
}
</style>
